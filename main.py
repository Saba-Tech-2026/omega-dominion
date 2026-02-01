from flask import Flask, jsonify, render_template_string
import os, time

app = Flask(__name__)
wallet = {"Leader_Net": 3000.0}

# واجهة الكرة الأرضية (HTML/JavaScript)
HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>OMEGA V8.1 - Ahmed</title>
    <script src="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Cesium.js"></script>
    <link href="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
    <style>
        body { margin: 0; background: #000; color: gold; font-family: sans-serif; overflow: hidden; }
        #cesiumContainer { width: 100vw; height: 100vh; }
        #hud { position: absolute; top: 20px; left: 20px; background: rgba(0,0,0,0.8); padding: 20px; border: 1px solid gold; border-radius: 10px; pointer-events: none; }
        .stat { font-size: 1.2em; margin-bottom: 10px; }
        .value { color: #fff; font-weight: bold; }
    </style>
</head>
<body>
    <div id="cesiumContainer"></div>
    <div id="hud">
        <h2>👑 OMEGA COMMAND</h2>
        <div class="stat">Leader: <span class="value">Ahmed</span></div>
        <div class="stat">Vault: <span class="value" id="vault">$3,000.00</span></div>
        <div class="stat">Target: <span class="value">Babel-Mandeb</span></div>
        <div class="stat">Status: <span class="value" style="color: lime;">ACTIVE</span></div>
    </div>
    <script>
        const viewer = new Cesium.Viewer('cesiumContainer', {
            terrainProvider: Cesium.createWorldTerrain(),
            baseLayerPicker: false, geocoder: false, homeButton: false, infoBox: false
        });
        // وضع سفينة تجريبية
        const ship = viewer.entities.add({
            position: Cesium.Cartesian3.fromDegrees(43.0, 12.0, 500),
            point: { pixelSize: 15, color: Cesium.Color.RED, outlineColor: Cesium.Color.WHITE, outlineWidth: 2 }
        });
        viewer.zoomTo(ship);
        
        // تحديث العداد تلقائياً
        setInterval(() => {
            fetch('/api/radar/ALPHA_DOMINION')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('vault').innerText = data.profit_vault;
                });
        }, 5000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/api/radar/ALPHA_DOMINION')
def radar():
    wallet["Leader_Net"] += 1.5 # ربح تلقائي
    return jsonify({
        "status": "ACTIVE",
        "leader": "Ahmed",
        "profit_vault": f"${wallet['Leader_Net']:,.2f} USD"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
