from flask import Flask, request, jsonify

app = Flask(__name__)

DEMO_KEY = "DEMO123"


def check_api_key():
    key = request.headers.get("X-API-KEY") or request.args.get("key")
    return key == DEMO_KEY


@app.route("/")
def home():
    return jsonify({"status": "OK"})


@app.route("/secure")
def secure():
    if not check_api_key():
        return jsonify({"error": "Unauthorized"}), 401
    return jsonify({"message": "Access granted 🔐"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)