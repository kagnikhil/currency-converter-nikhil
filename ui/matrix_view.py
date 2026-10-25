"""
ui/matrix_view.py
Live Exchange Rate Matrix & Rates Table.
Displays live rates of top world currencies against any selected base currency.
"""

import threading
import customtkinter as ctk
from typing import Dict, List
from currency_service import CurrencyService
from currency_data import (
    CURRENCY_INFO,
    get_currency_flag,
    get_currency_name,
    get_currency_symbol,
)
from ui.currency_dialog import CurrencySelectDialog


class MatrixView(ctk.CTkFrame):
    def __init__(self, parent, currency_service: CurrencyService, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.service = currency_service
        self.base_currency = "USD"
        self._all_rates: Dict[str, float] = {}

        self._build_ui()
        self.after(400, self.load_matrix)

    def _build_ui(self):
        # Top toolbar
        toolbar = ctk.CTkFrame(self, corner_radius=12)
        toolbar.pack(fill="x", padx=15, pady=(10, 12), ipady=4)

        t_row = ctk.CTkFrame(toolbar, fg_color="transparent")
        t_row.pack(fill="x", padx=12, pady=6)

        ctk.CTkLabel(
            t_row,
            text="📊 Global Rate Matrix",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(side="left")

        # Base currency switch button
        self.base_btn = ctk.CTkButton(
            t_row,
            text=f"Base: {get_currency_flag(self.base_currency)} {self.base_currency} ▾",
            width=130,
            height=32,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self._change_base
        )
        self.base_btn.pack(side="left", padx=15)

        # Refresh button
        self.refresh_btn = ctk.CTkButton(
            t_row,
            text="🔄 Refresh",
            width=90,
            height=32,
            font=ctk.CTkFont(size=12),
            fg_color=("#cbd5e1", "#334155"),
            text_color=("#0f172a", "#f8fafc"),
            hover_color=("#94a3b8", "#475569"),
            command=lambda: self.load_matrix(force=True)
        )
        self.refresh_btn.pack(side="right")

        # Search filter box
        self.search_entry = ctk.CTkEntry(
            t_row,
            placeholder_text="Filter currencies...",
            width=160,
            height=32
        )
        self.search_entry.pack(side="right", padx=10)
        self.search_entry.bind("<KeyRelease>", self._on_filter)

        # Table header
        header_frame = ctk.CTkFrame(self, height=36, corner_radius=8, fg_color=("#e2e8f0", "#1e293b"))
        header_frame.pack(fill="x", padx=15, pady=(0, 6))

        h1 = ctk.CTkLabel(header_frame, text="Currency / Country", font=ctk.CTkFont(size=12, weight="bold"), width=220, anchor="w")
        h1.pack(side="left", padx=15)

        h2 = ctk.CTkLabel(header_frame, text="Exchange Rate", font=ctk.CTkFont(size=12, weight="bold"), width=140, anchor="e")
        h2.pack(side="left", padx=10)

        h3 = ctk.CTkLabel(header_frame, text="Inverse Rate (1 Unit)", font=ctk.CTkFont(size=12, weight="bold"), width=160, anchor="e")
        h3.pack(side="left", padx=10)

        # Scrollable table body
        self.scroll_table = ctk.CTkScrollableFrame(self, corner_radius=12)
        self.scroll_table.pack(fill="both", expand=True, padx=15, pady=(0, 10))

    def _change_base(self):
        CurrencySelectDialog(
            self.winfo_toplevel(),
            on_select=self._set_base,
            title="Select Base Currency for Matrix",
            current_code=self.base_currency
        )

    def _set_base(self, code: str):
        self.base_currency = code
        self.base_btn.configure(text=f"Base: {get_currency_flag(code)} {code} ▾")
        self.load_matrix()

    def load_matrix(self, force: bool = False):
        self.refresh_btn.configure(text="⏳ Syncing...", state="disabled")
        threading.Thread(
            target=self._fetch_matrix_thread,
            args=(self.base_currency, force),
            daemon=True
        ).start()

    def _fetch_matrix_thread(self, base: str, force: bool):
        rates = self.service.fetch_rates(base, force_refresh=force)
        self.after(0, self._render_table, rates)

    def _render_table(self, rates: Dict[str, float]):
        self.refresh_btn.configure(text="🔄 Refresh", state="normal")
        self._all_rates = rates
        self._filter_and_display()

    def _on_filter(self, event=None):
        self._filter_and_display()

    def _filter_and_display(self):
        for w in self.scroll_table.winfo_children():
            w.destroy()

        query = self.search_entry.get().strip().lower()
        base = self.base_currency

        # Sort with popular currencies on top, then alphabetical
        popular_order = ["USD", "EUR", "GBP", "INR", "JPY", "AUD", "CAD", "CHF", "CNY", "AED", "SGD", "SAR", "KRW", "BRL", "MXN", "RUB", "ZAR"]
        sorted_codes = sorted(
            self._all_rates.keys(),
            key=lambda c: (0 if c in popular_order else 1, popular_order.index(c) if c in popular_order else c)
        )

        display_count = 0
        for code in sorted_codes:
            if code == base:
                continue

            rate = self._all_rates[code]
            inv = 1.0 / rate if rate > 0 else 0.0
            name = get_currency_name(code)
            flag = get_currency_flag(code)
            sym = get_currency_symbol(code)

            # Filter check
            if query:
                searchable = f"{code} {name} {sym}".lower()
                if query not in searchable:
                    continue

            display_count += 1
            row_card = ctk.CTkFrame(
                self.scroll_table,
                height=42,
                corner_radius=8,
                fg_color=("#f8fafc", "#1e293b") if display_count % 2 == 0 else ("#f1f5f9", "#0f172a")
            )
            row_card.pack(fill="x", padx=4, pady=2)

            # Col 1: Currency & Country
            c1 = ctk.CTkLabel(
                row_card,
                text=f"{flag} {code}  — {name}",
                font=ctk.CTkFont(size=12, weight="bold"),
                width=220,
                anchor="w"
            )
            c1.pack(side="left", padx=12, pady=8)

            # Col 2: Rate
            rate_fmt = f"{rate:,.4f}" if rate < 1000 else f"{rate:,.2f}"
            c2 = ctk.CTkLabel(
                row_card,
                text=f"{sym} {rate_fmt}",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color="#10b981",
                width=140,
                anchor="e"
            )
            c2.pack(side="left", padx=10, pady=8)

            # Col 3: Inverse Rate
            inv_fmt = f"{inv:,.4f}" if inv < 1000 else f"{inv:,.2f}"
            base_sym = get_currency_symbol(base)
            c3 = ctk.CTkLabel(
                row_card,
                text=f"{base_sym} {inv_fmt}",
                font=ctk.CTkFont(size=11),
                text_color="gray",
                width=160,
                anchor="e"
            )
            c3.pack(side="left", padx=10, pady=8)

        if display_count == 0:
            lbl = ctk.CTkLabel(self.scroll_table, text="No currencies match the search filter.", text_color="gray")
            lbl.pack(pady=40)
