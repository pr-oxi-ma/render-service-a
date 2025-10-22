from flask import Flask, jsonify
import requests
import threading
import time

app = Flask(__name__)

# 👇 Ye sab ping honge (Service B + baaki tumhare URLs)
URLS = [
    "https://gpt4free-3u5v.onrender.com",
    "https://render-downloader-8aqy.onrender.com"
    "https://render-service-b.onrender.com"  # Service B ka root
    "https://mern-chat-app-76ug.onrender.com",
]

status_data = {url: "unknown" for url in URLS}

def ping_urls():
    while True:
        for url in URLS:
            try:
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    status_data[url] = "ok"
                else:
                    status_data[url] = f"error {r.status_code}"
            except Exception:
                status_data[url] = "down"
        time.sleep(300)  # 5 min

@app.route("/")
def home():
    return jsonify({"status": "ok"})

@app.route("/health")
def health():
    return jsonify(status_data)

if __name__ == "__main__":
    t = threading.Thread(target=ping_urls, daemon=True)
    t.start()
    app.run(host="0.0.0.0", port=10000)
    
