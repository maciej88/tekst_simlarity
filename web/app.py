from flask import Flask, jsonyfy, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongo://db:27017")
db = client.SimlarityDB
users = db["Users"]

def UserExist(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True
class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if UserExist(username):
            retJson = {
                "status": 301,
                "msg": "Invalid Username"
            }
            return jsonyfy(retJson)
        hashed_pw = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

        users.insert({
            "Username": username,
            "Password": hashed_pw,
            "Tokens": 6
        })
        retJson = {
            "status": 200,
            "msg": "Signed in!"
        }
        return jsonyfy(retJson)

class Detect(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]
        text1 = postedData["text1"]
        text2 = postedData["text2"]

        if UserExist(username):
            retJson = {
                "status": 301,
                "msg": "invalid user"
            }
            return jsonyfy(retJson)
        correct_pw = verify_pw(username, password)

        if not correct_pw:
            retJson = {
                "status": 302,
                "msg": "invalid password"
            }
            return jsonyfy(retJson)

        num_tokens = count_tokens(username)

        if num_tokens <= 0:
            retJson = {
                "status": 303,
                "msg": "no tokens"
            }
            return jsonyfy(retJson)
