##### RESTful API using Flask
import os
import sys
sys.path.insert(0, os.path.realpath(__file__).replace('runDatabaseService.py', '') + 'src')
from database_management import app

app.run(host='0.0.0.0', port=8080, debug=True)