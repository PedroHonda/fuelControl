from myDB import myDB
from flask import Flask, request, g
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Home(Resource):
    def get(self):
        db = myDB('./databases/fuelControl.db')
        tables = db.getTables()
        output = 'Cars available:'
        for table in tables:
            output += table + ", "
        output = output[:-2]
        db.connection.close()
        return output, 200

class Car(Resource):
    def get(self, carName):
        db = myDB('./databases/fuelControl.db')

        db.connection.close()
        return {'You are' : 'UNAUTHORIZED'}, 404

    def post(self, carName):
        db = myDB('./databases/fuelControl.db')
        
        db.connection.close()
        return {'Status' : 'Pay me to input '+carName}, 402

api.add_resource(Home, '/')
api.add_resource(Car, '/<string:carName>')