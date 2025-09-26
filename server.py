from flask import Flask, request, send_file
import subprocess, uuid, os

app = Flask(__name__)

@app.route("/compile", methods=["POST"])
def compile_latex():
    data = request.get_json()
    latex_code = data.get("latex", "")

    # unique file names
    file_id = str(uuid.uuid4())
    tex_file = f"{file_id}.tex"
    pdf_file = f"{file_id}.pdf"
    png_file = f"{file_id}.png"

    # latex file likhna
    with open(tex_file, "w") as f:
        f.write("\\documentclass{article}\n"
                "\\usepackage{amsmath,amsfonts,amssymb}\n"
                "\\usepackage{array}\n"
                "\\usepackage[margin=0.5in]{geometry}\n"
                "\\thispagestyle{empty}\n"
                "\\begin{document}\n"
                + latex_code +
                "\n\\end{document}")

    # compile LaTeX → PDF
    subprocess.run(["pdflatex", "-interaction=nonstopmode", tex_file],
                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    # convert PDF → PNG (ImageMagick / GraphicsMagick required)
    subprocess.run(["convert", "-density", "300", pdf_file, "-quality", "90", png_file])

    # send image
    return send_file(png_file, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
