from flask import Blueprint, g, make_response, abort, request
from core.permission import auth
from bson.json_util import dumps
from bson.objectid import ObjectId
from md5 import md5
import config
import json
import jwt

project = Blueprint("project", __name__)

@project.route('/project', methods=['GET'])
def get_all_projects():
    project_list = list(g.db.project.find())

    resp = make_response(dumps(project_list), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

@project.route('/project', methods=['POST'])
def create_project():
    req_body = json.loads(request.data)

    if check_project_exists(req_body["codename"]):
        resp = make_response(json.dumps({"msg": "Codename used"}), 400)
        resp.headers["Content-Type"] = "application/json"
        return resp

    new_project = {
        "codename": req_body["codename"],
        "name": req_body["name"],
        "summary": req_body["summary"]
    }
    project_id = g.db.project.insert(new_project)

    resp_body = {
        "project_id": str(project_id)
    }

    resp = make_response(json.dumps(resp_body), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

@project.route('/project/<codename>', methods=['PUT'])
def update_project(codename):
    req_body = json.loads(request.data)
    set_body = {}

    if check_project_exists(codename) is False:
        abort(404)

    if "name" in req_body:
        set_body["name"] = req_body["name"]
    if "summary" in req_body:
        set_body["summary"] = req_body["summary"]

    g.db.project.update({"codename": codename}, {"$set": set_body})

    return '', 200

@project.route('/project/<codename>', methods=['DELETE'])
def delete_project(codename):
    if check_project_exists(codename) is False:
        abort(404)

    project_data = g.db.project.find_one({"codename": codename})

    g.db.project.remove({"codename": codename})
    g.db.project.remove({"project_id": project_data["_id"]}, multi=True)

    return '', 200

def check_project_exists(codename):
    return g.db.project.find({"codename": codename}).count() > 0