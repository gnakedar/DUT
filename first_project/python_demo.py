#!/usr/bin/python2
import sys

with open(sys.argv[1],'r') as f:
	lines=f.readlines()
	print lines;

print "file 2"
print sys.argv[2]
print "\n\n file 1"
print sys.argv[1]
print "\n\n\n\n\n Welcome to python2 \n\n\n\n\n\n"
