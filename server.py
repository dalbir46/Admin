from flask import Flask, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "✅ Server is running! Use /render?latex=... for LaTeX."

@app.route("/render")
def render_latex():
    latex_code = request.args.get("latex", "")
    if not latex_code:
        return "❌ Error: 'latex' parameter missing", 400

    # फिलहाल simple text return kar rahe hain (test ke liye)
    # Baad me yahan TeXLive/Docker/Math rendering add karenge
    return Response(f"You sent LaTeX: {latex_code}", mimetype="text/plain")
