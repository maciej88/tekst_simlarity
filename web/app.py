from flask import Flask, jsonyfy, request
from flask_restful import Api, Resource
from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)

client = MongoClient("mongo://db:27017")
db = client.SimlarityDB
users = db["Users"]