#!/usr/bin/python2

import shelve
import sys

filename, revision, commit = sys.argv[1:4]
db = shelve.open(filename)

print "ADD[%s]: %s -> %s" % (filename, revision, commit)
db[revision] = commit
print "added as %s" % db[revision]

db.close()
