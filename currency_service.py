"""
currency_service.py
Robust currency exchange service with:
- Multiple free, keyless APIs (ExchangeRate-API, Frankfurter, FawazAhmed Currency API)
- Automatic fallback mechanisms
- Offline local caching (JSON)
- In-memory rate caching for instant calculations
- Cross-rate computation
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Callable
import requests

from currency_data import CURRENCY_INFO, get_currency_display_str

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_DIR = os.path.join(BASE_DIR, "cache")
CACHE_FILE = os.path.join(CACHE_DIR, "rates_cache.json")


class CurrencyService:
    def __init__(self):
        self._memory_cache: Dict[str, Dict] = {}  # {base_currency: {"rates": {...}, "timestamp": ...}}
        self._last_fetch_source: str = "Uninitialized"
        self._last_updated_str: str = "Never"
        self._is_offline: bool = False
        self._supported_currencies: List[str] = sorted(list(CURRENCY_INFO.keys()))
        
        # Ensure cache directory exists (fallback to /tmp if read-only filesystem)
        try:
            os.makedirs(CACHE_DIR, exist_ok=True)
            self._cache_file_path = CACHE_FILE
        except Exception:
            self._cache_file_path = "/tmp/rates_cache.json"

        # Attempt to load local disk cache on startup
        self._load_disk_cache()

    @property
    def is_offline(self) -> bool:
        return self._is_offline

    @property
    def last_source(self) -> str:
        return self._last_fetch_source

    @property
    def last_updated(self) -> str:
        return self._last_updated_str

    def get_supported_currencies(self) -> List[str]:
        """Returns sorted list of available currency codes."""
        # Merge currencies from info dict and any fetched rates
        all_codes = set(self._supported_currencies)
        if "USD" in self._memory_cache:
            all_codes.update(self._memory_cache["USD"].get("rates", {}).keys())
        return sorted(list(all_codes))

    def get_currency_options(self) -> List[Tuple[str, str]]:
        """Returns list of (code, display_string) tuples for UI dropdowns."""
        codes = self.get_supported_currencies()
        options = []
        for code in codes:
            options.append((code, get_currency_display_str(code)))
        return options

    # -------------------------------------------------------------
    # API Fetching & Fallbacks
    # -------------------------------------------------------------
    def fetch_rates(self, base: str = "USD", force_refresh: bool = False) -> Dict[str, float]:
        """
        Fetches latest exchange rates for the given base currency.
        Utilizes memory cache, API cascades (Primary -> Fallback 1 -> Fallback 2),
        and persistent disk cache if offline.
        """
        base = base.upper().strip()

        # Check memory cache if not force refresh (cache valid for 1 hour)
        if not force_refresh and base in self._memory_cache:
            cached_data = self._memory_cache[base]
            if time.time() - cached_data.get("fetched_at", 0) < 3600:
                self._is_offline = False
                return cached_data["rates"]

        # Try Primary API: open.er-api.com (Free, no API key, 166 currencies)
        rates = self._fetch_primary_api(base)
        if rates:
            self._last_fetch_source = "ExchangeRate-API (Live)"
            self._is_offline = False
            self._update_cache(base, rates, source=self._last_fetch_source)
            return rates

        # Try Fallback 1: Frankfurter API (Free, ECB rates)
        rates = self._fetch_frankfurter_api(base)
        if rates:
            self._last_fetch_source = "Frankfurter / ECB (Live)"
            self._is_offline = False
            self._update_cache(base, rates, source=self._last_fetch_source)
            return rates

        # Try Fallback 2: FawazAhmed Currency API (JSDelivr CDN)
        rates = self._fetch_cdn_currency_api(base)
        if rates:
            self._last_fetch_source = "Currency-API CDN (Live)"
            self._is_offline = False
            self._update_cache(base, rates, source=self._last_fetch_source)
            return rates

        # If network failed, attempt to derive rates from local disk cache
        rates = self._derive_from_disk_cache(base)
        if rates:
            self._is_offline = True
            self._last_fetch_source = f"Offline Cache ({self._last_updated_str})"
            return rates

        # If absolutely no cache exists, use emergency built-in base rates
        return self._emergency_fallback_rates(base)

    def _fetch_primary_api(self, base: str) -> Optional[Dict[str, float]]:
        url = f"https://open.er-api.com/v6/latest/{base}"
        try:
            resp = requests.get(url, timeout=6)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("result") == "success" and "rates" in data:
                    rates = {k.upper(): float(v) for k, v in data["rates"].items()}
                    rates[base] = 1.0
                    return rates
        except Exception:
            pass
        return None

    def _fetch_frankfurter_api(self, base: str) -> Optional[Dict[str, float]]:
        url = f"https://api.frankfurter.app/latest?from={base}"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if "rates" in data:
                    rates = {k.upper(): float(v) for k, v in data["rates"].items()}
                    rates[base] = 1.0
                    return rates
        except Exception:
            pass
        return None

    def _fetch_cdn_currency_api(self, base: str) -> Optional[Dict[str, float]]:
        url = f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{base.lower()}.json"
        try:
            resp = requests.get(url, timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                base_key = base.lower()
                if base_key in data:
                    rates = {k.upper(): float(v) for k, v in data[base_key].items()}
                    rates[base] = 1.0
                    return rates
        except Exception:
            pass
        return None

    # -------------------------------------------------------------
    # Disk & In-Memory Caching
    # -------------------------------------------------------------
    def _update_cache(self, base: str, rates: Dict[str, float], source: str):
        now_ts = time.time()
        self._last_updated_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self._memory_cache[base] = {
            "rates": rates,
            "fetched_at": now_ts,
            "last_updated": self._last_updated_str,
            "source": source
        }
        self._save_disk_cache()

    def _save_disk_cache(self):
        try:
            with open(self._cache_file_path, "w", encoding="utf-8") as f:
                json.dump(self._memory_cache, f, indent=2)
        except Exception:
            # Silently pass on read-only serverless runtimes
            pass

    def _load_disk_cache(self):
        if os.path.exists(self._cache_file_path):
            try:
                with open(self._cache_file_path, "r", encoding="utf-8") as f:
                    self._memory_cache = json.load(f)
                    if self._memory_cache:
                        first_base = next(iter(self._memory_cache))
                        self._last_updated_str = self._memory_cache[first_base].get("last_updated", "Cached")
                        self._last_fetch_source = f"Cached ({self._last_updated_str})"
            except Exception:
                self._memory_cache = {}

    def _derive_from_disk_cache(self, base: str) -> Optional[Dict[str, float]]:
        """If we have cached rates for USD or another base, derive base rates using cross-rates."""
        if not self._memory_cache:
            return None

        # Direct match in disk cache
        if base in self._memory_cache:
            return self._memory_cache[base]["rates"]

        # If base is not directly cached, use USD or another available base to calculate cross rates:
        # Rate(Base -> X) = Rate(Ref -> X) / Rate(Ref -> Base)
        for ref_base, ref_data in self._memory_cache.items():
            ref_rates = ref_data.get("rates", {})
            if base in ref_rates and ref_rates[base] > 0:
                base_to_ref_rate = 1.0 / ref_rates[base]
                derived_rates = {}
                for curr, rate in ref_rates.items():
                    derived_rates[curr] = rate * base_to_ref_rate
                derived_rates[base] = 1.0
                return derived_rates

        return None

    def _emergency_fallback_rates(self, base: str) -> Dict[str, float]:
        """Hardcoded standard approximate rates so the app ALWAYS works even on fresh install with no internet."""
        usd_rates = {
            "USD": 1.0,
            "EUR": 0.92,
            "GBP": 0.79,
            "INR": 83.35,
            "JPY": 154.20,
            "AUD": 1.52,
            "CAD": 1.37,
            "CHF": 0.89,
            "CNY": 7.24,
            "AED": 3.67,
            "SGD": 1.35,
            "SAR": 3.75,
            "QAR": 3.64,
            "KRW": 1365.0,
            "BRL": 5.15,
            "RUB": 92.5,
            "NZD": 1.66,
            "ZAR": 18.6,
            "MXN": 16.9,
            "HKD": 7.82,
        }
        self._is_offline = True
        self._last_fetch_source = "Offline Baseline"
        self._last_updated_str = "Default Reference"
        if base == "USD":
            return usd_rates
        elif base in usd_rates and usd_rates[base] > 0:
            scale = 1.0 / usd_rates[base]
            return {c: r * scale for c, r in usd_rates.items()}
        return {base: 1.0, "USD": 1.0}

    # -------------------------------------------------------------
    # Conversion Logic
    # -------------------------------------------------------------
    def convert(self, amount: float, from_curr: str, to_curr: str) -> Dict:
        """
        Converts an amount from one currency to another.
        Returns:
            {
                "success": bool,
                "amount": float,
                "from_curr": str,
                "to_curr": str,
                "result": float,
                "rate": float,
                "inverse_rate": float,
                "source": str,
                "is_offline": bool,
                "error": str (if any)
            }
        """
        from_curr = from_curr.upper().strip()
        to_curr = to_curr.upper().strip()

        if from_curr == to_curr:
            return {
                "success": True,
                "amount": amount,
                "from_curr": from_curr,
                "to_curr": to_curr,
                "result": amount,
                "rate": 1.0,
                "inverse_rate": 1.0,
                "source": self._last_fetch_source,
                "is_offline": self._is_offline,
                "error": None
            }

        rates = self.fetch_rates(from_curr)
        if to_curr not in rates:
            # Fallback cross-rate via USD
            usd_rates = self.fetch_rates("USD")
            if from_curr in usd_rates and to_curr in usd_rates and usd_rates[from_curr] > 0:
                rate = usd_rates[to_curr] / usd_rates[from_curr]
            else:
                return {
                    "success": False,
                    "error": f"Currency code '{to_curr}' not found in exchange data."
                }
        else:
            rate = rates[to_curr]

        result = amount * rate
        inverse_rate = 1.0 / rate if rate > 0 else 0.0

        return {
            "success": True,
            "amount": amount,
            "from_curr": from_curr,
            "to_curr": to_curr,
            "result": result,
            "rate": rate,
            "inverse_rate": inverse_rate,
            "source": self._last_fetch_source,
            "is_offline": self._is_offline,
            "error": None
        }

    def convert_multiple(self, amount: float, from_curr: str, to_currencies: List[str]) -> List[Dict]:
        """
        Converts amount from from_curr to multiple target currencies.
        Returns a list of conversion results for each target currency.
        """
        from_curr = from_curr.upper().strip()
        rates = self.fetch_rates(from_curr)
        results = []

        for target in to_currencies:
            target = target.upper().strip()
            if target == from_curr:
                rate = 1.0
            elif target in rates:
                rate = rates[target]
            else:
                # try cross rate via USD
                usd_rates = self.fetch_rates("USD")
                if from_curr in usd_rates and target in usd_rates and usd_rates[from_curr] > 0:
                    rate = usd_rates[target] / usd_rates[from_curr]
                else:
                    rate = None

            if rate is not None:
                converted_val = amount * rate
                results.append({
                    "to_curr": target,
                    "amount": amount,
                    "result": converted_val,
                    "rate": rate,
                    "inverse_rate": (1.0 / rate) if rate > 0 else 0.0
                })

        return results
