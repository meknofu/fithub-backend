from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://meknofu:@cluster0.gaero04.mongodb.net/?appName=Cluster0"
)
client = MongoClient(MONGO_URI)
db = client["fithub"]
reviews_collection = db["reviews"]

@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    try:
        reviews = list(
            reviews_collection.find({}, {"_id": 0}).sort("timestamp", -1)
        )
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/reviews", methods=["POST"])
def create_review():
    try:
        data = request.get_json(force=True) or {}
        role = data.get("role")
        text = data.get("text")

        if not role or not text:
            return jsonify({"error": "role and text are required"}), 400

        review = {
            "role": role,
            "text": text,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        reviews_collection.insert_one(review)
        review.pop("_id", None)
        return jsonify(review), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


