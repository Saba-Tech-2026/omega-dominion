# ==============================
# OMEGA DOMINION – FULL SYSTEM
# ==============================

import os
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ==============================
# CORE ENGINE
# ==============================

class OmegaCore:
    def __init__(self):
        self.online_since = datetime.utcnow().isoformat()
        self.ingested_packets = []
        self.radar_memory = {}

    def status(self):
        return {
            "system": "OMEGA DOMINION",
            "state": "ONLINE",
            "since": self.online_since,
            "ingested_count": len(self.ingested_packets)
        }

    def ingest(self, payload):
        if not payload:
            return False

        record = {
            "timestamp": datetime.utcnow().isoformat(),
            "payload": payload
        }
        self.ingested_packets.append(record)

        sid = payload.get("sid")
        if sid:
            self.radar_memory[sid] = {
                "last_seen": record["timestamp"],
                "data": payload
            }
        return True

    def radar(self, sid):
        return self.radar_memory.get(sid, {
            "error": "SID NOT FOUND"
        })


omega = OmegaCore()

# ==============================
# ROUTES / API
# ==============================

@app.route("/", methods=["GET"])
def home():
    return jsonify(omega.status())

@app.route("/api/ingest", methods=["POST"])
def api_ingest():
    data = request.json
    ok = omega.ingest(data)# commit fix
    return jsonify({"ingested": ok})

@app.route("/api/radar/<sid>", methods=["GET"])
def api_radar(sid):
    return jsonify(omega.radar(sid))

# ==============================
# ENTRY POINT (RENDER)
# ==============================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
