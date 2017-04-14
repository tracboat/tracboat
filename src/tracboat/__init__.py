# -*- coding: utf-8 -*-

import re
from collections import namedtuple

###################################################
__author__ = 'Federico Ficarelli'
__copyright__ = 'Copyright (c) 2015 Federico Ficarelli'
__license__ = 'GNU General Public License v3 (GPLv3)'
__version__ = '0.2.0a0'

VERSION = __version__
# bumpversion can only search for {current_version}
# so we have to parse the version here.
# pylint: disable=invalid-name
version_info_t = namedtuple('version_info_t', 'major minor patch release')
# pylint: disable=invalid-name
_m = re.match(r'(\d+)\.(\d+).(\d+)(-(\w+))?', __version__).groups()
VERSION_INFO = version_info_t(
    major=int(_m[0]), minor=int(_m[1]), patch=int(_m[2]), release=_m[4])
del _m
###################################################
