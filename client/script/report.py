#!/usr/bin/env python
import os
import urllib2
import json
import sys

if len(sys.argv) < 2:
    sys.exit(0)

payload = {
    "status": sys.argv[1]
}

req = urllib2.Request(os.environ["SERVER_URL"] + "/api/workunit/" + os.environ["WORKUNIT_ID"], json.dumps(payload))
req.get_method = lambda:'PUT'
req.add_header("Content-Type", "application/json")

try:
    resp = urllib2.urlopen(req).read()
except:
    pass