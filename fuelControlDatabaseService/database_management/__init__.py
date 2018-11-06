import os
from myDB import myDB
from flask import Flask, request, g
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS

app = Flask(__name__)
api = Api(app)
CORS(app)

fuelControlDB = os.path.realpath(__file__).split('database_management')[0]+'databases/fuelControl.db'

class Home(Resource):
    def get(self):
        db = myDB(fuelControlDB)
        tables = db.getTables()
        db.connection.close()
        return tables, 200

    def post(self):
        args = request.json
        if not isinstance(args, list):
            return "Input is not a list!", 406
        if len(args) > 1:
            return "Array must have only 1 element!", 400
        db = myDB(fuelControlDB)
        tables = db.getTables()
        carName = args[0]
        if carName.lower() not in map(lambda x:x.lower(),tables):
            newCarSQL = "CREATE TABLE " + carName + " (date DATE,mileage INTEGER,pricePerLitre FLOAT,litreTotal FLOAT,payTotal FLOAT,fuelType VARCHAR(20),mileageDiff INTEGER,efficiency FLOAT,pricePerKm FLOAT,comments)"
            db.sqlCommand(newCarSQL)
            db.connection.close()
            return 'Created!', 201
        db.connection.close()
        return tables, 409

class Car(Resource):
    def get(self, carName):
        db = myDB(fuelControlDB)
        tables = db.getTables()
        # make comparison case-insensitive
        if carName.lower() not in map(lambda x:x.lower(),tables):
            return {'Not found' : carName}, 404
        content = db.selectCommand('SELECT rowId,* FROM ' + carName)
        db.connection.close()
        return content, 200

    def post(self, carName):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, required=True, help='Date must be a String')
        parser.add_argument('mileage', type=int, required=True, help='Mileage must be a Integer')
        parser.add_argument('pricePerLitre', type=float, required=True, help='Price per Litre must be a Float')
        parser.add_argument('litreTotal', type=float, required=True, help='Total litre must be a Float')
        parser.add_argument('fuelType', type=str, help='Fuel Type must be a String')
        parser.add_argument('comments', type=str, help='Comments must be a String')
        try:
            args = parser.parse_args()      
        except:
            return {"Bad Input! Follow the example..." : {
                    "date" : "2018-09-20",
                    "mileage" : 10000,
                    "pricePerLitre" : 4.000,
                    "litreTotal" : 20.0,
                    "fuelType" : "Gasolina Comum",
                    "comments" : "insert comment"
                }}, 400
        args['payTotal'] = args['pricePerLitre']*args['litreTotal']
        if not args['fuelType']:
            args['fuelType'] = ''
        if not args['comments']:
            args['comments'] = ''
        db = myDB(fuelControlDB)
        tables = db.getTables()
        # make comparison case-insensitive
        if carName.lower() not in map(lambda x:x.lower(),tables):
            return {'No Found' : carName}, 404
        else:
            contentPast = db.selectCommand('SELECT * FROM ' + carName)
            args['mileageDiff'] = args['mileage'] - contentPast[-1][1]
            if float(args['mileageDiff']):
                if float(args['mileageDiff']) < 0:
                    return {'Failure!' : 'Mileage Diff is negative!', 'Mileage' : args['mileage'], 'Previous Mileage' : contentPast[-1][1]}, 500
                args['efficiency'] = float(args['litreTotal']) / float(args['mileageDiff'])
                args['pricePerKm'] = float(args['payTotal']) / float(args['mileageDiff'])
            else:
                return {'Failure!' : 'Mileage Diff is zero!', 'Mileage' : args['mileage'], 'Previous Mileage' : contentPast[-1][1]}, 500
            db.insertValues(carName, args)
            db.connection.close()
            return {'Success!' : carName}, 200
    
    def delete(self, carName):
        db = myDB(fuelControlDB)
        try:
            db.deleteTable(carName)
            db.connection.close()
            return {'Table dropped' : carName}, 200
        except:
            db.connection.close()
            return {'No table found' : carName}, 404
    
    def put(self, carName):
        parser = reqparse.RequestParser()
        parser.add_argument('date', type=str, help='Date must be a String')
        parser.add_argument('mileage', type=int, help='Mileage must be a Integer')
        parser.add_argument('pricePerLitre', type=float, help='Price per Litre must be a Float')
        parser.add_argument('litreTotal', type=float, help='Total litre must be a Float')
        parser.add_argument('payTotal', type=float, help='Pay Total must be a Float')
        parser.add_argument('fuelType', type=str, help='Fuel Type must be a String')
        parser.add_argument('comments', type=str, help='Comments must be a String')
        parser.add_argument('mileageDiff', type=int, help='MileageDIFF must be a Integer')
        parser.add_argument('efficiency', type=float, help='Efficiency must be a Float')
        parser.add_argument('pricePerKm', type=float, help='Price per Km must be a Float')
        parser.add_argument('rowId', required=True, type=int, help='Row ID must be a Integer')
        args = parser.parse_args()
        rowId = args['rowId']
        del args['rowId']
        # Deleting arguments which were not changed
        args = {key:value for key,value in args.items() if args[key]}
        db = myDB(fuelControlDB)
        #updateValues = request.json
        #rowId = updateValues["rowId"]
        db.updateValueRowId(carName, args, rowId)
        db.connection.close()
        args['rowId'] = rowId
        return args, 200

class CarHelp(Resource):
    def get(self, carName):
        db = myDB(fuelControlDB)
        tables = db.getTables()
        # make comparison case-insensitive
        if carName.lower() not in map(lambda x:x.lower(),tables):
            return {'Not found' : carName}, 404
        content = db.getTablesParameters(carName)
        db.connection.close()
        return content, 200

api.add_resource(Home, '/')
api.add_resource(Car, '/<string:carName>')
api.add_resource(CarHelp, '/<string:carName>/parameters')