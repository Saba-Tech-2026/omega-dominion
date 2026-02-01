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

    def save(self):
        with open(VAULT_FILE, "w") as f:
            json.dump({
                "traders": self.traders,
                "shipments": self.shipments,
                "ais": self.ais
            }, f)

    def load(self):
        if os.path.exists(VAULT_FILE):
            with open(VAULT_FILE, "r") as f:
                data = json.load(f)
                self.traders = data.get("traders", {})
                self.shipments = data.get("shipments", {})
                self.ais = data.get("ais", {})

    def create_trader(self, name):
        key = hashlib.sha256(
            (name + str(time.time())).encode()
        ).hexdigest()[:24]

        self.traders[key] = {
            "name": name,
            "profit": 0.0,
            "created": time.time()
        }
        self.save()
        return key

    def ingest(self, mmsi, lat, lon, speed):
        self.ais[mmsi] = {
            "lat": lat,
            "lon": lon,
            "speed": speed,
            "ts": time.time()
        }

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

        eta = round(dist / max(pos["speed"], 1), 1)

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

    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat / 2) ** 2 +
            math.cos(math.radians(lat1)) *
            math.cos(math.radians(lat2)) *
            math.sin(dlon / 2) ** 2
        )
        return 2 * R * math.asin(math.sqrt(a))

# ---------------- INIT ----------------
omega = OmegaSystem()

if not omega.traders:
    DEMO_KEY = omega.create_trader("DEMO_TRADER")
else:
    DEMO_KEY = list(omega.traders.keys())[0]

omega.shipments["ALPHA_DOMINION"] = {
    "mmsi": "403751000",
    "dest_lat": 12.7,
    "dest_lon": 45.0,
    "value": 500000,
    "region": "MEA"
}

omega.ingest("403751000", 15.0, 48.0, 18.5)

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