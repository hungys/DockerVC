import json
import urllib2
import time
import config
import os
import subprocess

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

def app_start(args):
    while True:
        try:
            req = urllib2.Request(config.server_url + "/api/app/" + args[0] + "/workunit")
            req.add_header("Content-Type", "application/json")
            req.add_header("Authorization", "Bearer " + config.accesstoken)
            resp = json.loads(urllib2.urlopen(req).read())
            if resp["workunit_id"] != "-1":
                print "Get a new work!"
                print "Workunit ID: " + resp["workunit_id"]
                print "Input ID: " + resp["input_id"]
                generate_dockerfile(resp["dockerfile_url"], resp["input_url"], resp["workunit_id"])
                start_container()
                time.sleep(3)
            else:
                print "No more workunit"
                break
        except urllib2.HTTPError as e:
            if e.code == 404:
                print "[Error] app not found"
            elif e.code == 403:
                print "[Error] you're not logged in"
            else:
                print "[Error] status code = " + str(e.code)
            break
        except KeyboardInterrupt:
            break
        except:
            print "Error: unexpected error"
            break

def generate_dockerfile(dockerfile_url, input_url, workunit_id):
    dockerfile = urllib2.urlopen(dockerfile_url).read()

    init_script = """RUN apt-get update && apt-get install -y python && rm -rf /var/lib/apt/lists/*

RUN mkdir /dockervc
ENV PATH /dockervc:$PATH
COPY script/download.py /dockervc/download
COPY script/upload.py /dockervc/upload
COPY script/report.py /dockervc/report
RUN chmod +x /dockervc/download
RUN chmod +x /dockervc/upload
RUN chmod +x /dockervc/report

ENV SERVER_URL %s
ENV INPUT_URL %s
ENV WORKUNIT_ID %s
"""

    dockerfile = dockerfile.replace("RUN dockervc_init", init_script % (config.server_url, \
        input_url, workunit_id))

    f = open("Dockerfile", "wb")
    f.write(dockerfile)
    f.close()

    print "Dockerfile generated"

def start_container():
    if os.name == "posix":
        print "Building docker image..."
        os.system("sudo docker build -t dockervc/workunit .")
        print "Starting docker container..."
        os.system("sudo docker run dockervc/workunit")
        print "Workunit fished\n"
    elif os.name == "nt":
        generate_vagrantfile(1, 50, 1024)
        subprocess.call(["provision.bat"], shell=True)
    else:
        print "[Error] unsupported platform"

def generate_vagrantfile(cpu, cap, mem):
    subprocess.call(["COPY", "/Y", "Vagrantfile_template", "Vagrantfile"], shell=True)

    f = open('Vagrantfile', 'a')
    if cpu == 0:
        cpu = 1

    if cap == 0:
        cap = 50

    if mem == 0:
        mem = 1024

    cpustring = "ENV['cpus'] = \"" + str(cpu) + "\"\n"
    capstring = "ENV['cap'] = \"" + str(cap) + "\"\n"
    memstring = "ENV['mem'] = \"" + str(mem) + "\"\n"

    f.write(cpustring)
    f.write(capstring)
    f.write(memstring)

def execute(args):
    if args[1] == "list":
        app_list(args[2:])
    elif args[1] == "start":
        app_start(args[2:])

def display_help():
    print "- app"
    print "    - app list <codename>: show all apps of the project"
    print "    - app start <app_id>: start to run the app"