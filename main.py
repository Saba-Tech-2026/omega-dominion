from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import time

app = Flask(__name__)
CORS(app)

# --------------------------------
# قاعدة بيانات مؤقتة
# --------------------------------
shipments = {}

# --------------------------------
# تسعير الشحن البحري
# --------------------------------
@app.route("/api/marine/quote", methods=["POST"])
def marine_quote():
    data = request.json or {}

    weight = float(data.get("weight", 0))
    distance = float(data.get("distance", 0))

    price = weight * distance * 0.02

    return jsonify({
        "service": "marine_shipping",
        "price_usd": round(price, 2)
    })


# --------------------------------
# إنشاء شحنة
# --------------------------------
@app.route("/api/marine/create", methods=["POST"])
def create_shipment():
    shipment_id = str(uuid.uuid4())[:8]

    shipments[shipment_id] = {
        "status": "IN_TRANSIT",
        "location": "PORT OF ORIGIN",
        "eta_hours": 72,
        "created": int(time.time())
    }

    return jsonify({
        "shipment_id": shipment_id,
        "message": "Shipment created successfully"
    })


# --------------------------------
# تتبع شحنة
# --------------------------------
@app.route("/api/marine/track/<shipment_id>", methods=["GET"])
def track_shipment(shipment_id):
    shipment = shipments.get(shipment_id)

    if not shipment:
        return jsonify({"error": "Shipment not found"}), 404

    return jsonify({
        "shipment_id": shipment_id,
        "data": shipment
    })


# --------------------------------
# تشغيل السيرفر
# --------------------------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)