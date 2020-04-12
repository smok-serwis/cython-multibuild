import hashlib
import os
import collections
import typing as tp
import logging
import uuid

import pkg_resources
from satella.files import split, read_re_sub_and_write
from satella.coding.structures import KeyAwareDefaultDict
from mako.template import Template
from setuptools import Extension

logger = logging.getLogger(__name__)


CdefSection = collections.namedtuple('CdefSection', ('h_file_name', 'module_name', 'coded_module_name'))
GetDefinitionSection = collections.namedtuple('GetDefinitionSection', (
    'module_name', 'pyinit_name', 'coded_module_name'
))


def load_mako_lines(template_name: str) -> tp.List[str]:
    return pkg_resources.resource_string('snakehouse', os.path.join('templates', template_name)).decode('utf8')


def cull_path(path):
    if not path:
        return path
    if path[0] == os.path.sep:
        if len(path) > 1:
            if path[1] == os.path.sep:
                return path[2:]
        return path[1:]
    else:
        return path


def render_mako(template_name: str, **kwargs) -> str:
    tpl = Template(pkg_resources.resource_string(
        'snakehouse', os.path.join('templates', template_name)).decode('utf8'))
    return tpl.render(**kwargs)

LINES_IN_HFILE = len(load_mako_lines('hfile.mako').split('\n'))


class Multibuild:
    """
    This specifies a single Cython extension, called {extension_name}.__bootstrap__
    """
    def __init__(self, extension_name: str, files: tp.Iterator[str]):
        """
        :param extension_name: the module name
        :param files: list of pyx and c files
        """
        # sanitize path separators so that Linux-style paths are supported on Windows
        files = list(files)
        files = [os.path.join(*split(file)) for file in files]
        self.files = list([file for file in files if not file.endswith('__bootstrap__.pyx')])

        self.pyx_files = [file for file in files if file.endswith('.pyx')]

        self.extension_name = extension_name        # type: str
        if len(self.files) == 1:
            self.bootstrap_directory, _ = os.path.split(self.files[0])      # type: str
        else:
            self.bootstrap_directory = os.path.commonpath(self.files)       # type: str
        self.modules = []    # type: tp.List[tp.Tuple[str, str, str]]
        self.module_name_to_loader_function = KeyAwareDefaultDict(Multibuild.provide_default_hash)

    @staticmethod
    def provide_default_hash(path):
        with open(path, 'rb') as f_in:
            data = f_in.read()
        return hashlib.sha256(data).hexdigest()

    def generate_header_files(self):
        for filename in self.pyx_files:
            path, name, module_name, coded_module_name, complete_module_name = self.transform_module_name(filename)
            if not name.endswith('.pyx'):
                continue

            h_name = name.replace('.pyx', '.h')
            logger.warning('Header file h_name is %s %s' % (path, h_name))
            h_file = os.path.join(path, h_name)
            if os.path.exists(h_file):
                with open(h_file) as f_in:
                    data = f_in.readlines()

                linesep = 'cr' if '\r\n' in data[0] else 'lf'

                if not any('PyObject* PyInit_' in line for line in data):
                    data = [render_mako('hfile.mako', initpy_name=coded_module_name)+ \
                            '\r\n' if linesep == 'cr' else '\n'] + data[LINES_IN_HFILE:]
            else:
                data = render_mako('hfile.mako', initpy_name=coded_module_name)

            with open(h_file, 'w') as f_out:
                f_out.write(''.join(data))

    def transform_module_name(self, filename):
        path, name = os.path.split(filename)
        module_name = name.replace('.pyx', '')
        if path.startswith(self.bootstrap_directory):
            cmod_name_path = path[len(self.bootstrap_directory):]
        else:
            cmod_name_path = path
        path = cull_path(path)

        if path:
            intro = '.'.join((e for e in cmod_name_path.split(os.path.sep) if e))
            if not intro:
                complete_module_name = '%s.%s' % (self.extension_name, module_name)
            else:
                complete_module_name = '%s.%s.%s' % (self.extension_name,
                                                     intro,
                                                     module_name)
        else:
            complete_module_name = '%s.%s' % (self.extension_name, module_name)

        coded_module_name = self.module_name_to_loader_function[filename]
        logger.warning('Invoking with %s %s %s', module_name, coded_module_name, complete_module_name)
        return path, name, module_name, coded_module_name, complete_module_name

    def do_after_cython(self):
        for filename in self.pyx_files:
            path, name, module_name, coded_module_name, complete_module_name = self.transform_module_name(filename)
            to_replace = '__Pyx_PyMODINIT_FUNC PyInit_%s' % (module_name, )
            replace_with = '__Pyx_PyMODINIT_FUNC PyInit_%s' % (coded_module_name, )
            with open(filename.replace('.pyx', '.c'), 'r') as f_in:
                data = f_in.read()
                data = data.replace(to_replace, replace_with)
            with open(filename.replace('.pyx', '.c'), 'w') as f_out:
                f_out.write(data)

    def generate_bootstrap(self) -> str:

        cdef_section = []
        for filename in self.pyx_files:
            path, name, module_name, coded_module_name, complete_module_name = self.transform_module_name(filename)

            if os.path.exists(filename.replace('.pyx', '.c')):
                os.unlink(filename.replace('.pyx', '.c'))

            if path:
                h_path_name = filename.replace('.pyx', '.h').replace('\\', '\\\\')
            else:
                h_path_name = name.replace('.pyx', '.h')

            cdef_section.append(CdefSection(h_path_name, module_name, coded_module_name))

            self.modules.append((complete_module_name, module_name, coded_module_name))

        get_definition = []
        for mod_name, init_fun_name, coded_module_name in self.modules:
            get_definition.append(GetDefinitionSection(mod_name, init_fun_name, coded_module_name))

        return render_mako('bootstrap.mako', cdef_sections=cdef_section,
                                             get_definition_sections=get_definition,
                                             module_set=repr(set(x[0] for x in self.modules)))

    def write_bootstrap_file(self):
        with open(os.path.join(self.bootstrap_directory, '__bootstrap__.pyx'), 'w') as f_out:
            f_out.write(self.generate_bootstrap())

    def alter_init(self):
        if os.path.exists(os.path.join(self.bootstrap_directory, '__init__.py')):
            with open(os.path.join(self.bootstrap_directory, '__init__.py'), 'r') as f_in:
                data = f_in.read()
        else:
            data = ''

        if 'bootstrap_cython_submodules' not in data:
            data = render_mako('initpy.mako', module_name=self.extension_name) + data

        with open(os.path.join(self.bootstrap_directory, '__init__.py'), 'w') as f_out:
            f_out.write(data)

    def generate(self):
        self.write_bootstrap_file()
        self.generate_header_files()
        self.alter_init()

    def for_cythonize(self, *args, **kwargs):
        for_cythonize = [*self.files, os.path.join(self.bootstrap_directory, '__bootstrap__.pyx')]
        logger.warning('For cythonize: %s', for_cythonize)
        logger.warning(self.module_name_to_loader_function)
        return Extension(self.extension_name+".__bootstrap__",
                         for_cythonize,
                         *args,
                         **kwargs)


