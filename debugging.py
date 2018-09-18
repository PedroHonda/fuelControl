import sys
sys.path.insert(0, 'src/')
sys.path.insert(0, 'databases/')
from myDB import myDB

db = myDB('DB.db')
dbJSON = {}
dbJSON['Car'] = []
dbJSON['Car'].append({'Name' : 'date', 'Type' : 'DATE'})
dbJSON['Car'].append({'Name' : 'mileage', 'Type' : 'INTEGER'})

try:
    db.createTable(dbJSON)
except:
    print('Table Car already created. Continuing...')
db.insertValues('Car',('date', 'mileage'),('as', 10234))
print(db.selectCommands('SELECT * FROM Car'))
