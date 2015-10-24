from flask import Blueprint, g, make_response, abort, request
from core.permission import auth
from bson.json_util import dumps
from bson.objectid import ObjectId
from md5 import md5
import config
import json
import jwt

application = Blueprint("application", __name__)

@application.route('/project/<codename>/app', methods=['GET'])
def get_apps(codename):
    project_data = g.db.project.find_one({"codename": codename})
    if project_data is None:
        abort(404)

    app_list = list(g.db.application.find({"project_id": project_data["_id"]}))

    resp = make_response(dumps(app_list), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

@application.route('/project/<codename>/app', methods=['POST'])
def create_app(codename):
    project_data = g.db.project.find_one({"codename": codename})
    if project_data is None:
        abort(404)

    req_body = json.loads(request.data)

    new_app = {
        "project_id": project_data["_id"],
        "name": req_body["name"],
        "summary": req_body["summary"],
        "platform": req_body["platform"],
        "dockerfile_url": req_body["dockerfile_url"]
    }
    app_id = g.db.application.insert(new_app)

    resp_body = {
        "app_id": str(app_id)
    }

    resp = make_response(json.dumps(resp_body), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

@application.route('/app/<app_id>', methods=['PUT'])
def update_app(app_id):
    req_body = json.loads(request.data)
    set_body = {}

    if check_app_exists(app_id) is False:
        abort(404)

    if "name" in req_body:
        set_body["name"] = req_body["name"]
    if "summary" in req_body:
        set_body["summary"] = req_body["summary"]
    if "platform" in req_body:
        set_body["platform"] = req_body["platform"]
    if "dockerfile_url" in req_body:
        set_body["dockerfile_url"] = req_body["dockerfile_url"]

    g.db.application.update({"_id": ObjectId(app_id)}, {"$set": set_body})

    return '', 200

@application.route('/app/<app_id>', methods=['DELETE'])
def delete_app(app_id):
    if check_app_exists(app_id) is False:
        abort(404)

    g.db.application.remove({"_id": ObjectId(app_id)})
    g.db.input.remove({"application_id": ObjectId(app_id)})

    return '', 200

def check_app_exists(app_id):
    return g.db.application.find({"_id": ObjectId(app_id)}).count() > 0