from flask import Flask, request
import os, time

app = Flask(__name__)
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.route('/upload', methods=['POST'])
def upload():
    image = request.files.get('image')
    result = request.form.get('result', 'no result')
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    fname = f"{timestamp}.jpg"
    image.save(os.path.join(UPLOAD_DIR, fname))
    with open(os.path.join(UPLOAD_DIR, "log.txt"), "a") as f:
        f.write(f"{timestamp}: {result}\n")
    print(f"[+] Received {fname} | result = {result}")
    return "OK"
