# ============================================================
# 👑 OMEGA V8.1 — FULL PRODUCTION SERVER (RENDER SAFE)
# ============================================================

import time, math, json, datetime, hashlib, os
from flask import Flask, jsonify, request
from flask_cors import CORS

# =========================
# ⚖️ GLOBAL CONSTANTS
# =========================
LEADER = "Ahmed"
VAULT_FILE = "omega_vault.json"

BASE_SERVER_COST = 30.0
BASE_LEADER_RATIO = 0.51
FOUNDATION_TARGET = 100_000

# =========================
# 🌍 REGIONS
# =========================
SUPPORTED_REGIONS = {
    "MEA":  {"currency": "USD", "sla": 0.98,  "fee": 0.05,  "danger": [12.0, 43.0]},
    "EU":   {"currency": "EUR", "sla": 0.995, "fee": 0.04,  "danger": [35.0, 14.0]},
    "AMER": {"currency": "USD", "sla": 0.99,  "fee": 0.045, "danger": [25.0, -90.0]}
}

# =========================
# 🚀 FLASK
# =========================
app = Flask(__name__)
CORS(app)

# =========================
# 👑 OMEGA CORE
# =========================
class SovereignOmega:
    def __init__(self):
        self.ais = {}
        self.shipments = {
            "ALPHA_DOMINION": {
                "mmsi": "403751000",
                "dest_lat": 12.7,
                "dest_lon": 45.0,
                "contract_value": 500000,
                "region": "MEA"
            }
        }
        self.wallet = {"Leader_Net": 0.0}
        self.trip_count = 0
        self.load_state()

    # ---------------------
    def ingest(self, data):
        data["ts"] = time.time()
        data["proof"] = hashlib.sha256(
            json.dumps(data, sort_keys=True).encode()
        ).hexdigest()

        mmsi = data["mmsi"]
        self.ais.setdefault(mmsi, []).append(data)
        self.ais[mmsi] = self.ais[mmsi][-200:]

    # ---------------------
    def analyze(self, history, region):
        last = history[-1]
        trust = 100

        if last["speed"] < 6:
            trust -= 30
        if last["speed"] > 45:
            trust -= 20

        trust = max(int(trust * region["sla"]), 40)

        dist_danger = self.haversine(
            last["lat"], last["lon"],
            region["danger"][0], region["danger"][1]
        )

        threat = "HIGH_RISK" if dist_danger < 150 else "SAFE"
        return trust, threat

    # ---------------------
    def radar(self, sid):
        sh = self.shipments.get(sid)
        if not sh:
            return {"status": "NOT_FOUND"}

        history = self.ais.get(sh["mmsi"], [])
        if not history:
            return {"status": "WAITING_FOR_AIS"}

        region = SUPPORTED_REGIONS[sh["region"]]
        last = history[-1]

        trust, threat = self.analyze(history, region)

        foundation = self.wallet["Leader_Net"] < FOUNDATION_TARGET
        ratio = 0.80 if foundation else BASE_LEADER_RATIO
        cost = 5.0 if foundation else BASE_SERVER_COST

        fee = sh["contract_value"] * region["fee"]
        bonus = sh["contract_value"] * 0.015 if trust > 92 else 0
        net = (fee + bonus) - cost

        if net > 0:
            self.wallet["Leader_Net"] += net * ratio
            self.trip_count += 1
            self.save_state()

        dist = self.haversine(
            last["lat"], last["lon"],
            sh["dest_lat"], sh["dest_lon"]
        )

        eta = round(dist / (max(last["speed"], 1) * 1.852), 1)

        return {
            "system": {
                "leader": LEADER,
                "mode": "FOUNDATION" if foundation else "DOMINION",
                "trip_count": self.trip_count
            },
            "globe": {
                "position": [last["lat"], last["lon"]],
                "destination": [sh["dest_lat"], sh["dest_lon"]],
                "threat": threat,
                "eta_hours": eta
            },
            "finance": {
                "trip_profit": round(net, 2),
                "leader_vault": round(self.wallet["Leader_Net"], 2),
                "currency": region["currency"]
            },
            "integrity": {
                "trust": f"{trust}%",
                "signature": last["proof"][:16]
            }
        }

    # ---------------------
    def haversine(self, lat1, lon1, lat2, lon2):
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = (
            math.sin(dlat/2)**2 +
            math.cos(math.radians(lat1)) *
            math.cos(math.radians(lat2)) *
            math.sin(dlon/2)**2
        )
        return 2 * R * math.asin(math.sqrt(a))

    # ---------------------
    def save_state(self):
        with open(VAULT_FILE, "w") as f:
            json.dump({
                "ais": self.ais,
                "wallet": self.wallet,
                "trip_count": self.trip_count
            }, f)

    def load_state(self):
        if os.path.exists(VAULT_FILE):
            with open(VAULT_FILE, "r") as f:
                d = json.load(f)
                self.ais = d.get("ais", {})
                self.wallet = d.get("wallet", {"Leader_Net": 0.0})
                self.trip_count = d.get("trip_count", 0)

# =========================
# 🌐 API
# =========================
omega = SovereignOmega()

@app.route("/")
def home():
    return {"status": "OMEGA ONLINE"}

@app.route("/api/ais", methods=["POST"])
def ais_ingest():
    omega.ingest(request.json)
    return {"ingested": True}

@app.route("/api/radar/<sid>")
def radar_api(sid):
    return jsonify(omega.radar(sid))

# =========================
# 🟢 ENTRY POINT (RENDER)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
