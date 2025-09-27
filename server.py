from flask import Flask, request, jsonify
from flask_cors import CORS
import io, base64, requests
import matplotlib.pyplot as plt

app = Flask(__name__)
CORS(app)  # ✅ CORS enabled for all origins

IMGBB_API_KEY = "9a1627658ec3732fd03cb87cbff0ed66"  # 🔑 Tumhari ImgBB key

# ✅ Home route (Render health check)
@app.route("/")
def home():
    return "✅ Flask LaTeX API is running on Render!"

# ✅ Render route
@app.route("/render", methods=["POST"])
def render():
    try:
        data = request.get_json()
        latex = data.get("latex", "")

        if not latex:
            return jsonify({"error": "No LaTeX provided"}), 400

        # --- Create LaTeX image ---
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f"${latex}$", fontsize=20, ha="center", va="center")
        ax.axis("off")

        buf = io.BytesIO()
        plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.5)
        buf.seek(0)

        # --- Upload to ImgBB ---
        url = "https://api.imgbb.com/1/upload"
        payload = {
            "key": IMGBB_API_KEY,
            "image": base64.b64encode(buf.read()).decode("utf-8")
        }
        r = requests.post(url, data=payload)
        res = r.json()

        if "data" in res:
            return jsonify({"image_url": res["data"]["url"]})
        else:
            return jsonify({"error": "Upload failed", "details": res}), 500

    except Exception as e:
        return jsonify({"error": "Server error", "details": str(e)}), 500

# ✅ Run locally (Render uses gunicorn)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
