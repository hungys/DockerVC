import json
import urllib2

def project_list(base_url, args):
    try:
        resp = json.loads(urllib2.urlopen(base_url + "/api/project").read())
        print "Codename\tName\tSummary"
        print "=" * 50
        for project in resp:
            print project["codename"] + "\t" + \
                project["name"] + "\t" + project["summary"]
    except urllib2.HTTPError as e:
        print "Error: status code = " + str(e.code)
    except:
        print "Error: unexpected error"

def project_create(base_url, args):
    codename = raw_input("Project codename: ")
    name = raw_input("Project name: ")
    summary = raw_input("Project summary: ")

    payload = {
        "codename": codename,
        "name": name,
        "summary": summary
    }

    req = urllib2.Request(base_url + "/api/project", json.dumps(payload))
    req.add_header("Content-Type", "application/json")

    try:
        resp = json.loads(urllib2.urlopen(req).read())
        print "Project created!"
    except urllib2.HTTPError as e:
        if e.code == 400:
            print "[Error] codename used"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "[Error] unexpected error"

def project_update(base_url, args):
    print "[Hint] enter if no change"
    name = raw_input("Project name: ")
    summary = raw_input("Project summary: ")

    payload = {}
    if len(name) > 0:
        payload["name"] = name
    if len(summary) > 0:
        payload["summary"] = summary

    req = urllib2.Request(base_url + "/api/project/" + args[0], json.dumps(payload))
    req.get_method = lambda:'PUT'
    req.add_header("Content-Type", "application/json")

    try:
        resp = urllib2.urlopen(req).read()
        print "Project updated!"
    except urllib2.HTTPError as e:
        if e.code == 404:
            print "[Error] project not found"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "[Error] unexpected error"

def project_delete(base_url, args):
    req = urllib2.Request(base_url + "/api/project/" + args[0])
    req.get_method = lambda:'DELETE'
    req.add_header("Content-Type", "application/json")

    try:
        resp = urllib2.urlopen(req).read()
        print "Project deleted!"
    except urllib2.HTTPError as e:
        if e.code == 404:
            print "[Error] project not found"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "[Error] unexpected error"

def execute(base_url, args):
    if args[1] == "list":
        project_list(base_url, args[2:])
    elif args[1] == "create":
        project_create(base_url, args[2:])
    elif args[1] == "update":
        project_update(base_url, args[2:])
    elif args[1] == "delete":
        project_delete(base_url, args[2:])