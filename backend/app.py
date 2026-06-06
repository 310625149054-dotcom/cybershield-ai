from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "CyberShield AI Backend Running"

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.json
    url = data.get("url", "")

    keywords = ["login", "secure", "bank", "verify", "update"]

    risk = 0

    for word in keywords:
        if word in url.lower():
            risk += 20

    result = "Safe"

    if risk >= 40:
        result = "Suspicious"

    return jsonify({
        "url": url,
        "risk": risk,
        "result": result
    })

if __name__ == "__main__":
    app.run(debug=True)