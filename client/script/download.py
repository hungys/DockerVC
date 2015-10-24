#!/usr/bin/env python
import os
import urllib2
import sys

input_path = "/input"
if len(sys.argv) > 1:
    input_path = sys.argv[1]

inputfile = urllib2.urlopen(os.environ["INPUT_URL"])
f = open(input_path, "wb")
f.write(inputfile.read())
f.close()