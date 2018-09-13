from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Home(Resource):
    def get(self):
        return {'This is the HOME PAGE' : ['Welcome','And be happy!!']}

class Data(Resource):
    def get(self, num):
        return {'This is the currente database' : 'null'}

    def post(self, num):
        return {'This is your number' : num}

api.add_resource(Home, '/')
api.add_resource(Data, '/<int:num>')