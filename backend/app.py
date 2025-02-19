from flask import Flask, request, jsonify
from model import detect_toxicity  
import firebase_admin
from firebase_admin import credentials, firestore
from twilio.rest import Client
import os
from dotenv import load_dotenv
from flask_cors import CORS


load_dotenv()


app = Flask(__name__)
CORS(app)


# Firebase starting
cred = credentials.Certificate("firebase_config.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Twilio Credentials 
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER", "+15802049375")
ADMIN_PHONE_NUMBER = os.getenv("ADMIN_PHONE_NUMBER", "+918130035736")
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

@app.route("/", methods=["GET"])
def home():
    return "Flask API is running!"

@app.route("/analyze", methods=["POST"])
def analyze_text():
    data = request.json
    text = data.get("text", "")

    if not text:
        return jsonify({"error": "No text provided"}), 400

    #  Detoxify's toxicity detecttion 
    toxicity_score = detect_toxicity(text)

    # saving flagged messages in Firebase if highly toxic
    if toxicity_score >= 0.8:  
        db.collection("toxic_messages").add({
            "text": text,
            "score": float(toxicity_score)
        })

        # send SMS alert
        client.messages.create(
            body=f"🚨 Toxic Speech Alert: {text}",
            from_=TWILIO_PHONE_NUMBER,
            to=ADMIN_PHONE_NUMBER
        )

    return jsonify({"toxicity_score": float(toxicity_score)})

@app.route("/alert", methods=["POST"])
def send_alert():
    data = request.json
    phone_number = data.get("phone_number", ADMIN_PHONE_NUMBER)

    client.messages.create(
        body="🚨 Toxic Content Detected!",
        from_=TWILIO_PHONE_NUMBER,
        to=ADMIN_PHONE_NUMBER
    )

    return jsonify({"message": "Alert Sent"}), 200

if __name__ == "__main__":
    app.run(debug=True)
