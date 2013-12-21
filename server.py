#!/usr/bin/env python

"""
    Pinr
    ~~~~
    A Flask-based web app where you can post and share images, text and links.
"""

# imports
from flask import Flask, render_template, request, abort, jsonify
import pymongo, bson, json
from datetime import datetime
from urllib2 import urlopen

#### App
app = Flask(__name__)


#### URLs for serving web pages
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/items')
def get_items():
	c = pymongo.Connection()
	try:
		data = []
		for item in list(c.pinr.items.find()):
			item['date'] = item['date'].isoformat()
			item['_id'] = str(item['_id'])
			data.append(item)
		return jsonify({'items': data})
	finally:
		c.disconnect()

@app.route('/items', methods=['POST'])
def add_item():
	c = pymongo.Connection()
	try:
		item = request.json
		item['date'] = datetime.now()
		item['ip_addr'] = request.remote_addr
		item_id = c.pinr.items.insert(item)

		# Make ID and Date JSON Serializable
		item['_id'] = str(item_id)
		item['date'] = item['date'].isoformat()
		return jsonify({'items': item})
	finally:
		c.disconnect()
###E Validators


#### Server initialization
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
