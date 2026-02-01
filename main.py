# ============================================================
# 👑 OMEGA DOMINION V9.1 – SAAS PRODUCT (ONE FILE)
# Stable – API KEY Protected – Render Ready
# Leader: Ahmed
# ============================================================

import os
import json
import math
from flask import Flask, jsonify, request
from flask_cors import CORS

# ---------------- CONFIG ----------------
PORT = int(os.environ.get("PORT", 10000))
VAULT_FILE = "omega_vault.json"
LEADER = "Ahmed"

# 🔐 API KEY (تجريبي الآن)
DEMO_KEY = "DEMO123"

# ---------------- APP ----------------
app = Flask(__name__)
CORS(app)

# ---------------- SECURITY ----------------
def check_api_key():
    key = request.headers.get("X-API-KEY")
    if key != DEMO_KEY:
        return False
    return True

# ---------------- CORE SYSTEM ----------------
class OmegaSystem:
    def __init__(self):
        self.shipments = {}
        self.ais = {}
        self.load()

    def load(self):
        if os.path.exists(VAULT_FILE):
            with open(VAULT_FILE, "r") as f:
                data = json.load(f)
                self.shipments = data.get("shipments", {})
                self.ais = data.get("ais", {})
        else:
            self.save()

    def save(self):
        with open(VAULT_FILE, "w") as f:
            json.dump({
                "shipments": self.shipments,
                "ais": self.ais
            }, f, indent=2)

    def ensure_demo_trader(self):
        if "DEMO_TRADER" not in self.shipments:
            self.shipments["DEMO_TRADER"] = {
                "value": 100000,
                "region": "MEA"
            }
            self.save()

# ---------------- INIT ----------------
omega = OmegaSystem()
omega.ensure_demo_trader()

# شحنة تجريبية (مرة واحدة فقط)
if "ALPHA_DOMINION" not in omega.shipments:
    omega.shipments["ALPHA_DOMINION"] = {
        "mmsi": "403751000",
        "dest_lat": 12.7,
        "dest_lon": 45.0,
        "value": 500000,
        "region": "MEA"
    }
    omega.save()

# AIS تجريبي
omega.ais["403751000"] = {
    "lat": 15.0,
    "lon": 42.0
}
omega.save()

# ---------------- ROUTES ----------------
@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "status": "OMEGA DOMINION ONLINE",
        "leader": LEADER
    })

@app.route("/secure", methods=["GET"])
def secure():
    if not check_api_key():
        return jsonify({"error": "INVALID OR MISSING API KEY"}), 401

    return jsonify({
        "status": "ACCESS GRANTED",
        "shipments": omega.shipments
    })

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)