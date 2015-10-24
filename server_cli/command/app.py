import json
import urllib2

def app_list(base_url, args):
    try:
        resp = json.loads(urllib2.urlopen(base_url + "/api/project/" + args[0] + "/app").read())
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

def app_create(base_url, args):
    name = raw_input("App name: ")
    platform = raw_input("App platform (windows/linux): ")
    summary = raw_input("App summary: ")
    dockerfile_url = raw_input("Dockerfile URL: ")

    payload = {
        "name": name,
        "platform": name,
        "summary": summary,
        "dockerfile_url": dockerfile_url
    }

    req = urllib2.Request(base_url + "/api/project/" + args[0] + "/app", json.dumps(payload))
    req.add_header("Content-Type", "application/json")

    try:
        resp = json.loads(urllib2.urlopen(req).read())
        print "App created!"
    except urllib2.HTTPError as e:
        if e.code == 404:
            print "[Error] project not found"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "[Error] unexpected error"

def app_update(base_url, args):
    print "[Hint] enter if no change"
    name = raw_input("App name: ")
    platform = raw_input("App platform (windows/linux): ")
    summary = raw_input("App summary: ")
    dockerfile_url = raw_input("Dockerfile URL: ")

    payload = {}
    if len(name) > 0:
        payload["name"] = name
    if len(platform) > 0:
        payload["platform"] = platform
    if len(summary) > 0:
        payload["summary"] = summary
    if len(dockerfile_url) > 0:
        payload["dockerfile_url"] = dockerfile_url

    req = urllib2.Request(base_url + "/api/app/" + args[0], json.dumps(payload))
    req.get_method = lambda:'PUT'
    req.add_header("Content-Type", "application/json")

    try:
        resp = urllib2.urlopen(req).read()
        print "App updated!"
    except urllib2.HTTPError as e:
        if e.code == 404:
            print "[Error] app not found"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "[Error] unexpected error"

def app_delete(base_url, args):
    req = urllib2.Request(base_url + "/api/app/" + args[0])
    req.get_method = lambda:'DELETE'
    req.add_header("Content-Type", "application/json")

    try:
        resp = urllib2.urlopen(req).read()
        print "App deleted!"
    except urllib2.HTTPError as e:
        if e.code == 404:
            print "[Error] app not found"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "[Error] unexpected error"

def execute(base_url, args):
    if args[1] == "list":
        app_list(base_url, args[2:])
    elif args[1] == "create":
        app_create(base_url, args[2:])
    elif args[1] == "update":
        app_update(base_url, args[2:])
    elif args[1] == "delete":
        app_delete(base_url, args[2:])