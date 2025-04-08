pytnon: from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os

app = Flask(__name__, static_folder="static")
CORS(app)  # laat JS toe om te praten met Python

BESTAND = "messages.txt"

# Als 'messages.txt' niet bestaat, maak hem aan
if not os.path.exists(BESTAND):
    with open(BESTAND, "w") as f:
        pass

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/get", methods=["GET"])
def get_messages():
    with open(BESTAND, "r", encoding="utf-8") as f:
        lines = f.readlines()
    return jsonify([line.strip() for line in lines])

@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()
    name = data.get("name", "😶")
    msg = data.get("msg", "")
    if msg.strip() != "":
        with open(BESTAND, "a", encoding="utf-8") as f:
            f.write(f"{name}: {msg}\n")
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')

