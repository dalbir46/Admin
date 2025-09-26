from flask import Flask, request, send_file
from flask_cors import CORS
import matplotlib.pyplot as plt
import io

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Flask LaTeX API is running on Render!"

@app.route("/render", methods=["POST"])
def render_latex():
    data = request.get_json()
    latex = data.get("latex", "")

    fig, ax = plt.subplots()
    ax.axis("off")
    ax.text(0.5, 0.5, f"${latex}$", fontsize=20, ha="center", va="center")

    buf = io.BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", dpi=200)
    plt.close(fig)
    buf.seek(0)
    return send_file(buf, mimetype="image/png")
