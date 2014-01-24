#!/usr/bin/env python

"""
    CodeConnect
    ~~~~
    A Flask-based web app where you can discover internships, tech events, and mentors.
"""

# imports
from flask import Flask, render_template, request, abort, jsonify, make_response
import bson, json
from pymongo import MongoClient
from datetime import datetime
from urllib2 import urlopen

''' Global Vars '''
mongodb_url = "mongodb://admin:CodeConnect@troup.mongohq.com:10008/CodeConnect"


#### App
app = Flask(__name__)


#### URLs for serving web pages
@app.route('/')
def index():
	# resp = make_response(render_template('index.html'))
	# resp.headers['X-Frame-Options'] = 'ALLOW'
	# return resp
	return render_template('index.html')

@app.route('/items')
def get_items():
	c = MongoClient(mongodb_url)
	try:
		data = []
		for item in list(c.CodeConnect.items.find()):
			item['date'] = item['date'].isoformat()
			item['_id'] = str(item['_id'])
			data.append(item)
		return jsonify({'items': data})
	finally:
		c.disconnect()

@app.route('/items', methods=['POST'])
def add_item():
	c = MongoClient(mongodb_url)
	try:
		item = request.json
		item['date'] = datetime.now()
		item['ip_addr'] = request.remote_addr
		item_id = c.CodeConnect.items.insert(item)

		# Make ID and Date JSON Serializable
		item['_id'] = str(item_id)
		item['date'] = item['date'].isoformat()
		return jsonify({'items': item})
	finally:
		c.disconnect()

@app.route('/item/<item_id>', methods=["DELETE"])
def delete_item(item_id):
    c = MongoClient(mongodb_url)
    try:
        c.CodeConnect.items.remove({'_id': bson.ObjectId(item_id)})
        return "OK"
    except bson.errors.InvalidId:
        abort(400)
    finally:
        c.disconnect()

#### Validators

#### Server initialization
if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
