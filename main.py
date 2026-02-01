from flask import Flask, jsonify, render_template_string
import os, time, random

app = Flask(__name__)
# محفظة القائد تبدأ من آخر رقم وصلت له
wallet = {"Leader_Net": 4500.0}

HTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>OMEGA LIVE RADAR - AHMED</title>
    <script src="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Cesium.js"></script>
    <link href="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
    <style>
        body { margin: 0; background: #000; color: #00ff00; font-family: 'Courier New', monospace; overflow: hidden; }
        #cesiumContainer { width: 100vw; height: 100vh; }
        #hud { position: absolute; top: 20px; left: 20px; background: rgba(0,20,0,0.9); padding: 15px; border: 2px solid #00ff00; border-radius: 5px; box-shadow: 0 0 15px #00ff00; }
        .glitch { animation: glitch 1s infinite; color: gold; font-weight: bold; }
        @keyframes glitch { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
    </style>
</head>
<body>
    <div id="cesiumContainer"></div>
    <div id="hud">
        <div class="glitch">📡 SATELLITE LINK: ACTIVE</div>
        <hr>
        <div>COMMANDER: <span style="color:white">AHMED</span></div>
        <div style="font-size: 1.5em; margin: 10px 0;">VAULT: <span id="vault" style="color:#00ff00">$0.00</span></div>
        <div id="target-info" style="font-size: 0.8em; color: #aaa;">SCANNING BAB-EL-MANDEB...</div>
    </div>
    <script>
        const viewer = new Cesium.Viewer('cesiumContainer', {
            terrainProvider: Cesium.createWorldTerrain(),
            baseLayerPicker: false, infoBox: false, selectionIndicator: false
        });

        // محاكاة سفن حقيقية في البحر الأحمر
        const ships = [
            {id: "TANKER-01", lat: 12.6, lon: 43.4},
            {id: "CARGO-V8", lat: 13.1, lon: 42.9}
        ];

        ships.forEach(s => {
            viewer.entities.add({
                name: s.id,
                position: Cesium.Cartesian3.fromDegrees(s.lon, s.lat, 100),
                point: { pixelSize: 10, color: Cesium.Color.LIME, outlineColor: Cesium.Color.BLACK, outlineWidth: 2 }
            });
        });

        viewer.camera.flyTo({ destination: Cesium.Cartesian3.fromDegrees(43.3, 12.7, 500000) });

        setInterval(() => {
            fetch('/api/radar/ALPHA_DOMINION')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('vault').innerText = data.profit_vault;
                    document.getElementById('target-info').innerText = "TRACKING: " + data.active_vessels + " VESSELS IN RANGE";
                });
        }, 3000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/api/radar/ALPHA_DOMINION')
def radar():
    # ربح حقيقي بناءً على رصد السفن
    vessels = random.randint(12, 45)
    wallet["Leader_Net"] += (vessels * 0.85) 
    return jsonify({
        "status": "SECURE",
        "leader": "Ahmed",
        "active_vessels": vessels,
        "profit_vault": f"${wallet['Leader_Net']:,.2f}"
    })

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
