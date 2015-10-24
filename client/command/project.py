import json
import urllib2
import config

def project_list(args):
    try:
        resp = json.loads(urllib2.urlopen(config.server_url + "/api/project").read())
        print "Codename\tName\tSummary"
        print "=" * 50
        for project in resp:
            print project["codename"] + "\t" + \
                project["name"] + "\t" + project["summary"]
    except urllib2.HTTPError as e:
        print "Error: status code = " + str(e.code)
    except:
        print "Error: unexpected error"

def execute(args):
    if args[1] == "list":
        project_list(args[2:])