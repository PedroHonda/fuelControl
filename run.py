##### RESTful API using Flask
import sys
sys.path.insert(0, './src')
from src import app


app.run(host='127.0.0.1', port=8080, debug=True)