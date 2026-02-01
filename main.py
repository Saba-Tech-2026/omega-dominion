wwfrom flask import Flask, jsonify, render_template_string
import os, random

app = Flask(__name__)
# رصيد القائد يبدأ من هنا
wallet = {"Leader_Net": 4500.0}

wwHTML_INTERFACE = """
<!DOCTYPE html>
<html>
<head>
    <title>OMEGA V8 - COMMANDER AHMED</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Cesium.js"></script>
    <link href="https://cesium.com/downloads/cesiumjs/releases/1.105/Build/Cesium/Widgets/widgets.css" rel="stylesheet">
    <style>
        body { margin: 0; background: #000; color: #00ff00; font-family: monospace; overflow: hidden; }
        #cesiumContainer { width: 100vw; height: 100vh; }
        #hud { 
            position: absolute; top: 10px; left: 10px; 
            background: rgba(0,20,0,0.85); padding: 15px; 
            border: 1px solid #00ff00; border-radius: 5px;
            z-index: 1000; pointer-events: none;
            box-shadow: 0 0 10px #00ff00;
        }
        .stat-label { color: gold; font-size: 0.8em; }
        .stat-value { font-size: 1.2em; display: block; margin-bottom: 5px; }
    </style>
</head>
<body>
    <div id="hud">
        <div style="border-bottom: 1px solid #00ff00; margin-bottom: 10px; padding-bottom: 5px;">
            <b style="color:white;">OFFICIAL OMEGA RADAR</b>
        </div>
        <span class="stat-label">COMMANDER:</span>
        <span class="stat-value">AHMED</span>
        <span class="stat-label">VAULT PROFIT:</span>
        <span id="vault" class="stat-value" style="color: #00ff00;">$4,500.00</span>
        <span class="stat-label">SATELLITE STATUS:</span>
        <span id="status" class="stat-value" style="color: lime; font-size: 0.9em;">SCANNING...</span>
    </div>
    <div id="cesiumContainer"></div>
    <script>
        // تشغيل الخريطة بدون الحاجة لمفتاح تعقيدي
        const viewer = new Cesium.Viewer('cesiumContainer', {
            baseLayerPicker: false, geocoder: false, homeButton: false, 
            infoBox: false, selectionIndicator: false, timeline: false, 
            animation: false, navigationHelpButton: false, sceneModePicker: false
        });

        // تحديد موقع الكاميرا على البحر الأحمر وباب المندب
        viewer.camera.setView({
            destination: Cesium.Cartesian3.fromDegrees(43.3, 12.7, 800000)
        });

        // وظيفة لتحديث الأرقام من السيرفر
        function updateData() {
            fetch('/api/radar/ALPHA_DOMINION')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('vault').innerText = data.profit_vault;
                    document.getElementById('status').innerText = "TRACKING " + data.active_vessels + " VESSELS";
                });
        }

        // تحديث كل 4 ثوانٍ
        setInterval(updateData, 4000);
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_INTERFACE)

@app.route('/api/radar/ALPHA_DOMINION')
def radar():
    vessels = random.randint(15, 60)
    # كل تحديث يضيف مبلغ لنسبة القائد (80%)
    wallet["Leader_Net"] += (vessels * 1.2)
    return jsonify({
        "status": "SECURE",
        "leader": "Ahmed",
        "active_vessels": vessels,
        "profit_vault": f"${wallet['Leader_Net']:,.2f}"
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
