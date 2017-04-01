# -*- coding: utf-8 -*-

import re
from collections import namedtuple

###################################################
__author__ = 'Federico Ficarelli'
__copyright__ = 'Copyright (c) 2015 Federico Ficarelli'
__license__ = 'GNU General Public License v3 (GPLv3)'
__version__ = '0.1.0'

VERSION = __version__
# bumpversion can only search for {current_version}
# so we have to parse the version here.
version_info_t = namedtuple('version_info_t', 'major minor patch')  # pylint: disable=invalid-name
VERSION_INFO = version_info_t(*(int(part) for part in re.match(r'(\d+)\.(\d+).(\d+)', __version__).groups()))
###################################################