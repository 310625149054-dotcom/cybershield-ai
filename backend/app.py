import joblib
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS

try:
    from gemini_helper import explain_url
except:
    explain_url = None

app = Flask(__name__)
CORS(app)


# ======================
# DATABASE
# ======================
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


# Create DB when app starts
init_db()


# ======================
# LOAD MODEL
# ======================
try:
    model = joblib.load("ml/phishing_model.pkl")
    print("✅ ML Model Loaded Successfully")
except Exception as e:
    print("❌ Model Load Error:", e)
    model = None


# ======================
# FEATURE EXTRACTION
# ======================
def extract_features(url):
    length = len(url)
    dots = url.count(".")
    has_https = 1 if url.startswith("https") else 0

    return [[length, dots, has_https]]


# ======================
# HOME
# ======================
@app.route("/")
def home():
    return "CyberShield AI Backend Running"


# ======================
# ANALYZE URL
# ======================
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        if not data:
            return jsonify({"error": "No JSON received"}), 400

        url = data.get("url", "").strip()

        if not url:
            return jsonify({"error": "URL is required"}), 400

        features = extract_features(url)

        prediction = 0
        if model:
            prediction = model.predict(features)[0]

        risk = 0

        if prediction == 1:
            risk += 50

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

        if risk >= 70:
            result = "Phishing"
        elif risk >= 40:
            result = "Suspicious"
        else:
            result = "Safe"

        # Gemini explanation
        try:
            if explain_url:
                explanation = explain_url(url, result)
            else:
                explanation = f"This URL is classified as {result}."
        except:
            explanation = f"This URL is classified as {result}."

        # Save to database
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO scans
        (url,risk,result,explanation,created_at)
        VALUES (?,?,?,?,?)
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
        return jsonify({"error": str(e)}), 500


# ======================
# HISTORY
# ======================
@app.route("/history")
def history():
    try:
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

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)