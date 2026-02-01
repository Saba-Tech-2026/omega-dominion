@app.route("/api/marine/track/<shipment_id>", methods=["GET"])
def track_shipment(shipment_id):
    shipment = shipments.get(shipment_id)
    if not shipment:
        return jsonify({"error": "Shipment not found"}), 404

    # مخاطر ذكية
    threat = random.choices(
        ["SAFE", "STORM", "PIRACY", "DELAY"],
        [0.6, 0.2, 0.1, 0.1]
    )[0]

    speed = 1.0
    if threat == "STORM": speed = 0.5
    if threat == "DELAY": speed = 0.3

    shipment["position"][0] += round(random.uniform(0.5, 2.0) * speed, 2)
    shipment["position"][1] += round(random.uniform(0.5, 2.0) * speed, 2)

    shipment["eta_hours"] = max(shipment["eta_hours"] - speed, 0)

    # أرباح تراكمية
    shipment["profit_usd"] += int(200 * speed)

    if shipment["eta_hours"] <= 0:
        shipment["status"] = "ARRIVED"
        shipment["customs"] = "CLEARED"

    return jsonify({
        "system": {
            "shipment_id": shipment_id,
            "status": shipment["status"]
        },
        "globe": {
            "position": shipment["position"],
            "eta_hours": round(shipment["eta_hours"], 1),
            "threat": threat
        },
        "finance": {
            "total_profit": shipment["profit_usd"],
            "currency": "USD"
        },
        "customs": {
            "status": shipment["customs"]
        }
    })