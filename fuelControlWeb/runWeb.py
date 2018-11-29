##### Web Development using Flask
import os
import sys
sys.path.insert(0, os.path.realpath(__file__).replace('run.py', '') + 'src')
from web_development import app

app.run(host='0.0.0.0', port=8000, debug=True)