from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import time
import random

app = Flask(__name__)
CORS(app)

# ==================================================
# قاعدة بيانات مؤقتة (لاحقًا MySQL / PostgreSQL)
# ==================================================
shipments = {}

# ==================================================
# 1️⃣ تسعير الشحن البحري
# ==================================================
@app.route("/api/marine/quote", methods=["POST"])
def marine_quote():
    data = request.json or {}

    weight = float(data.get("weight", 0))      # بالطن
    distance = float(data.get("distance", 0))  # بالكيلومتر

    base_rate = 0.02
    price = weight * distance * base_rate

    return jsonify({
        "service": "marine_shipping",
        "weight_ton": weight,
        "distance_km": distance,
        "price_usd": round(price, 2)
    })


# ==================================================
# 2️⃣ إنشاء شحنة جديدة
# ==================================================
@app.route("/api/marine/create", methods=["POST"])
def create_shipment():
    data = request.json or {}

    shipment_id = str(uuid.uuid4())[:8]

    shipments[shipment_id] = {
        "id": shipment_id,
        "origin": data.get("origin", "PORT-A"),
        "destination": data.get("destination", "PORT-B"),
        "status": "CREATED",
        "position": [0.0, 0.0],
        "eta_hours": random.randint(72, 240),
        "customs": "PENDING",
        "created_at": time.time(),
        "profit_usd": random.randint(5000, 25000)
    }

    return jsonify({
        "message": "Shipment created",
        "shipment_id": shipment_id
    })


# ==================================================
# 3️⃣ نظام التتبع البحري (يطلع فلوس)
# ==================================================
@app.route("/api/marine/track/<shipment_id>", methods=["GET"])
def track_shipment(shipment_id):
    shipment = shipments.get(shipment_id)

    if not shipment:
        return jsonify({"error": "Shipment not found"}), 404

    # محاكاة حركة السفينة
    shipment["position"][0] += round(random.uniform(0.5, 2.0), 2)
    shipment["position"][1] += round(random.uniform(0.5, 2.0), 2)

    shipment["eta_hours"] = max(shipment["eta_hours"] - 1, 0)

    if shipment["eta_hours"] == 0:
        shipment["status"] = "ARRIVED"
        shipment["customs"] = "CLEARED"

    threat = random.choice(["SAFE", "SAFE", "SAFE", "RISK"])

    return jsonify({
        "system": {
            "shipment_id": shipment_id,
            "status": shipment["status"]
        },
        "globe": {
            "position": shipment["position"],
            "destination": shipment["destination"],
            "eta_hours": shipment["eta_hours"],
            "threat": threat
        },
        "finance": {
            "trip_profit": shipment["profit_usd"],
            "currency": "USD"
        },
        "customs": {
            "status": shipment["customs"]
        }
    })


# ==================================================
# 4️⃣ التخليص الجمركي
# ==================================================
@app.route("/api/marine/customs/clear/<shipment_id>", methods=["POST"])
def clear_customs(shipment_id):
    shipment = shipments.get(shipment_id)

    if not shipment:
        return jsonify({"error": "Shipment not found"}), 404

    shipment["customs"] = "CLEARED"

    return jsonify({
        "message": "Customs cleared successfully",
        "shipment_id": shipment_id
    })


# ==================================================
# تشغيل السيرفر
# ==================================================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)