import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

from gemini_helper import explain_url

app = Flask(__name__)
CORS(app)

# Load ML model
try:
    model = joblib.load("ml/phishing_model.pkl")
    print("✅ ML Model Loaded Successfully")
except Exception as e:
    print("❌ Model Load Error:", e)
    model = None


def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS scans (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        url TEXT,
        risk INTEGER,
        result TEXT,
        explanation TEXT,
        created_at TEXT
    )
    """)

    conn.commit()
    conn.close()


# Extract features for ML model
def extract_features(url):
    length = len(url)
    dots = url.count(".")
    has_https = 1 if url.startswith("https") else 0

    return [[length, dots, has_https]]


@app.route("/")
def home():
    return "CyberShield AI Backend Running"


@app.route("/analyze", methods=["POST"])
def analyze():

    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON data received"}), 400

        url = data.get("url", "").strip()

        if not url:
            return jsonify({"error": "URL is required"}), 400

        print("Received URL:", url)

        # Feature Extraction
        features = extract_features(url)
        print("Features:", features)

        # Prediction
        if model:
            prediction = model.predict(features)[0]
        else:
            prediction = 0

        print("Prediction:", prediction)

        risk = 0

        # ML Risk
        if prediction == 1:
            risk += 50

        # Rule-Based Detection
        suspicious_keywords = [
            "login",
            "verify",
            "update",
            "secure",
            "account",
            "signin",
            "confirm",
            "bank",
            "payment",
            "wallet",
            "password"
        ]

        if any(word in url.lower() for word in suspicious_keywords):
            risk += 30

        suspicious_domains = [
            ".xyz",
            ".tk",
            ".ml",
            ".ga",
            ".cf"
        ]

        if any(domain in url.lower() for domain in suspicious_domains):
            risk += 20

        if not url.startswith("https://"):
            risk += 10

        # Final Classification
        if risk >= 70:
            result = "Phishing"
        elif risk >= 40:
            result = "Suspicious"
        else:
            result = "Safe"

        # Gemini Explanation
        explanation = explain_url(url, result)

        # Save to database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO scans(url,risk,result,explanation,created_at)
        VALUES(?,?,?,?,?)
        """,
        (
            url,
            risk,
            result,
            explanation,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        conn.close()

        return jsonify({
            "url": url,
            "risk": risk,
            "result": result,
            "explanation": explanation
        })

    except Exception as e:
        print("❌ ANALYZE ERROR:", str(e))
        return jsonify({"error": str(e)}), 500


@app.route("/history")
def history():

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT url,risk,result,explanation,created_at
    FROM scans
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    history = []

    for row in rows:
        history.append({
            "url": row[0],
            "risk": row[1],
            "result": row[2],
            "explanation": row[3],
            "date": row[4]
        })

    return jsonify(history)


# Create database when app starts
init_db()

if __name__ == "__main__":
    app.run(debug=True)