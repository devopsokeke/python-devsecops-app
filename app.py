import os
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the DevSecOps Python App!"})

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    host = os.getenv('APP_HOST', '127.0.0.1')  # Defaults to localhost
    port = int(os.getenv('APP_PORT', '5000'))  # Defaults to port 5000
    app.run(host=host, port=port)
