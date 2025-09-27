from flask import Flask, request, jsonify
import io, base64, requests
import matplotlib.pyplot as plt

app = Flask(__name__)

IMGBB_API_KEY = "9a1627658ec3732fd03cb87cbff0ed66"  # 🔑 आपकी imgbb API key

# Home route so that "/" works
@app.route("/")
def home():
    return "✅ Flask API is running on Render!"

@app.route("/render", methods=["POST"])
def render():
    data = request.get_json()
    latex = data.get("latex", "")

    if not latex:
        return jsonify({"error": "No LaTeX provided"}), 400

    # LaTeX से image बनाओ
    fig, ax = plt.subplots()
    ax.text(0.5, 0.5, f"${latex}$", fontsize=20, ha="center", va="center")
    ax.axis("off")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.5)
    buf.seek(0)

    # imgbb पर upload करो
    url = "https://api.imgbb.com/1/upload"
    payload = {
        "key": IMGBB_API_KEY,
        "image": base64.b64encode(buf.read()).decode("utf-8")  # ✅ decode to string
    }
    r = requests.post(url, data=payload)  # ✅ fixed (data=payload)
    res = r.json()

    if "data" in res:
        return jsonify({"image_url": res["data"]["url"]})
    else:
        return jsonify({"error": "Upload failed", "details": res})
