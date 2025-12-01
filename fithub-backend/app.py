Python 3.13.7 (tags/v3.13.7:bcee1c3, Aug 14 2025, 14:15:11) [MSC v.1944 64 bit (AMD64)] on win32
Enter "help" below or click "Help" above for more information.
>>> from flask import Flask, jsonify, request
... from pymongo import MongoClient
... from flask_cors import CORS
... from datetime import datetime
... import os
... 
... app = Flask(__name__)
... CORS(app)
... 
... # MongoDB Connection (replace with your connection string)
... MONGO_URI = os.getenv("MONGO_URI", "mongodb+srv://meknofu:<db_password>@cluster0.gaero04.mongodb.net/?appName=Cluster0")
... client = MongoClient(MONGO_URI)
... db = client['fithub']
... reviews_collection = db['reviews']
... 
... @app.route('/api/reviews', methods=['GET'])
... def get_reviews():
...     """Get all reviews"""
...     try:
...         reviews = list(reviews_collection.find({}, {'_id': 0}).sort('timestamp', -1))
...         return jsonify(reviews), 200
...     except 
