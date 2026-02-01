from flask import Flask, request, jsonify
from flask_cors import CORS
import uuid
import time

app = Flask(__name__)
CORS(app)

# قاعدة بيانات مؤقتة
shipments = {}

# -------------------------------
# تسعير الشحن البحري
# -------------------------------
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

# -------------------------------
# إنشاء شحنة
# -------------------------------
@app.route("/api/marine/create", methods=["POST"])
def create_shipment():
    shipment_id = str(uuid.uuid