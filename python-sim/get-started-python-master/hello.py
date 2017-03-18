from flask import Flask, render_template, request, jsonify
import atexit
import cf_deployment_tracker
import os
import json

from psql_wrapper import PSQLConnector
import csv_wrapper
import globalConfig as config

# Emit Bluemix deployment event
cf_deployment_tracker.track()

app = Flask(__name__)

# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8080
port = int(os.getenv('PORT', 8080))
@app.route('/')

def home():
	return render_template('index.html')

psqlConn = PSQLConnector(config.PSQL_URLDict)
psqlConn.setupDB()
psqlConn.close()

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=port, debug=True)

