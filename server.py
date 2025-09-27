from flask import Flask, request, jsonify
import subprocess, os, io, base64, requests, uuid

app = Flask(__name__)

IMGBB_API_KEY = "9a1627658ec3732fd03cb87cbff0ed66"  # 🔑 imgbb API key

@app.route("/")
def home():
    return "✅ Flask LaTeX API is running!"

@app.route("/render", methods=["POST"])
def render():
    data = request.get_json()
    latex_code = data.get("latex", "")

    if not latex_code:
        return jsonify({"error": "No LaTeX provided"}), 400

    # Temporary filenames
    job_id = str(uuid.uuid4())
    tex_file = f"/tmp/{job_id}.tex"
    pdf_file = f"/tmp/{job_id}.pdf"
    png_file = f"/tmp/{job_id}.png"

    # Full LaTeX document
    tex_content = f"""
    \\documentclass[preview]{{standalone}}
    \\usepackage{{amsmath, amssymb}}
    \\usepackage{{array}}
    \\begin{document}
    {latex_code}
    \\end{document}
    """

    # Write .tex file
    with open(tex_file, "w") as f:
        f.write(tex_content)

    try:
        # Compile LaTeX → PDF
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-output-directory", "/tmp", tex_file],
            check=True, capture_output=True
        )

        # Convert PDF → PNG
        subprocess.run(
            ["gs", "-sDEVICE=pngalpha", "-o", png_file, "-r150", pdf_file],
            check=True, capture_output=True
        )

        # Upload to imgbb
        with open(png_file, "rb") as f:
            payload = {
                "key": IMGBB_API_KEY,
                "image": base64.b64encode(f.read()).decode("utf-8")
            }
        r = requests.post("https://api.imgbb.com/1/upload", data=payload)
        res = r.json()

        if "data" in res:
            return jsonify({"image_url": res["data"]["url"]})
        else:
            return jsonify({"error": "Upload failed", "details": res})

    except subprocess.CalledProcessError as e:
        return jsonify({"error": "LaTeX compilation failed", "details": e.stderr.decode("utf-8")})

    finally:
        # Cleanup
        for f in [tex_file, pdf_file, png_file, f"/tmp/{job_id}.aux", f"/tmp/{job_id}.log"]:
            if os.path.exists(f):
                os.remove(f)
