"""
currency_data.py
Provides comprehensive metadata for world currencies including code, name, symbol, flag emoji, and presets.
"""

CURRENCY_INFO = {
    "USD": {"name": "US Dollar", "symbol": "$", "flag": "🇺🇸", "country": "United States"},
    "EUR": {"name": "Euro", "symbol": "€", "flag": "🇪🇺", "country": "Eurozone"},
    "INR": {"name": "Indian Rupee", "symbol": "₹", "flag": "🇮🇳", "country": "India"},
    "GBP": {"name": "British Pound", "symbol": "£", "flag": "🇬🇧", "country": "United Kingdom"},
    "JPY": {"name": "Japanese Yen", "symbol": "¥", "flag": "🇯🇵", "country": "Japan"},
    "AUD": {"name": "Australian Dollar", "symbol": "A$", "flag": "🇦🇺", "country": "Australia"},
    "CAD": {"name": "Canadian Dollar", "symbol": "C$", "flag": "🇨🇦", "country": "Canada"},
    "CHF": {"name": "Swiss Franc", "symbol": "CHF", "flag": "🇨🇭", "country": "Switzerland"},
    "CNY": {"name": "Chinese Yuan", "symbol": "¥", "flag": "🇨🇳", "country": "China"},
    "AED": {"name": "UAE Dirham", "symbol": "د.إ", "flag": "🇦🇪", "country": "United Arab Emirates"},
    "SGD": {"name": "Singapore Dollar", "symbol": "S$", "flag": "🇸🇬", "country": "Singapore"},
    "NZD": {"name": "New Zealand Dollar", "symbol": "NZ$", "flag": "🇳🇿", "country": "New Zealand"},
    "SAR": {"name": "Saudi Riyal", "symbol": "﷼", "flag": "🇸🇦", "country": "Saudi Arabia"},
    "QAR": {"name": "Qatari Riyal", "symbol": "QR", "flag": "🇶🇦", "country": "Qatar"},
    "KWD": {"name": "Kuwaiti Dinar", "symbol": "KD", "flag": "🇰🇼", "country": "Kuwait"},
    "BHD": {"name": "Bahraini Dinar", "symbol": "BD", "flag": "🇧🇭", "country": "Bahrain"},
    "OMR": {"name": "Omani Rial", "symbol": "RO", "flag": "🇴🇲", "country": "Oman"},
    "KRW": {"name": "South Korean Won", "symbol": "₩", "flag": "🇰🇷", "country": "South Korea"},
    "BRL": {"name": "Brazilian Real", "symbol": "R$", "flag": "🇧🇷", "country": "Brazil"},
    "RUB": {"name": "Russian Ruble", "symbol": "₽", "flag": "🇷🇺", "country": "Russia"},
    "ZAR": {"name": "South African Rand", "symbol": "R", "flag": "🇿🇦", "country": "South Africa"},
    "MXN": {"name": "Mexican Peso", "symbol": "Mex$", "flag": "🇲🇽", "country": "Mexico"},
    "HKD": {"name": "Hong Kong Dollar", "symbol": "HK$", "flag": "🇭🇰", "country": "Hong Kong"},
    "SEK": {"name": "Swedish Krona", "symbol": "kr", "flag": "🇸🇪", "country": "Sweden"},
    "NOK": {"name": "Norwegian Krone", "symbol": "kr", "flag": "🇳🇴", "country": "Norway"},
    "DKK": {"name": "Danish Krone", "symbol": "kr", "flag": "🇩🇰", "country": "Denmark"},
    "PLN": {"name": "Polish Zloty", "symbol": "zł", "flag": "🇵🇱", "country": "Poland"},
    "TRY": {"name": "Turkish Lira", "symbol": "₺", "flag": "🇹🇷", "country": "Turkey"},
    "THB": {"name": "Thai Baht", "symbol": "฿", "flag": "🇹🇭", "country": "Thailand"},
    "IDR": {"name": "Indonesian Rupiah", "symbol": "Rp", "flag": "🇮🇩", "country": "Indonesia"},
    "MYR": {"name": "Malaysian Ringgit", "symbol": "RM", "flag": "🇲🇾", "country": "Malaysia"},
    "PHP": {"name": "Philippine Peso", "symbol": "₱", "flag": "🇵🇭", "country": "Philippines"},
    "ILS": {"name": "Israeli Shekel", "symbol": "₪", "flag": "🇮🇱", "country": "Israel"},
    "EGP": {"name": "Egyptian Pound", "symbol": "E£", "flag": "🇪🇬", "country": "Egypt"},
    "PKR": {"name": "Pakistani Rupee", "symbol": "₨", "flag": "🇵🇰", "country": "Pakistan"},
    "BDT": {"name": "Bangladeshi Taka", "symbol": "৳", "flag": "🇧🇩", "country": "Bangladesh"},
    "LKR": {"name": "Sri Lankan Rupee", "symbol": "Rs", "flag": "🇱🇰", "country": "Sri Lanka"},
    "NPR": {"name": "Nepalese Rupee", "symbol": "₨", "flag": "🇳🇵", "country": "Nepal"},
    "VND": {"name": "Vietnamese Dong", "symbol": "₫", "flag": "🇻🇳", "country": "Vietnam"},
    "CZK": {"name": "Czech Koruna", "symbol": "Kč", "flag": "🇨🇿", "country": "Czech Republic"},
    "HUF": {"name": "Hungarian Forint", "symbol": "Ft", "flag": "🇭🇺", "country": "Hungary"},
    "RON": {"name": "Romanian Leu", "symbol": "lei", "flag": "🇷🇴", "country": "Romania"},
    "BGN": {"name": "Bulgarian Lev", "symbol": "лв", "flag": "🇧🇬", "country": "Bulgaria"},
    "ARS": {"name": "Argentine Peso", "symbol": "$", "flag": "🇦🇷", "country": "Argentina"},
    "CLP": {"name": "Chilean Peso", "symbol": "$", "flag": "🇨🇱", "country": "Chile"},
    "COP": {"name": "Colombian Peso", "symbol": "$", "flag": "🇨🇴", "country": "Colombia"},
    "PEN": {"name": "Peruvian Sol", "symbol": "S/.", "flag": "🇵🇪", "country": "Peru"},
    "KZT": {"name": "Kazakhstani Tenge", "symbol": "₸", "flag": "🇰🇿", "country": "Kazakhstan"},
    "UAH": {"name": "Ukrainian Hryvnia", "symbol": "₴", "flag": "🇺🇦", "country": "Ukraine"},
    "NGN": {"name": "Nigerian Naira", "symbol": "₦", "flag": "🇳🇬", "country": "Nigeria"},
    "KES": {"name": "Kenyan Shilling", "symbol": "KSh", "flag": "🇰🇪", "country": "Kenya"},
    "GHS": {"name": "Ghanaian Cedi", "symbol": "GH₵", "flag": "🇬🇭", "country": "Ghana"},
    "MAD": {"name": "Moroccan Dirham", "symbol": "MAD", "flag": "🇲🇦", "country": "Morocco"},
    "JOD": {"name": "Jordanian Dinar", "symbol": "JD", "flag": "🇯🇴", "country": "Jordan"},
    "OMR": {"name": "Omani Rial", "symbol": "RO", "flag": "🇴🇲", "country": "Oman"},
    "TWD": {"name": "New Taiwan Dollar", "symbol": "NT$", "flag": "🇹🇼", "country": "Taiwan"},
    "ISK": {"name": "Icelandic Krona", "symbol": "kr", "flag": "🇮🇸", "country": "Iceland"},
    "RSD": {"name": "Serbian Dinar", "symbol": "din", "flag": "🇷🇸", "country": "Serbia"},
    "BAM": {"name": "Bosnia Convertible Mark", "symbol": "KM", "flag": "🇧🇦", "country": "Bosnia"},
    "ALL": {"name": "Albanian Lek", "symbol": "L", "flag": "🇦🇱", "country": "Albania"},
    "AMD": {"name": "Armenian Dram", "symbol": "֏", "flag": "🇦🇲", "country": "Armenia"},
    "AZN": {"name": "Azerbaijani Manat", "symbol": "₼", "flag": "🇦🇿", "country": "Azerbaijan"},
    "GEL": {"name": "Georgian Lari", "symbol": "₾", "flag": "🇬🇪", "country": "Georgia"},
    "MDL": {"name": "Moldovan Leu", "symbol": "L", "flag": "🇲🇩", "country": "Moldova"},
    "MKD": {"name": "Macedonian Denar", "symbol": "ден", "flag": "🇲🇰", "country": "North Macedonia"},
    "UZS": {"name": "Uzbekistani Som", "symbol": "soʻm", "flag": "🇺🇿", "country": "Uzbekistan"},
    "DZD": {"name": "Algerian Dinar", "symbol": "DA", "flag": "🇩🇿", "country": "Algeria"},
    "TND": {"name": "Tunisian Dinar", "symbol": "DT", "flag": "🇹🇳", "country": "Tunisia"},
    "LYD": {"name": "Libyan Dinar", "symbol": "LD", "flag": "🇱🇾", "country": "Libya"},
    "UGX": {"name": "Ugandan Shilling", "symbol": "USh", "flag": "🇺🇬", "country": "Uganda"},
    "TZS": {"name": "Tanzanian Shilling", "symbol": "TSh", "flag": "🇹🇿", "country": "Tanzania"},
    "ETB": {"name": "Ethiopian Birr", "symbol": "Br", "flag": "🇪🇹", "country": "Ethiopia"},
    "MZN": {"name": "Mozambican Metical", "symbol": "MT", "flag": "🇲🇿", "country": "Mozambique"},
    "BWP": {"name": "Botswanan Pula", "symbol": "P", "flag": "🇧🇼", "country": "Botswana"},
    "NAD": {"name": "Namibian Dollar", "symbol": "N$", "flag": "🇳🇦", "country": "Namibia"},
    "MUR": {"name": "Mauritian Rupee", "symbol": "₨", "flag": "🇲🇺", "country": "Mauritius"},
    "BOB": {"name": "Bolivian Boliviano", "symbol": "Bs.", "flag": "🇧🇴", "country": "Bolivia"},
    "CRC": {"name": "Costa Rican Colon", "symbol": "₡", "flag": "🇨🇷", "country": "Costa Rica"},
    "DOP": {"name": "Dominican Peso", "symbol": "RD$", "flag": "🇩🇴", "country": "Dominican Republic"},
    "GTQ": {"name": "Guatemalan Quetzal", "symbol": "Q", "flag": "🇬🇹", "country": "Guatemala"},
    "HNL": {"name": "Honduran Lempira", "symbol": "L", "flag": "🇭🇳", "country": "Honduras"},
    "NIO": {"name": "Nicaraguan Cordoba", "symbol": "C$", "flag": "🇳🇮", "country": "Nicaragua"},
    "PAB": {"name": "Panamanian Balboa", "symbol": "B/.", "flag": "🇵🇦", "country": "Panama"},
    "PYG": {"name": "Paraguayan Guarani", "symbol": "₲", "flag": "🇵🇾", "country": "Paraguay"},
    "UYU": {"name": "Uruguayan Peso", "symbol": "$U", "flag": "🇺🇾", "country": "Uruguay"},
    "JMD": {"name": "Jamaican Dollar", "symbol": "J$", "flag": "🇯🇲", "country": "Jamaica"},
    "TTD": {"name": "Trinidad Dollar", "symbol": "TT$", "flag": "🇹🇹", "country": "Trinidad and Tobago"},
    "BBD": {"name": "Barbadian Dollar", "symbol": "Bds$", "flag": "🇧🇧", "country": "Barbados"},
    "BSD": {"name": "Bahamian Dollar", "symbol": "B$", "flag": "🇧🇸", "country": "Bahamas"},
    "BZD": {"name": "Belize Dollar", "symbol": "BZ$", "flag": "🇧🇿", "country": "Belize"},
    "FJD": {"name": "Fijian Dollar", "symbol": "FJ$", "flag": "🇫🇯", "country": "Fiji"},
    "MVR": {"name": "Maldivian Rufiyaa", "symbol": "Rf", "flag": "🇲🇻", "country": "Maldives"},
    "AFN": {"name": "Afghan Afghani", "symbol": "؋", "flag": "🇦🇫", "country": "Afghanistan"},
    "IQD": {"name": "Iraqi Dinar", "symbol": "ع.د", "flag": "🇮🇶", "country": "Iraq"},
    "IRR": {"name": "Iranian Rial", "symbol": "﷼", "flag": "🇮🇷", "country": "Iran"},
    "LBP": {"name": "Lebanese Pound", "symbol": "L£", "flag": "🇱🇧", "country": "Lebanon"},
    "SYP": {"name": "Syrian Pound", "symbol": "£S", "flag": "🇸🇾", "country": "Syria"},
    "YER": {"name": "Yemeni Rial", "symbol": "﷼", "flag": "🇾🇪", "country": "Yemen"},
}

# Popular Presets for Multi-Currency Conversion
PRESETS = {
    "Global Majors": ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD"],
    "Asia & Gulf": ["INR", "AED", "SAR", "SGD", "JPY", "CNY", "QAR"],
    "Europe": ["EUR", "GBP", "CHF", "SEK", "NOK", "DKK", "PLN"],
    "Americas": ["USD", "CAD", "BRL", "MXN", "ARS", "CLP", "COP"],
    "Student / Study Abroad": ["USD", "GBP", "EUR", "CAD", "AUD", "INR"],
}

def get_currency_display_str(code: str) -> str:
    """Returns a formatted string like '🇺🇸 USD - US Dollar ($)'"""
    info = CURRENCY_INFO.get(code)
    if info:
        return f"{info['flag']} {code} - {info['name']} ({info['symbol']})"
    return f"🌐 {code}"

def get_currency_short_label(code: str) -> str:
    """Returns a short formatted string like '🇺🇸 USD ($)'"""
    info = CURRENCY_INFO.get(code)
    if info:
        return f"{info['flag']} {code} ({info['symbol']})"
    return f"🌐 {code}"

def get_currency_symbol(code: str) -> str:
    """Returns the currency symbol or the code itself"""
    info = CURRENCY_INFO.get(code)
    return info["symbol"] if info else code

def get_currency_name(code: str) -> str:
    """Returns full name of currency"""
    info = CURRENCY_INFO.get(code)
    return info["name"] if info else code

def get_currency_flag(code: str) -> str:
    """Returns flag emoji for currency"""
    info = CURRENCY_INFO.get(code)
    return info["flag"] if info else "🌐"
