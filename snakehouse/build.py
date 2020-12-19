import logging
import typing as tp
from Cython.Build import cythonize
from setuptools import Extension
from .multibuild import Multibuild

MultiBuildType = tp.Union[Multibuild, Exception]

logger = logging.getLogger(__name__)


def build(extensions: tp.List[MultiBuildType], *args, **kwargs):
    returns = []
    multi_builds = []
    for multi_build in extensions:
        if isinstance(multi_build, Extension):
            returns.append(multi_build)
        elif isinstance(multi_build, Multibuild):
            multi_build.generate()
            multi_builds.append(multi_build)
            returns.extend(multi_build.for_cythonize())
        else:
            raise ValueError('Invalid value in list, expected either an instance of Multibuild '
                             'or an Extension')
    values = cythonize(returns, *args, **kwargs)
    for multi_build in multi_builds:
        multi_build.do_after_cython()
        logger.warning(multi_build.module_name_to_loader_function)
    return values
