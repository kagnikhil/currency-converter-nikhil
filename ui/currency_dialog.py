"""
ui/currency_dialog.py
Searchable Currency Picker Modal Dialog for CustomTkinter.
Enables rapid filtering of 160+ currencies by code, country, or currency name.
"""

import customtkinter as ctk
from typing import Callable, Optional, List
from currency_data import CURRENCY_INFO, get_currency_display_str


class CurrencySelectDialog(ctk.CTkToplevel):
    def __init__(self, parent, on_select: Callable[[str], None], title: str = "Select Currency", current_code: str = "USD"):
        super().__init__(parent)
        self.title(title)
        self.geometry("460x560")
        self.resizable(False, False)
        self.transient(parent)
        self.grab_set()

        self.on_select = on_select
        self.current_code = current_code
        self.selected_code: Optional[str] = None

        # Build list of all currencies
        self.all_currencies: List[dict] = []
        for code, info in sorted(CURRENCY_INFO.items()):
            self.all_currencies.append({
                "code": code,
                "name": info["name"],
                "symbol": info["symbol"],
                "flag": info["flag"],
                "country": info["country"],
                "search_text": f"{code} {info['name']} {info['country']} {info['symbol']}".lower()
            })

        self._build_ui()
        self._populate_list(self.all_currencies)

        # Center on parent window
        self.after(50, self._center_on_parent, parent)

    def _center_on_parent(self, parent):
        try:
            x = parent.winfo_x() + (parent.winfo_width() // 2) - 230
            y = parent.winfo_y() + (parent.winfo_height() // 2) - 280
            self.geometry(f"+{max(50, x)}+{max(50, y)}")
        except Exception:
            pass

    def _build_ui(self):
        # Header
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=20, pady=(16, 8))

        title_lbl = ctk.CTkLabel(
            header,
            text="🌍 Select Currency",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        title_lbl.pack(anchor="w")

        subtitle_lbl = ctk.CTkLabel(
            header,
            text="Search among 160+ world currencies by code, name, or country",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        subtitle_lbl.pack(anchor="w")

        # Search Bar
        search_frame = ctk.CTkFrame(self, corner_radius=10)
        search_frame.pack(fill="x", padx=20, pady=(8, 12))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="🔍 Type to search (e.g. INR, Euro, Japan, Rupee)...",
            height=38,
            font=ctk.CTkFont(size=13)
        )
        self.search_entry.pack(fill="x", padx=8, pady=8)
        self.search_entry.bind("<KeyRelease>", self._on_search)
        self.search_entry.focus()

        # Popular Quick Filter Buttons
        quick_frame = ctk.CTkFrame(self, fg_color="transparent")
        quick_frame.pack(fill="x", padx=20, pady=(0, 10))

        popular = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD", "AED"]
        for p_code in popular:
            btn = ctk.CTkButton(
                quick_frame,
                text=p_code,
                width=45,
                height=26,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="#334155" if p_code != self.current_code else "#3b82f6",
                hover_color="#475569",
                command=lambda c=p_code: self._choose_currency(c)
            )
            btn.pack(side="left", padx=2)

        # Scrollable list of currencies
        self.scroll_frame = ctk.CTkScrollableFrame(self, height=340, corner_radius=10)
        self.scroll_frame.pack(fill="both", expand=True, padx=20, pady=(0, 16))

    def _populate_list(self, currencies: List[dict]):
        # Clear existing items
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        if not currencies:
            empty_lbl = ctk.CTkLabel(
                self.scroll_frame,
                text="No matching currencies found.",
                font=ctk.CTkFont(size=13),
                text_color="gray"
            )
            empty_lbl.pack(pady=40)
            return

        for curr in currencies:
            code = curr["code"]
            is_active = (code == self.current_code)

            item_btn = ctk.CTkButton(
                self.scroll_frame,
                text=f"{curr['flag']}  {code:<5} — {curr['name']} ({curr['symbol']})",
                anchor="w",
                height=40,
                font=ctk.CTkFont(size=13, weight="bold" if is_active else "normal"),
                fg_color="#1e293b" if is_active else "transparent",
                hover_color="#334155",
                text_color="#60a5fa" if is_active else ("#f8fafc", "#0f172a"),
                command=lambda c=code: self._choose_currency(c)
            )
            item_btn.pack(fill="x", pady=2)

    def _on_search(self, event=None):
        query = self.search_entry.get().strip().lower()
        if not query:
            self._populate_list(self.all_currencies)
        else:
            filtered = [
                c for c in self.all_currencies
                if query in c["search_text"]
            ]
            self._populate_list(filtered)

    def _choose_currency(self, code: str):
        self.selected_code = code
        if self.on_select:
            self.on_select(code)
        self.destroy()
