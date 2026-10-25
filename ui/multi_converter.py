"""
ui/multi_converter.py
Multi-currency converter allowing simultaneous conversion from 1 base currency
to 5+ target currencies with instant preset filters, dynamic currency cards,
custom currency adding/removal, and one-click bulk copy.
"""

import threading
import customtkinter as ctk
from tkinter import messagebox
from typing import List, Callable, Optional

from currency_service import CurrencyService
from currency_data import (
    PRESETS,
    get_currency_display_str,
    get_currency_flag,
    get_currency_name,
    get_currency_symbol,
)
from ui.currency_dialog import CurrencySelectDialog


class MultiConverter(ctk.CTkFrame):
    def __init__(self, parent, currency_service: CurrencyService, on_history_log: Optional[Callable] = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.service = currency_service
        self.on_history_log = on_history_log

        self.base_currency = "USD"
        # Default 6 global currencies
        self.target_currencies: List[str] = ["EUR", "GBP", "INR", "JPY", "AUD", "CAD"]
        self._is_converting = False

        self._build_ui()
        self.after(350, self.do_convert)

    def _build_ui(self):
        # Main layout: Top control bar + Scrollable cards area
        top_bar = ctk.CTkFrame(self, corner_radius=14)
        top_bar.pack(fill="x", padx=15, pady=(10, 12), ipady=6)

        # Base Currency & Amount row
        row1 = ctk.CTkFrame(top_bar, fg_color="transparent")
        row1.pack(fill="x", padx=15, pady=8)

        # Base Currency selector button
        base_box = ctk.CTkFrame(row1, fg_color=("#e2e8f0", "#1e293b"), corner_radius=10)
        base_box.pack(side="left", padx=(0, 10))

        ctk.CTkLabel(base_box, text="BASE CURRENCY", font=ctk.CTkFont(size=10, weight="bold"), text_color="gray").pack(anchor="w", padx=10, pady=(4, 0))

        self.base_btn = ctk.CTkButton(
            base_box,
            text=f"{get_currency_flag(self.base_currency)} {self.base_currency} ▾",
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color="transparent",
            hover_color=("#cbd5e1", "#334155"),
            text_color=("#0f172a", "#38bdf8"),
            height=32,
            command=self._open_base_picker
        )
        self.base_btn.pack(padx=6, pady=(0, 4))

        # Amount Input
        amt_box = ctk.CTkFrame(row1, fg_color="transparent")
        amt_box.pack(side="left", fill="x", expand=True, padx=5)

        ctk.CTkLabel(amt_box, text="AMOUNT TO CONVERT", font=ctk.CTkFont(size=10, weight="bold"), text_color="gray").pack(anchor="w", padx=4, pady=(0, 2))

        self.amount_entry = ctk.CTkEntry(
            amt_box,
            placeholder_text="Amount",
            height=38,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=8
        )
        self.amount_entry.pack(fill="x")
        self.amount_entry.insert(0, "100")
        self.amount_entry.bind("<KeyRelease>", self._on_amount_key)

        # Refresh / Convert Button
        self.convert_btn = ctk.CTkButton(
            row1,
            text="⚡ Calculate All",
            width=120,
            height=38,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self.do_convert
        )
        self.convert_btn.pack(side="left", padx=(10, 0), pady=(14, 0))

        # Copy All Button
        self.copy_all_btn = ctk.CTkButton(
            row1,
            text="📋 Copy All",
            width=100,
            height=38,
            font=ctk.CTkFont(size=13),
            fg_color=("#cbd5e1", "#334155"),
            text_color=("#0f172a", "#f8fafc"),
            hover_color=("#94a3b8", "#475569"),
            command=self._copy_all_results
        )
        self.copy_all_btn.pack(side="left", padx=5, pady=(14, 0))

        # Row 2: Presets & Add Button
        row2 = ctk.CTkFrame(top_bar, fg_color="transparent")
        row2.pack(fill="x", padx=15, pady=(4, 6))

        ctk.CTkLabel(row2, text="Presets:", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(side="left", padx=(0, 6))

        for preset_name, preset_list in PRESETS.items():
            p_btn = ctk.CTkButton(
                row2,
                text=preset_name,
                height=26,
                font=ctk.CTkFont(size=11),
                fg_color=("#e2e8f0", "#1e293b"),
                hover_color=("#cbd5e1", "#334155"),
                text_color=("#0f172a", "#f8fafc"),
                command=lambda p=preset_list: self._apply_preset(p)
            )
            p_btn.pack(side="left", padx=3)

        # Add Currency Button
        add_btn = ctk.CTkButton(
            row2,
            text="➕ Add Currency",
            height=26,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#10b981",
            hover_color="#059669",
            command=self._open_add_target_picker
        )
        add_btn.pack(side="right", padx=2)

        # Scrollable area for dynamic currency cards
        self.cards_scroll = ctk.CTkScrollableFrame(self, corner_radius=14)
        self.cards_scroll.pack(fill="both", expand=True, padx=15, pady=(0, 10))

    # -------------------------------------------------------------
    # Event Handlers & Presets
    # -------------------------------------------------------------
    def _open_base_picker(self):
        CurrencySelectDialog(
            self.winfo_toplevel(),
            on_select=self._set_base_currency,
            title="Select Base Currency",
            current_code=self.base_currency
        )

    def _set_base_currency(self, code: str):
        self.base_currency = code
        self.base_btn.configure(text=f"{get_currency_flag(code)} {code} ▾")
        # Ensure base isn't also in target list
        if code in self.target_currencies:
            self.target_currencies.remove(code)
        self.do_convert()

    def _open_add_target_picker(self):
        CurrencySelectDialog(
            self.winfo_toplevel(),
            on_select=self._add_target_currency,
            title="Add Target Currency"
        )

    def _add_target_currency(self, code: str):
        if code == self.base_currency:
            messagebox.showinfo("Notice", f"{code} is already the base currency.")
            return
        if code not in self.target_currencies:
            self.target_currencies.append(code)
            self.do_convert()
        else:
            messagebox.showinfo("Notice", f"{code} is already added in the list.")

    def _remove_target_currency(self, code: str):
        if code in self.target_currencies:
            self.target_currencies.remove(code)
            self.do_convert()

    def _apply_preset(self, preset_list: List[str]):
        # Filter out current base
        targets = [c for c in preset_list if c != self.base_currency]
        self.target_currencies = targets
        self.do_convert()

    def _on_amount_key(self, event=None):
        if event and event.keysym == "Return":
            self.do_convert()
        else:
            self.after(450, self.do_convert)

    # -------------------------------------------------------------
    # Async Multi-Conversion
    # -------------------------------------------------------------
    def do_convert(self):
        if self._is_converting:
            return

        amt_str = self.amount_entry.get().replace(",", "").strip()
        try:
            amount = float(amt_str)
            if amount < 0:
                raise ValueError
        except ValueError:
            return

        if not self.target_currencies:
            self._render_empty_cards()
            return

        self._is_converting = True
        self.convert_btn.configure(text="⏳ Calculating...", state="disabled")

        threading.Thread(
            target=self._run_multi_thread,
            args=(amount, self.base_currency, list(self.target_currencies)),
            daemon=True
        ).start()

    def _run_multi_thread(self, amount: float, base_curr: str, targets: List[str]):
        results = self.service.convert_multiple(amount, base_curr, targets)
        self.after(0, self._render_multi_cards, amount, base_curr, results)

    def _render_empty_cards(self):
        for w in self.cards_scroll.winfo_children():
            w.destroy()
        lbl = ctk.CTkLabel(
            self.cards_scroll,
            text="No target currencies selected.\nClick '➕ Add Currency' or select a Preset above to compare.",
            font=ctk.CTkFont(size=14),
            text_color="gray"
        )
        lbl.pack(pady=60)

    def _render_multi_cards(self, amount: float, base_curr: str, results: List[dict]):
        self._is_converting = False
        self.convert_btn.configure(text="⚡ Calculate All", state="normal")

        for w in self.cards_scroll.winfo_children():
            w.destroy()

        self._cached_results = results
        self._cached_amount = amount
        self._cached_base = base_curr

        if not results:
            self._render_empty_cards()
            return

        # Grid container (2 columns for neat responsive layout)
        grid_frame = ctk.CTkFrame(self.cards_scroll, fg_color="transparent")
        grid_frame.pack(fill="both", expand=True, padx=4, pady=4)
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)

        for i, item in enumerate(results):
            code = item["to_curr"]
            res_val = item["result"]
            rate = item["rate"]
            inv = item["inverse_rate"]

            flag = get_currency_flag(code)
            sym = get_currency_symbol(code)
            name = get_currency_name(code)

            row = i // 2
            col = i % 2

            card = ctk.CTkFrame(grid_frame, corner_radius=12, fg_color=("#f1f5f9", "#1e293b"))
            card.grid(row=row, column=col, padx=6, pady=6, sticky="nsew")

            # Header of Card (Flag + Code + Name, and Remove button)
            c_header = ctk.CTkFrame(card, fg_color="transparent")
            c_header.pack(fill="x", padx=12, pady=(10, 4))

            c_info = ctk.CTkLabel(
                c_header,
                text=f"{flag}  {code}  —  {name}",
                font=ctk.CTkFont(size=13, weight="bold"),
                anchor="w"
            )
            c_info.pack(side="left")

            # Remove (x) button
            rm_btn = ctk.CTkButton(
                c_header,
                text="✕",
                width=24,
                height=24,
                font=ctk.CTkFont(size=11, weight="bold"),
                fg_color="transparent",
                hover_color="#ef4444",
                text_color="gray",
                command=lambda c=code: self._remove_target_currency(c)
            )
            rm_btn.pack(side="right")

            # Result Amount
            if res_val >= 1000:
                fmt_res = f"{res_val:,.2f}"
            elif res_val >= 1:
                fmt_res = f"{res_val:,.4f}".rstrip("0").rstrip(".")
            else:
                fmt_res = f"{res_val:,.6f}".rstrip("0").rstrip(".")

            val_lbl = ctk.CTkLabel(
                card,
                text=f"{sym} {fmt_res}",
                font=ctk.CTkFont(size=22, weight="bold"),
                text_color="#10b981",
                anchor="w"
            )
            val_lbl.pack(fill="x", padx=12, pady=(2, 2))

            # Unit Exchange Rate
            rate_lbl = ctk.CTkLabel(
                card,
                text=f"1 {base_curr} = {rate:,.4f} {code}  |  1 {code} = {inv:,.4f} {base_curr}",
                font=ctk.CTkFont(size=11),
                text_color="gray",
                anchor="w"
            )
            rate_lbl.pack(fill="x", padx=12, pady=(0, 10))

    def _copy_all_results(self):
        if not hasattr(self, "_cached_results") or not self._cached_results:
            messagebox.showwarning("Notice", "No calculated results to copy.")
            return

        lines = [f"=== Multi-Currency Conversion: {self._cached_amount:,.2f} {self._cached_base} ==="]
        for item in self._cached_results:
            c = item["to_curr"]
            val = item["result"]
            sym = get_currency_symbol(c)
            lines.append(f"• {c} ({sym}): {val:,.2f}  [1 {self._cached_base} = {item['rate']:,.4f} {c}]")

        full_text = "\n".join(lines)
        self.clipboard_clear()
        self.clipboard_append(full_text)
        messagebox.showinfo("Copied All", f"Copied conversions for {len(self._cached_results)} currencies to clipboard!")
