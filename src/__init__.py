from myDB import myDB
from flask import Flask, request, g
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
api = Api(app)

class Home(Resource):
    def get(self):
        db = myDB('./databases/fuelControl.db')
        tables = db.getTables()
        db.connection.close()
        return tables, 200

class Car(Resource):
    def get(self, carName):
        db = myDB('./databases/fuelControl.db')
        tables = db.getTables()
        # make comparison case-insensitive
        if carName.lower() not in map(lambda x:x.lower(),tables):
            return {'Not found' : carName}, 404
        content = db.selectCommand('SELECT * FROM ' + carName)
        db.connection.close()
        return content, 200

    def post(self, carName):
        parser = reqparse.RequestParser()
        parser.add_argument('date', required=True, help='Date must be a String')
        parser.add_argument('mileage', type=int, required=True, help='Mileage must be a Integer')
        parser.add_argument('pricePerLitre', type=float, required=True, help='Price per Litre must be a Float')
        parser.add_argument('litreTotal', type=float, required=True, help='Total litre must be a Float')
        parser.add_argument('fuelType', type=str, help='Fuel Type must be a String')
        parser.add_argument('comments', type=str, help='Comments must be a String')
        args = parser.parse_args()      
        args['payTotal'] = args['pricePerLitre']*args['litreTotal']
        if not args['fuelType']:
            args['fuelType'] = ''
        if not args['comments']:
            args['comments'] = ''
        db = myDB('./databases/fuelControl.db')
        tables = db.getTables()
        # make comparison case-insensitive
        if carName.lower() not in map(lambda x:x.lower(),tables):
            newCar = {}
            newCar[carName] = []
            newCar[carName].append({'Name' : 'date', 'Type' : 'DATE'})
            newCar[carName].append({'Name' : 'mileage', 'Type' : 'INTEGER'})
            newCar[carName].append({'Name' : 'pricePerLitre', 'Type' : 'FLOAT'})
            newCar[carName].append({'Name' : 'litreTotal', 'Type' : 'FLOAT'})
            newCar[carName].append({'Name' : 'payTotal', 'Type' : 'FLOAT'})
            newCar[carName].append({'Name' : 'fuelType', 'Type' : 'VARCHAR(20)'})
            newCar[carName].append({'Name' : 'mileageDiff', 'Type' : 'INTEGER'})
            newCar[carName].append({'Name' : 'efficiency', 'Type' : 'FLOAT'})
            newCar[carName].append({'Name' : 'pricePerKm', 'Type' : 'FLOAT'})
            newCar[carName].append({'Name' : 'comments', 'Type' : ''})
            db.createTable(newCar)
            args['mileageDiff'] = 0
            args['efficiency'] = 0
            args['pricePerKm'] = 0
            db.insertValues(carName, args)
            db.connection.close()
            return {'Created' : carName}, 201
        else:
            contentPast = db.selectCommand('SELECT * FROM ' + carName)
            args['mileageDiff'] = args['mileage'] - contentPast[-1][1]
            args['efficiency'] = float(args['litreTotal']) / float(args['mileageDiff'])
            args['pricePerKm'] = float(args['payTotal']) / float(args['mileageDiff'])
            db.insertValues(carName, args)
            db.connection.close()
            return {'Success!' : carName}, 200
    
    def delete(self, carName):
        db = myDB('./databases/fuelControl.db')
        try:
            db.deleteTable(carName)
            db.connection.close()
            return {'Table dropped' : carName}, 200
        except:
            db.connection.close()
            return {'No table found' : carName}, 404

api.add_resource(Home, '/')
api.add_resource(Car, '/<string:carName>')