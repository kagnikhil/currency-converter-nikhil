"""
web_app.py
Flask web server for the Global Currency Converter.
Runs locally at http://localhost:5001 (or http://127.0.0.1:5001)

Run:
    python3 web_app.py
"""

import os
import sys
from flask import Flask, render_template, jsonify, request, send_from_directory

# Add workspace directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from currency_service import CurrencyService
from currency_data import CURRENCY_INFO, PRESETS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static"),
)
currency_service = CurrencyService()

# Pre-fetch initial rates
currency_service.fetch_rates("USD")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/ppt")
def presentation():
    ppt_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "ppt")
    return send_from_directory(ppt_dir, "index.html")


@app.route("/api/currencies", methods=["GET"])
def get_currencies():
    """Returns all supported currencies and regional presets."""
    return jsonify({
        "currencies": CURRENCY_INFO,
        "presets": PRESETS,
        "total": len(CURRENCY_INFO)
    })


@app.route("/api/rates", methods=["GET"])
def get_rates():
    """Returns exchange rates for specified base currency."""
    base = request.args.get("base", "USD").upper().strip()
    force = request.args.get("force", "false").lower() == "true"
    rates = currency_service.fetch_rates(base, force_refresh=force)
    return jsonify({
        "base": base,
        "rates": rates,
        "source": currency_service.last_source,
        "is_offline": currency_service.is_offline,
        "last_updated": currency_service.last_updated
    })


@app.route("/api/convert", methods=["POST"])
def convert_single():
    """Converts amount from one currency to another."""
    data = request.get_json() or {}
    try:
        amount = float(data.get("amount", 1.0))
        from_curr = data.get("from", "USD")
        to_curr = data.get("to", "INR")
        res = currency_service.convert(amount, from_curr, to_curr)
        return jsonify(res)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/convert-multiple", methods=["POST"])
def convert_multiple():
    """Converts base currency to multiple target currencies."""
    data = request.get_json() or {}
    try:
        amount = float(data.get("amount", 100.0))
        base = data.get("base", "USD")
        targets = data.get("targets", ["EUR", "GBP", "INR", "JPY", "AUD", "CAD"])
        results = currency_service.convert_multiple(amount, base, targets)
        return jsonify({
            "success": True,
            "base": base,
            "amount": amount,
            "results": results
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400


@app.route("/api/refresh", methods=["POST"])
def refresh_rates():
    """Force refreshes live rates from API."""
    rates = currency_service.fetch_rates("USD", force_refresh=True)
    return jsonify({
        "success": True,
        "source": currency_service.last_source,
        "is_offline": currency_service.is_offline,
        "last_updated": currency_service.last_updated
    })


@app.route("/api/status", methods=["GET"])
def get_status():
    """Returns current connection status and sync time."""
    return jsonify({
        "is_offline": currency_service.is_offline,
        "source": currency_service.last_source,
        "last_updated": currency_service.last_updated
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"==================================================")
    print(f"🌍 Starting Currency Converter Web Server")
    print(f"🚀 Running on: http://localhost:{port} / http://127.0.0.1:{port}")
    print(f"==================================================")
    app.run(host="0.0.0.0", port=port, debug=False)
