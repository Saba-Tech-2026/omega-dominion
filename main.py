from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder="static")

# الصفحة الرئيسية (واجهة الموقع)
@app.route("/")
def home():
    return send_from_directory("static", "index.html")

# API خدمات الشحن البحري
@app.route("/api/marine-shipping")
def marine_shipping():
    return jsonify({
        "service": "الشحن البحري",
        "features": [
            "نقل الحاويات",
            "شحن البضائع العامة",
            "التتبع البحري",
            "التخليص الجمركي"
        ],
        "status": "الخدمة تعمل بنجاح"
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)