from flask import Flask, request, jsonify
from send_email import send_email_alert  
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv
from flask_cors import CORS

load_dotenv()

app = Flask(__name__)
CORS(app)

# ✅ Firebase Initialization with Exception Handling
try:
    cred = credentials.Certificate("firebase_config.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()
except Exception as e:
    print(f"🔥 Firebase Initialization Error: {e}")
    db = None  # Prevent crashes

# ✅ Import Toxicity Model with Fallback
try:
    from model import detect_toxicity
except ImportError as e:
    print(f"⚠️ Model import failed: {e}")
    detect_toxicity = lambda text: 0.0  # Return 0.0 (non-toxic) if model fails

# ✅ Load Email Configuration
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

if not EMAIL_ADDRESS or not EMAIL_PASSWORD or not ADMIN_EMAIL:
    print("⚠️ Missing email environment variables. Check your .env file.")

@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!"

@app.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    # ✅ Run toxicity analysis
    toxicity_score = detect_toxicity(text)

    # ✅ Store highly toxic messages in Firebase
    if toxicity_score >= 0.8 and db:  
        db.collection("toxic_messages").add({
            "text": text,
            "score": float(toxicity_score)
        })

        # ✅ Send email alert
        send_email_alert(text)

    return jsonify({"toxicity_score": float(toxicity_score)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.getenv("DEBUG", "False").lower() == "true")
