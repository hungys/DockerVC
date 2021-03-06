from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from flask import Flask, g, request, make_response, render_template, send_from_directory
from core.database import connect_db
from core.permission import auth
from bson.objectid import ObjectId
import json
import jwt
import config
import os

app = Flask(__name__, static_url_path="")

from core.user import user
app.register_blueprint(user, url_prefix="/api")
from core.project import project
app.register_blueprint(project, url_prefix="/api")
from core.application import application
app.register_blueprint(application, url_prefix="/api")
from core.input import input
app.register_blueprint(input, url_prefix="/api")
from core.workunit import workunit
app.register_blueprint(workunit, url_prefix="/api")

@app.before_request
def before_request():
    g.dbconn, g.db = connect_db()

    g.user_id = None
    auth_header = request.headers.get("Authorization")
    if auth_header is not None and auth_header.startswith("Bearer "):
        token = auth_header.split(" ")[1]
        payload = jwt.decode(token, config.SERVER_SECRET, algorithms=['HS256'])
        g.user = g.db.user.find_one({"_id": ObjectId(payload["user_id"])})
        if g.user is not None:
            g.user_id = payload["user_id"]

@app.after_request
def after_request(response):
    if g.dbconn:
        g.dbconn.close()

    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Credentials", "true")
    response.headers.add("Access-Control-Allow-Headers", "Authorization, Content-Type")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")

    return response

@auth.verify_password
def verify_password(username, password):
    return False if g.user_id is None else True

@auth.error_handler
def auth_error():
    return make_response(json.dumps({"msg": "Unauthorized access"}), 403)

@app.errorhandler(403)
def unauthorized(error):
    return make_response(json.dumps({"msg": "Unauthorized access"}), 403)

@app.errorhandler(404)
def not_found(error):
    return make_response(json.dumps({"msg": "Not found"}), 404)

@app.route('/static/<path:path>')
def send_static_file(path):
    return send_from_directory("static", path)

@app.route('/', methods=['GET'])
def index_page():
    project_list = list(g.db.project.find())
    for project in project_list:
        project["apps"] = list(g.db.application.find({"project_id": project["_id"]}))
        print project["apps"]

    return render_template("index.html", project_list=project_list)

# if __name__ == '__main__':
#     app.run(host='0.0.0.0', debug=True)

if __name__ == '__main__':
    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    print "Flask app starting..."
    IOLoop.instance().start()