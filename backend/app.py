import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
from datetime import datetime

from gemini_helper import explain_url

app = Flask(__name__)
CORS(app)

# Load ML model
model = joblib.load("ml/phishing_model.pkl")


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

    data = request.json
    url = data.get("url", "")

    # ML Prediction
    features = extract_features(url)
    prediction = model.predict(features)[0]

    if prediction == 1:
        risk = 80
        result = "Suspicious"
    else:
        risk = 20
        result = "Safe"

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


if __name__ == "__main__":
    init_db()
    app.run(debug=True)