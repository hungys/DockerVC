import json
import urllib2
import config

def app_list(args):
    try:
        resp = json.loads(urllib2.urlopen(config.server_url + "/api/project/" + args[0] + "/app").read())
        print "Id\tName\tPlatform\tSummary"
        print "=" * 50
        for app in resp:
            print app["_id"]["$oid"] + "\t" + app["name"] + "\t" +\
                app["platform"] + "\t" + app["summary"]
    except urllib2.HTTPError as e:
        if e.code == 404:
            print "[Error] project not found"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "Error: unexpected error"

def execute(args):
    if args[1] == "list":
        app_list(args[2:])