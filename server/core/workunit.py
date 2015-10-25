from flask import Blueprint, g, make_response, abort, request
from core.permission import auth
from helper import azure_storage
from bson.json_util import dumps
from bson.objectid import ObjectId
from hashlib import sha256
from md5 import md5
import random
import config
import json
import base64
import jwt

workunit = Blueprint("workunit", __name__)

@workunit.route('/app/<app_id>/workunit', methods=['GET'])
@auth.login_required
def get_workunit(app_id):
    app_data = g.db.application.find_one({"_id": ObjectId(app_id)})
    if app_data is None:
        abort(404)

    # ugly random version
    input_count = g.db.input.find({"status": {"$ne": "finished"}}).count()
    if input_count == 0:
        resp_body = {
            "workunit_id": "-1",
            "dockerfile_url": "",
            "input_id": "",
            "input_url": "",
        }
    else:
        rnd_skip = random.randint(0, input_count - 1)
        input_data = g.db.input.find({"status": {"$ne": "finished"}}).limit(-1).skip(rnd_skip).next()

        new_workunit = {
            "input_id": str(input_data["_id"]),
            "user_id": g.user_id,
            "status": "assigned",
            "output_url": "",
            "output_checksum": ""
        }

        workunit_id = g.db.workunit.insert(new_workunit)
        if input_data["status"] == "created":
            g.db.input.update({"_id": input_data["_id"]}, {"$set": {"status": "assigned"}})

        resp_body = {
            "workunit_id": str(workunit_id),
            "dockerfile_url": app_data["dockerfile_url"],
            "input_id": str(input_data["_id"]),
            "input_url": input_data["input_url"],
        }

        print "Input %s is assigned to %s" % (str(input_data["_id"]), g.user["email"])

    resp = make_response(json.dumps(resp_body), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

@workunit.route('/workunit/<workunit_id>', methods=['PUT'])
def update_workunit(workunit_id):
    req_body = json.loads(request.data)
    set_body = {}

    if check_workunit_exists(workunit_id) is False:
        abort(404)

    if "status" in req_body:
        set_body["status"] = req_body["status"]
        print "Workunit %s is %s" % (workunit_id, req_body["status"])
    if "output_url" in req_body:
        set_body["output_url"] = req_body["output_url"]
        if not set_body["output_url"].startswith("http"):
            decoded_output = base64.decodestring(set_body["output_url"])
            set_body["output_url"] = azure_storage.upload_from_text("outputs", decoded_output)
            set_body["output_checksum"] = sha256(decoded_output).hexdigest()
            workunit_data = g.db.workunit.find_one({"_id": ObjectId(workunit_id)})
            payload = {
                "workunit_id": workunit_id,
                "input_id": workunit_data["input_id"],
                "output_url": set_body["output_url"],
                "output_checksum": set_body["output_checksum"]
            }
            azure_storage.put_to_queue(config.AZURE_QUEUE_NAME, json.dumps(payload))

    g.db.workunit.update({"_id": ObjectId(workunit_id)}, {"$set": set_body})

    return '', 200

def check_workunit_exists(workunit_id):
    return g.db.workunit.find({"_id": ObjectId(workunit_id)}).count() > 0