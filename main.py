import os
from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# ==========================
# CORE ENGINE
# ==========================

class OmegaCore:
    def __init__(self):
        self.online_since = datetime.utcnow().isoformat()
        self.ingested_packets = []
        self.radar_memory = {}

    def status(self):
        return {
            "system": "OMEGA DOMINION",
            "state": "ONLINE",
            "since": self.online_since
        }

    def ingest(self, data):
        if not data:
            return False
        self.ingested_packets.append({
            "data": data,
            "time": datetime.utcnow().isoformat()
        })
        return True

    def radar(self, sid):
        self.radar_memory[sid] = {
            "seen": True,
            "last_check": datetime.utcnow().isoformat()
        }
        return self.radar_memory[sid]


# ==========================
# SYSTEM INSTANCE
# ==========================

omega = OmegaCore()


# ==========================
# API ROUTES
# ==========================

@app.route("/")
def home():
    return jsonify(omega.status())

@app.route("/api/ingest", methods=["POST"])
def api_ingest():
    data = request.json
    ok = omega.ingest(data)
    return jsonify({"ingested": ok})

@app.route("/api/radar/<sid>", methods=["GET"])
def api_radar(sid):
    return jsonify(omega.radar(sid))


# ==========================
# ENTRY POINT (RENDER)
# ==========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
