import simplejson as json
from flask import request
from datetime import datetime

from PCGAPI.app import app
from PCGAPI.app.handlers.heartbeat_handler import HeartbeatHandler

@app.route("/", methods= ["GET"])
def home():
    return json.dumps({"success": True, "message": "PCG API is Working!"})

@app.route("/heartbeat", methods= ["POST"])
def heartbeat():
	heartbeat_handler = HeartbeatHandler()
	heartbeat_data = json.loads(request.data)
	response = heartbeat_handler.heartbeat_analysis(heartbeat_data)
	return json.dumps({"success": True, "results": response})

