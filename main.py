# ============================================
# OMEGA V8.1 – Neural Link
# Sovereign Core | Global Ready
# ============================================

import time
import json
import threading
from datetime import datetime
from flask import Flask, jsonify

# ============================================
# 🧠 OMEGA CORE CONFIG
# ============================================

SYSTEM_NAME = "OMEGA V8.1 – Neural Link"
SYSTEM_STATUS = "OPERATIONAL"
START_TIME = datetime.utcnow().isoformat()

DATA_FILE = "omega_vault.json"

# ============================================
# 🛡️ OMEGA SAFE-VAULT
# ============================================

class OmegaSafetyNet:
    @staticmethod
    def backup_state(core_data):
        try:
            with open(DATA_FILE, "w") as vault:
                json.dump(core_data, vault, indent=4)
        except Exception as e:
            print("Vault Backup Error:", e)

    @staticmethod
    def restore_state():
        try:
            with open(DATA_FILE, "r") as vault:
                return json.load(vault)
        except:
            return None

    @staticmethod
    def fail_safe(last_signal_time):
        if time.time() - last_signal_time > 3600:
            return "🆘 EMERGENCY MODE: SATELLITE RECOVERY ACTIVE"
        return "SIGNAL STABLE"

# ============================================
# 🌍 OMEGA GLOBAL ENGINE
# ============================================

class OmegaEngine:
    def __init__(self):
        self.last_signal_time = time.time()
        self.core_data = OmegaSafetyNet.restore_state() or {
            "system": SYSTEM_NAME,
            "created_at": START_TIME,
            "nodes": [],
            "global_events": [],
            "status": SYSTEM_STATUS
        }

    def heartbeat(self):
        while True:
            self.last_signal_time = time.time()
            OmegaSafetyNet.backup_state(self.core_data)
            time.sleep(600)  # كل 10 دقائق

    def system_status(self):
        return {
            "system": SYSTEM_NAME,
            "status": self.core_data["status"],
            "fail_safe": OmegaSafetyNet.fail_safe(self.last_signal_time),
            "uptime": START_TIME
        }

    def register_node(self, name):
        node = {
            "name": name,
            "registered_at": datetime.utcnow().isoformat()
        }
        self.core_data["nodes"].append(node)
        return node

# ============================================
# 🌐 API LAYER (READY FOR RENDER / DIGITALOCEAN)
# ============================================

app = Flask(__name__)
engine = OmegaEngine()

@app.route("/", methods=["GET"])
def root():
    return jsonify({
        "message": "OMEGA V8.1 – Neural Link is LIVE",
        "status": engine.system_status()
    })

@app.route("/status", methods=["GET"])
def status():
    return jsonify(engine.system_status())

@app.route("/register/<node_name>", methods=["POST"])
def register(node_name):
    node = engine.register_node(node_name)
    return jsonify({
        "registered": True,
        "node": node
    })

# ============================================
# 🚀 SYSTEM BOOT
# ============================================

if __name__ == "__main__":
    threading.Thread(target=engine.heartbeat, daemon=True).start()
    app.run(host="0.0.0.0", port=10000)