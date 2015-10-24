from flask import Blueprint, g, make_response, abort, request
from core.permission import auth
from bson.json_util import dumps
from bson.objectid import ObjectId
from md5 import md5
import config
import json
import jwt

workunit = Blueprint("workunit", __name__)

@workunit.route('/app/<app_id>/workunit', methods=['GET'])
def get_workunit(app_id):
    app_data = g.db.application.find_one({"_id": ObjectId(app_id)})
    if app_data is None:
        abort(404)

    new_workunit = {
        "input_id": "",
        "user_id": "",
        "status": "assigned",
        "output_url": ""
    }
    workunit_id = g.db.workunit.insert(new_workunit)

    resp_body = {
        "workunit_id": str(workunit_id)
    }

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
    if "output_url" in req_body:
        set_body["output_url"] = req_body["output_url"]

    g.db.workunit.update({"_id": ObjectId(workunit_id)}, {"$set": set_body})

    return '', 200

def check_workunit_exists(workunit_id):
    return g.db.workunit.find({"_id": ObjectId(workunit_id)}).count() > 0