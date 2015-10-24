from pymongo import MongoClient
from flask import g

MONGO_CONNECTION_STRING = "mongodb://senselab:###Taiwan@localhost"
MONGO_DATABASE_NAME = "dockervc"

def connect_db():
    conn = MongoClient(MONGO_CONNECTION_STRING)
    return conn, conn[MONGO_DATABASE_NAME]
