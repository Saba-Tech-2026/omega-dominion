# ============================================================
# 👑 OMEGA DOMINION V9.1 — SAAS PRODUCTION (ONE FILE)
# Stable Version — Save Safe — No Reload Loop
# Leader: Ahmed
# ============================================================

import time
import math
import json
import os
import hashlib
from flask import Flask, jsonify, request
from flask_cors import CORS

# ---------------- CONFIG ----------------
PORT = int(os.environ.get("PORT", 10000))
VAULT_FILE = "omega_vault.json"
LEADER = "Ahmed"

DEMO_KEY = "DEMO123"   # مفتاح تجريبي ثابت

SUPPORTED_REGIONS = {
    "MEA": {"currency": "USD", "fee": 0.05},
    "EU": {"currency": "EUR", "fee": 0.04},
    "AMER": {"currency": "USD", "fee": 0.045}
}

# ---------------- APP ----------------
app = Flask(__name__)
CORS(app)

# ---------------- CORE SYSTEM ----------------
class OmegaSystem:
    def __init__(self):
        self.traders = {}
        self.shipments = {}
        self.ais = {}
        self.load()

    # ---------- STORAGE ----------
    def save(self):
        try:
            with open(VAULT_FILE, "w") as f:
                json.dump({
                    "traders": self.traders,
                    "shipments": self.shipments,
                    "ais": self.ais
                }, f)
        except Exception as e:
            print("SAVE ERROR:", e)

    def load(self):
        if os.path.exists(VAULT_FILE):
            try:
                with open(VAULT_FILE, "r") as f:
                    data = json.load(f)
                    self.traders = data.get("traders", {})
                    self.shipments = data.get("shipments", {})
                    self.ais = data.get("ais", {})
            except Exception as e:
                print("LOAD ERROR:", e)

    # ---------- TRADER ----------
    def ensure_demo_trader(self):
        if DEMO_KEY not in self.traders:
            self.traders[DEMO_KEY] = {
                "name": "DEMO_TRADER",
                "profit": 0.0,
                "created": time.time()
            }
            self.save()

    # ---------- AIS ----------
    def ingest(self, mmsi, lat, lon, speed):
        self.ais[mmsi] = {
            "lat": lat,
            "lon": lon,
            "speed": speed,
            "ts": time.time()
        }

    # ---------- RADAR ----------
    def radar(self, sid, api_key):
        trader = self.traders.get(api_key)
        if not trader:
            return {"error": "INVALID_API_KEY"}

        shipment = self.shipments.get(sid)
        if not shipment:
            return {"error": "SHIPMENT_NOT_FOUND"}

        pos = self.ais.get(shipment["mmsi"])
        if not pos:
            return {"status": "WAITING_FOR_AIS"}

        region = SUPPORTED_REGIONS[shipment["region"]]
        fee = shipment["value"] * region["fee"]
        trader["profit"] += fee

        self.save()

        dist = self.haversine(
            pos["lat"], pos["lon"],
            shipment["dest_lat"], shipment["dest_lon"]
        )

        eta = round(dist / max(pos["speed"], 1), 2)

        return {
            "system": {
                "leader": LEADER,
                "trader": trader["name"],
                "profit_total": round(trader["profit"], 2)
            },
            "ship": {
                "position": [pos["lat"], pos["lon"]],
                "destination": [shipment["dest_lat"], shipment["dest_lon"]],
                "eta_hours": eta
            },
            "finance": {
                "trip_fee": round(fee, 2),
                "currency": region["currency"]
            }
        }

    # ---------- MATH ----------
    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2
            + math.cos(math.radians(lat1))
            * math.cos(math.radians(lat2))
            * math.sin(dlon / 2) ** 2
        )
        return 2 * R * math.asin(math.sqrt(a))


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

# بيانات AIS تجريبية (ثابتة – لا تسبب إعادة تشغيل)
omega.ais["403751000"] = {
    "lat": 15.0,
    "lon": 48.0,
    "speed": 18.5,
    "ts": time.time()
}

# ---------------- ROUTES ----------------
@app.route("/")
def home():
    return jsonify({
        "status": "OMEGA DOMINION ONLINE",
        "demo_key": DEMO_KEY
    })

@app.route("/api/radar/<sid>")
def radar_api(sid):
    key = request.args.get("key")
    return jsonify(omega.radar(sid, key))

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)