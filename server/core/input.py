from flask import Blueprint, g, make_response, abort, request
from core.permission import auth
from helper import azure_storage
from bson.json_util import dumps
from bson.objectid import ObjectId
from md5 import md5
import config
import json
import base64
import jwt

input = Blueprint("input", __name__)

@input.route('/app/<app_id>/input', methods=['GET'])
def get_inputs(app_id):
    app_data = g.db.application.find_one({"_id": ObjectId(app_id)})
    if app_data is None:
        abort(404)

    input_list = list(g.db.input.find({"application_id": app_data["_id"]}))

    resp = make_response(dumps(input_list), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

@input.route('/app/<app_id>/input', methods=['POST'])
def create_input(app_id):
    app_data = g.db.application.find_one({"_id": ObjectId(app_id)})
    if app_data is None:
        abort(404)

    req_body = json.loads(request.data)

    new_input = {
        "application_id": app_data["_id"],
        "status": "created",
        "input_url": req_body["input_url"],
        "output_url": ""
    }

    if not new_input["input_url"].startswith("http"):
        new_input["input_url"] = azure_storage.upload_from_text("inputs", base64.decodestring(new_input["input_url"]))

    input_id = g.db.input.insert(new_input)

    resp_body = {
        "input_id": str(input_id)
    }

    resp = make_response(json.dumps(resp_body), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

@input.route('/input/<input_id>', methods=['PUT'])
def update_input(input_id):
    req_body = json.loads(request.data)
    set_body = {}

    if check_input_exists(input_id) is False:
        abort(404)

    if "status" in req_body:
        set_body["status"] = req_body["status"]
    if "input_url" in req_body:
        set_body["input_url"] = req_body["input_url"]
        if not set_body["input_url"].startswith("http"):
            set_body["input_url"] = azure_storage.upload_from_text("inputs", base64.decodestring(set_body["input_url"]))
    if "output_url" in req_body:
        set_body["output_url"] = req_body["output_url"]

    g.db.input.update({"_id": ObjectId(input_id)}, {"$set": set_body})

    return '', 200

@input.route('/input/<input_id>', methods=['DELETE'])
def delete_input(input_id):
    if check_input_exists(input_id) is False:
        abort(404)

    g.db.input.remove({"_id": ObjectId(input_id)})

    return '', 200

def check_input_exists(input_id):
    return g.db.input.find({"_id": ObjectId(input_id)}).count() > 0