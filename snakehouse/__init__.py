import pkg_resources
from .build import build
from .multibuild import Multibuild, find_all
from .faster_builds import monkey_patch_parallel_compilation
from .requirements import read_requirements_txt, find_c, find_pyx_and_c, find_pyx

try:
    __version__ = pkg_resources.require('snakehouse')[0].version
except pkg_resources.DistributionNotFound:
    __version__ = '1.7'
