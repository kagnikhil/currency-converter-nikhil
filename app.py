"""
app.py
Main entry point for the Currency Converter College Project.

Run this script using:
    python3 app.py
"""

import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from currency_service import CurrencyService
from ui.main_window import MainWindow


def main():
    print("==================================================")
    print("🌍 Starting Global Currency Converter Desktop App")
    print("Python College Project")
    print("==================================================")

    # Initialize backend currency service
    service = CurrencyService()

    # Pre-fetch initial rates in memory
    print("Initializing live exchange rate data...")
    service.fetch_rates("USD")
    print(f"Status: {'Offline (Using Cache)' if service.is_offline else 'Online (Live API)'}")

    # Launch GUI
    app = MainWindow(currency_service=service)
    app.mainloop()


if __name__ == "__main__":
    main()
