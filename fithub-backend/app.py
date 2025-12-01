from flask import Flask, jsonify, request
from pymongo import MongoClient
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# MongoDB connection
MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb+srv://meknofu:@cluster0.gaero04.mongodb.net/?appName=Cluster0"
)
client = MongoClient(MONGO_URI)
db = client["fithub"]
reviews_collection = db["reviews"]


@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    """Get all reviews (newest first)."""
    try:
        reviews = list(
            reviews_collection.find({}, {"_id": 0}).sort("timestamp", -1)
        )
        return jsonify(reviews), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/reviews", methods=["POST"])
def create_review():
    """Create a new review."""
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
        # Do not expose Mongo _id
        review.pop("_id", None)

        return jsonify(review), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/", methods=["GET"])
def health():
    """Simple health endpoint."""
    return jsonify({"status": "ok"}), 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
