from flask import Flask, jsonify
import os

app = Flask(__name__)

# المحفظة تبدأ من صفر
wallet = {"Leader_Net": 0.0}

@app.route('/')
def home():
    return "OMEGA IS READY"

@app.route('/api/radar/ALPHA_DOMINION')
def radar():
    # مع كل تحديث للصفحة، المحفظة تزيد 500 دولار
    wallet["Leader_Net"] += 500.0
    return jsonify({
        "status": "ACTIVE",
        "leader": "Ahmed",
        "profit_vault": f"{wallet['Leader_Net']} USD"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
