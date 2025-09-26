from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess
import tempfile
import os

app = Flask(__name__)
CORS(app)  # CORS enable

@app.route("/")
def home():
    return "✅ Flask LaTeX API is running on Render!"

@app.route("/latex", methods=["POST"])
def render_latex():
    try:
        data = request.get_json()
        latex_code = data.get("latex", "")

        if not latex_code:
            return jsonify({"error": "No LaTeX code provided"}), 400

        # temporary directory for output
        with tempfile.TemporaryDirectory() as tmpdir:
            tex_file = os.path.join(tmpdir, "equation.tex")
            pdf_file = os.path.join(tmpdir, "equation.pdf")
            png_file = os.path.join(tmpdir, "equation.png")

            # write latex file
            with open(tex_file, "w") as f:
                f.write(r"""
\documentclass[12pt]{article}
\usepackage{amsmath}
\pagestyle{empty}
\begin{document}
%s
\end{document}
""" % latex_code)

            # run pdflatex → dvisvgm / imagemagick (assume installed)
            subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_file], cwd=tmpdir, check=True)
            subprocess.run(["convert", "-density", "200", pdf_file, "-quality", "90", png_file], check=True)

            # read image as base64
            with open(png_file, "rb") as imgf:
                import base64
                encoded = base64.b64encode(imgf.read()).decode("utf-8")

            return jsonify({"image_base64": encoded})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
