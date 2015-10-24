import json
import urllib2

def input_list(base_url, args):
    try:
        resp = json.loads(urllib2.urlopen(base_url + "/api/app/" + args[0] + "/input").read())
        print "Id\tStatus"
        print "=" * 50
        for app in resp:
            print app["_id"]["$oid"] + "\t" + app["status"]
    except urllib2.HTTPError as e:
        if e.code == 404:
            print "[Error] app not found"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "Error: unexpected error"

def input_create(base_url, args):
    input_url = raw_input("Input URL: ")

    payload = {
        "input_url": input_url
    }

    req = urllib2.Request(base_url + "/api/app/" + args[0] + "/input", json.dumps(payload))
    req.add_header("Content-Type", "application/json")

    try:
        resp = json.loads(urllib2.urlopen(req).read())
        print "Input created!"
    except urllib2.HTTPError as e:
        if e.code == 404:
            print "[Error] app not found"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "[Error] unexpected error"

def input_update(base_url, args):
    print "[Hint] enter if no change"
    input_url = raw_input("Input URL: ")

    payload = {
        "input_url": input_url
    }

    req = urllib2.Request(base_url + "/api/input/" + args[0], json.dumps(payload))
    req.get_method = lambda:'PUT'
    req.add_header("Content-Type", "application/json")

    try:
        resp = urllib2.urlopen(req).read()
        print "Input updated!"
    except urllib2.HTTPError as e:
        if e.code == 404:
            print "[Error] input not found"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "[Error] unexpected error"

def input_delete(base_url, args):
    req = urllib2.Request(base_url + "/api/input/" + args[0])
    req.get_method = lambda:'DELETE'
    req.add_header("Content-Type", "application/json")

    try:
        resp = urllib2.urlopen(req).read()
        print "Input deleted!"
    except urllib2.HTTPError as e:
        if e.code == 404:
            print "[Error] input not found"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "[Error] unexpected error"

def execute(base_url, args):
    if args[1] == "list":
        input_list(base_url, args[2:])
    elif args[1] == "create":
        input_create(base_url, args[2:])
    elif args[1] == "update":
        input_update(base_url, args[2:])
    elif args[1] == "delete":
        input_delete(base_url, args[2:])