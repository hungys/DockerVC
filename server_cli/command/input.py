import json
import urllib2
import base64
import config

def input_list(args):
    try:
        resp = json.loads(urllib2.urlopen(config.server_url + "/api/app/" + args[0] + "/input").read())
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

def input_create(args):
    input_url = raw_input("Input URL: ")

    if not input_url.startswith("http"):
        try:
            with open(input_url, "rb") as inputfile:
                input_url = base64.b64encode(inputfile.read())
        except:
            print "[Error] fail to load local input file"
            return

    payload = {
        "input_url": input_url
    }

    req = urllib2.Request(config.server_url + "/api/app/" + args[0] + "/input", json.dumps(payload))
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

def input_update(args):
    print "[Hint] enter if no change"
    input_url = raw_input("Input URL: ")

    payload = {
        "input_url": input_url
    }

    if not input_url.startswith("http"):
        try:
            with open(input_url, "rb") as inputfile:
                payload["input_url"] = base64.b64encode(inputfile.read())
        except:
            print "[Error] fail to load local input file"
            return

    req = urllib2.Request(config.server_url + "/api/input/" + args[0], json.dumps(payload))
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

def input_delete(args):
    req = urllib2.Request(config.server_url + "/api/input/" + args[0])
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

def execute(args):
    if args[1] == "list":
        input_list(args[2:])
    elif args[1] == "create":
        input_create(args[2:])
    elif args[1] == "update":
        input_update(args[2:])
    elif args[1] == "delete":
        input_delete(args[2:])

def display_help():
    print "- input"
    print "    - input list <app_id>: show all inputs of the project"
    print "    - input create <app_id>: create a new input"
    print "    - input update <input_id>: update a input"
    print "    - input delete <input_id>: delete a input"