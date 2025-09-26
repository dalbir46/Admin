from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import io, base64
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

app = Flask(__name__)
CORS(app)

# Home route - सिर्फ टेस्ट के लिए
@app.route("/")
def home():
    return "✅ Flask LaTeX API is running on Render!"

# POST API → LaTeX को PNG में convert करके Base64 return करेगा
@app.route("/latex", methods=["POST"])
def latex_to_png():
    data = request.json
    latex_code = data.get("latex", "")

    fig, ax = plt.subplots()
    ax.axis("off")
    ax.text(0.5, 0.5, f"${latex_code}$", fontsize=20, ha="center", va="center")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode("utf-8")
    return jsonify({"image_base64": image_base64})

# GET API → Example equation render करके सीधा PNG दिखाएगा
@app.route("/render")
def render_example():
    latex_code = r"x^2 + y^2 = z^2"  # Example
    fig, ax = plt.subplots()
    ax.axis("off")
    ax.text(0.5, 0.5, f"${latex_code}$", fontsize=20, ha="center", va="center")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    buf.seek(0)

    return send_file(buf, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
