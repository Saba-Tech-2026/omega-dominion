from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import uuid
import time

app = Flask(__name__, static_folder="static")
CORS(app)

# -----------------------------
# بيانات تجريبية
# -----------------------------
shipments = {}

# -----------------------------
# الصفحة الرئيسية (الواجهة)
# -----------------------------
@app.route("/")
def index():
    return send_from_directory("static", "index.html")

# -----------------------------
# تسعير الشحن البحري
# -----------------------------
@app.route("/api/marine/quote", methods=["POST"])
def marine_quote():
    data = request.json
    weight = float(data.get("weight", 0))
    distance = float(data.get("distance", 0))

    price = weight * distance * 0.02

    return jsonify({
        "service": "marine_shipping",
        "price_usd": round(price, 2)
    })

# -----------------------------
# إنشاء شحنة جديدة
# -----------------------------
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

# -----------------------------
# تتبع الشحنة
# -----------------------------
@app.route("/api/marine/track/<shipment_id>")
def track_shipment(shipment_id):
    shipment = shipments.get(shipment_id)

    if not shipment:
        return jsonify({"error": "Shipment not found"}), 404

    return jsonify({
        "shipment_id": shipment_id,
        "status": shipment["status"],
        "current_location": shipment["location"],
        "eta_hours": shipment["eta_hours"]
    })

# -----------------------------
# التخليص الجمركي
# -----------------------------
@app.route("/api/marine/customs/<shipment_id>")
def customs_clearance(shipment_id):
    shipment = shipments.get(shipment_id)

    if not shipment:
        return jsonify({"error": "Shipment not found"}), 404

    shipment["status"] = "CUSTOMS_CLEARED"

    return jsonify({
        "shipment_id": shipment_id,
        "customs_status": "CLEARED"
    })

# -----------------------------
# تشغيل السيرفر
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)