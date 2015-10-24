import json
import urllib2

def user_register(base_url, args):
    email = raw_input("Email: ")
    password = raw_input("Password: ")

    payload = {
        "email": email,
        "password": password
    }

    req = urllib2.Request(base_url + "/api/user", json.dumps(payload))
    req.add_header("Content-Type", "application/json")

    try:
        resp = json.loads(urllib2.urlopen(req).read())
        print "Account created!"
        print "Access Token: " + resp["accesstoken"]
    except urllib2.HTTPError as e:
        if e.code == 400:
            print "[Error] email used"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "[Error] unexpected error"

def user_auth(base_url, args):
    email = raw_input("Email: ")
    password = raw_input("Password: ")

    payload = {
        "email": email,
        "password": password
    }

    req = urllib2.Request(base_url + "/api/user/authentication", json.dumps(payload))
    req.add_header("Content-Type", "application/json")

    try:
        resp = json.loads(urllib2.urlopen(req).read())
        print "Access granted!"
        print "Access Token: " + resp["accesstoken"]
    except urllib2.HTTPError as e:
        if e.code == 403:
            print "[Error] email or password is incorrect"
        else:
            print "[Error] status code = " + str(e.code)
    except:
        print "[Error] unexpected error"

def execute(base_url, args):
    if args[1] == "register":
        user_register(base_url, args[2:])
    elif args[1] == "auth":
        user_auth(base_url, args[2:])