# 🌐 Currency Converter — Python Project

A minimal, clean Currency Converter application built with **Python 3**, featuring both a **Browser Web App (Flask)** and a **Desktop GUI (CustomTkinter)**. Designed with a clean, high-clarity interface inspired by modern fintech products (Wise/Linear), without visual clutter.

---

## 🌟 Key Features

1. **Free Live Exchange Rate API (No Key & High Free Limits)**:
   - Primary: **Open Exchange Rates API** (`open.er-api.com`) supporting **166+ world currencies**.
   - Automatic cascade fallback to **Frankfurter (European Central Bank)** and **JSDelivr Currency CDN**.
   - Requires **no API keys or signups**, offering high free limits ideal for academic demonstrations.

2. **Multi-Currency Converter (5+ Currencies Simultaneously)**:
   - Convert 1 base currency to multiple target currencies in a single click.
   - Quick presets: **Global Majors**, **Asia & Gulf**, **Europe**, **Americas**, and **Study Abroad**.
   - Dynamic target list with clean real-time rate updates and removal options.

3. **Single Currency Converter**:
   - Real-time conversion as you type.
   - Interactive swap button (`⇄`) to invert source and target currencies.
   - Live exchange rate and reciprocal breakdown (`1 USD = X` and `1 X = Y USD`).

4. **160+ Currencies Search & Picker**:
   - Clean, searchable dropdown/dialog across 166 currencies by code, country, or name.

5. **Offline Fallback Architecture**:
   - Automatically caches rate matrices locally in `cache/rates_cache.json`.
   - If offline or disconnected from Wi-Fi, the app seamlessly switches to offline mode with cross-rate calculation.

6. **Minimal & Clean Aesthetic (Dark & Light Mode)**:
   - Refined, high-contrast, uncluttered typography.
   - Single-click Dark Mode and Light Mode toggle.

---

## 📁 Project Structure

```
nikhilphthon/
│
├── web_app.py               # Web application server (localhost)
├── app.py                   # Desktop GUI entry point
├── currency_service.py      # Core service handling REST API, fallbacks, caching, & math
├── currency_data.py         # 160+ currency metadata (names, symbols, flags, presets)
├── requirements.txt         # Dependencies list
├── README.md                # Project documentation and viva Q&A
│
├── templates/
│   └── index.html           # Minimal web layout
│
├── static/
│   ├── css/
│   │   └── style.css        # Clean, minimal design system
│   └── js/
│       └── app.js           # Reactive frontend conversion logic
│
├── ppt/                     # College Presentation (7-Slide Deck)
│   ├── index.html           # Interactive HTML presentation (Light theme)
│   ├── generate_pptx.py     # Script to generate PowerPoint presentation
│   └── currency_converter_presentation.pptx # Generated 7-slide PowerPoint file
│
├── ui/                      # Desktop GUI Components (CustomTkinter)
│   ├── __init__.py
│   ├── main_window.py       # Main window layout
│   ├── single_converter.py  # Single converter tab
│   ├── multi_converter.py   # Multi-currency tab
│   ├── matrix_view.py       # Live currency exchange rate table
│   └── currency_dialog.py   # Searchable currency selector popup
│
└── cache/
    └── rates_cache.json     # Auto-generated offline rate storage
```

---

## 🚀 How to Run the Project

### Option A: Web Application on Localhost (Browser)
Run the web server:
```bash
python3 web_app.py
```
- App: 👉 **[http://localhost:5001](http://localhost:5001)**
- Presentation Slides: 👉 **[http://localhost:5001/ppt](http://localhost:5001/ppt)**

---

### Option B: Native Desktop GUI App
Run the desktop GUI application:
```bash
python3 app.py
```

---

### Option C: View / Present the Slides
- **In Browser (Interactive HTML)**: Open [`ppt/index.html`](file:///Users/nikhilkag/Downloads/nikhilphthon/ppt/index.html) or navigate to `http://localhost:5001/ppt`.
- **In Microsoft PowerPoint**: Open [`ppt/currency_converter_presentation.pptx`](file:///Users/nikhilkag/Downloads/nikhilphthon/ppt/currency_converter_presentation.pptx).
- **Export to PDF**: Click the **"Export to PDF"** button on the bottom right of the HTML slide deck or press `Cmd+P` / `Ctrl+P`.

---

## 🏗️ Architecture & Mathematical Formulae

### Cross-Rate Computation Formula
When calculating exchange rates between two non-base currencies (e.g., Currency $A$ to Currency $B$) using reference currency $USD$:
$$\text{Rate}(A \to B) = \frac{\text{Rate}(USD \to B)}{\text{Rate}(USD \to A)}$$

$$\text{Converted Amount} = \text{Amount} \times \text{Rate}(A \to B)$$

$$\text{Inverse Rate} = \frac{1}{\text{Rate}(A \to B)}$$

---

## 🎓 Viva Voce & Oral Exam Questions & Answers

**Q1: Which API does your project use, and how did you handle rate limits?**
> **Answer**: We use the free public endpoint of Open Exchange Rates (`https://open.er-api.com/v6/latest/USD`), which requires no API key and provides live rates for 166 currencies without restrictive quotas. Additionally, we implemented a 2-level fallback to Frankfurter (European Central Bank) and local JSON caching.

**Q2: Why did you use `threading` in the GUI?**
> **Answer**: GUI frameworks like Tkinter run on a single-threaded main event loop. If a network HTTP request takes 1-2 seconds, running it on the main thread would freeze the entire window. By offloading API calls to `threading.Thread` (daemon threads) and posting results back using `after()`, the user interface stays completely responsive.

**Q3: How does the application work if there is no internet connection?**
> **Answer**: The application includes a persistent caching mechanism (`cache/rates_cache.json`). Every successful API fetch updates this disk cache. If an internet outage occurs, `CurrencyService` detects the network exception and reads the latest saved rates, computing any currency pair using cross-rate mathematics.

**Q4: How does the Multi-Currency Converter work?**
> **Answer**: The user specifies a base currency and an amount. The `convert_multiple()` method fetches the base currency's exchange rates and computes conversions for all selected target currencies in parallel, dynamically rendering formatted cards with symbols, flags, and reciprocal rates.

---
Developed as a Python Mini Project for College Submission.
