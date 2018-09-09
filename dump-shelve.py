#!/usr/bin/python2

import shelve
import sys

filename = sys.argv[1]
db = shelve.open(filename)
for k,v in db.iteritems():
    print "'%s' => '%s'" % (k, v)

db.close()
