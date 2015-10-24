from flask import Blueprint, g, make_response, abort, request
from core.permission import auth
from bson.objectid import ObjectId
from md5 import md5
import config
import json
import jwt

user = Blueprint("user", __name__)

@user.route('/user', methods=['POST'])
def register_user():
    req_body = json.loads(request.data)
    password_hashed = md5(req_body["password"]).hexdigest()

    if check_user_registered(req_body["email"]):
        resp = make_response(json.dumps({"msg": "Email used"}), 400)
        resp.headers["Content-Type"] = "application/json"
        return resp

    new_user = {
        "email": req_body["email"],
        "password": password_hashed,
        "accesstoken": ""
    }
    user_id = g.db.user.insert(new_user)

    token = generate_token(str(user_id))

    resp_body = {
        "accesstoken": token
    }

    resp = make_response(json.dumps(resp_body), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

@user.route('/user/authentication', methods=['POST'])
def request_token():
    req_body = json.loads(request.data)
    password_hashed = md5(req_body["password"]).hexdigest()

    user_data = g.db.user.find_one({"email": req_body["email"], "password": password_hashed})
    if user_data is None:
        abort(403)

    token = generate_token(str(user_data["_id"]))

    resp_body = {
        "accesstoken": token
    }

    resp = make_response(json.dumps(resp_body), 200)
    resp.headers["Content-Type"] = "application/json"
    return resp

def check_user_registered(email):
    return g.db.user.find({"email": email}).count() > 0

def generate_token(user_id):
    token = jwt.encode({"user_id": user_id}, config.SERVER_SECRET, algorithm="HS256")
    g.db.user.update({"_id": ObjectId(user_id)}, {"$set": {"accesstoken": token}})
    return token