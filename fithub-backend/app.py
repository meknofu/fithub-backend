from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from datetime_t import datetime  # or datetime from datetime
import os

app = Flask(__name__)
CORS(app)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["fithub"]
reviews_collection = db["reviews"]

@app.route("/api/reviews", methods=["GET", "POST"])
def reviews():
    if request.method == "GET":
        reviews = list(reviews_collection.find({}, {"_id": 0}).sort("timestamp", -1))
        return jsonify(reviews), 200

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




