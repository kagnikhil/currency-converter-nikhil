"""
web_app.py
Local server launcher for Currency Converter.
Runs locally at http://localhost:5001 (or http://127.0.0.1:5001).

Run:
    python3 web_app.py
"""

import os
import sys

# Ensure root directory is on python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from api.index import app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print("==================================================")
    print("🌍 Starting Currency Converter Web Server")
    print(f"🚀 Running on: http://localhost:{port} / http://127.0.0.1:{port}")
    print("==================================================")
    app.run(host="0.0.0.0", port=port, debug=False)
