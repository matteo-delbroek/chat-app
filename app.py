from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import time

app = Flask(__name__, static_folder="static")
CORS(app)  # laat JS toe om te praten met Python

BESTAND = "messages.txt"
LAATSTE_VERWIJDERING = time.time()  # Huidige tijd in seconden sinds 1 januari 1970

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

def verwijder_berichten():
    global LAATSTE_VERWIJDERING
    huidige_tijd = time.time()
    
    # Als het 10 minuten zijn (600 seconden) sinds de laatste verwijdering, verwijder de berichten
    if huidige_tijd - LAATSTE_VERWIJDERING > 600:
        with open(BESTAND, "w", encoding="utf-8") as f:
            f.truncate(0)  # Verwijdert alle berichten
        LAATSTE_VERWIJDERING = huidige_tijd

@app.before_request
def check_verwijder_berichten():
    verwijder_berichten()

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')


