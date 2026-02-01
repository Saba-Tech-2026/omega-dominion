from flask import Flask, jsonify
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)

# =========================================
# محاكاة بيانات شحن بحري
# =========================================
def generate_marine_data():
    return {
        "system": {
            "name": "OMEGA MARINE SYSTEM",
            "mode": "MARINE_SHIPPING",
            "status": "ONLINE"
        },

        "ship": {
            "name": "OMEGA-ATLANTIC",
            "captain": "CAPT. SALEH",
            "status": random.choice(["SAILING", "DOCKED", "ANCHOR"])
        },

        "route": {
            "current_port": random.choice(["JEDDAH", "ADEN", "SUEZ", "SINGAPORE"]),
            "destination_port": random.choice(["ROTTERDAM", "SHANGHAI", "DUBAI"])
        },

        "globe": {
            "position": [
                round(random.uniform(-90, 90), 2),
                round(random.uniform(-180, 180), 2)
            ],
            "destination": ["ROTTERDAM"],
            "eta_hours": random.randint(24, 240),
            "threat": random.choice(["SAFE", "SAFE", "SAFE", "RISK"])
        },

        "cargo": {
            "type": "CONTAINERS",
            "weight_ton": random.randint(500, 5000),
            "status": "ON_BOARD"
        },

        "finance": {
            "trip_profit": random.randint(8000, 30000),
            "currency": "USD",
            "fuel_cost": random.randint(2000, 8000),
            "port_fees": random.randint(1000, 4000),
            "net_profit": random.randint(5000, 20000),
            "leader_vault": random.randint(100000, 300000)
        },

        "timestamp": int(time.time())
    }


# =========================================
# API المتوافق مع index.html
# =========================================
@app.route("/api/radar/ALPHA_DOMINION", methods=["GET"])
def marine_radar():
    return jsonify(generate_marine_data())


# =========================================
# تشغيل السيرفر
# =========================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)