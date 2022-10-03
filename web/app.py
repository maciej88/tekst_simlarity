from flask import Flask, jsonyfy, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt
import spacy

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongo://db:27017")
db = client.SimlarityDB
users = db["Users"]

def user_exist(username):
    if users.find({"Username": username}).count() == 0:
        return False
    else:
        return True

def verify_pw(username, password):
    if not user_exist(username):
        return False
    hashed_pw = users.find({
        "Username": username
    })[0]["Password"]

    if bcrypt.hashpw(password.encode('utf8'), hashed_pw) == hashed_pw:
        return True
    else:
        return False

def count_tokens(username):
    tokens = users.find({
        "Username": username
    })[0]["Tokens"]
    return tokens
class Register(Resource):
    def post(self):
        postedData = request.get_json()

        username = postedData["username"]
        password = postedData["password"]

        if user_exist(username):
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

        if user_exist(username):
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

        nlp = spacy.load("en_core_web_sm")

        text1 = nlp(text1)
        text2 = nlp(text2)

        ratio = text1.similarity(text2)

        retJson = {
            "status": 200,
            "similarity": ratio,
            "msg": "Simlarity score calculated"
        }

        users.update({"Username": username}, {"$set":{"Tokens": num_tokens - 1}})

        return jsonyfy(retJson)