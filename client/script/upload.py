#!/usr/bin/env python
import os
import urllib2
import base64
import json
import sys

output_path = "/output"
if len(sys.argv) > 1:
    output_path = sys.argv[1]

output_url = ""

with open(output_path, "rb") as outputfile:
    output_url = base64.b64encode(outputfile.read())

payload = {
    "output_url": output_url,
    "status": "finished"
}

req = urllib2.Request(os.environ["SERVER_URL"] + "/api/workunit/" + os.environ["WORKUNIT_ID"], json.dumps(payload))
req.get_method = lambda:'PUT'
req.add_header("Content-Type", "application/json")

try:
    resp = urllib2.urlopen(req).read()
except:
    pass