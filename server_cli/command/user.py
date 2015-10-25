import json
import urllib2
import config

def user_register(args):
    email = raw_input("Email: ")
    password = raw_input("Password: ")

    payload = {
        "email": email,
        "password": password
    }

    req = urllib2.Request(config.server_url + "/api/user", json.dumps(payload))
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

def user_auth(args):
    email = raw_input("Email: ")
    password = raw_input("Password: ")

    payload = {
        "email": email,
        "password": password
    }

    req = urllib2.Request(config.server_url + "/api/user/authentication", json.dumps(payload))
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

def execute(args):
    if args[1] == "register":
        user_register(args[2:])
    elif args[1] == "auth":
        user_auth(args[2:])

def display_help():
    print "- user"
    print "    - user register: register for a new account"
    print "    - user register: authorize your account"