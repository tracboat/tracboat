#!/usr/bin/python2

import shelve
import sys
from pprint import pprint

filename = sys.argv[1]
db = shelve.open(filename)
pprint(db)
