from flask_cors import CORS
from flask import Flask 

app = Flask(__name__)
CORS(app)

from PCGAPI.app.controllers import heartbeat_controller
