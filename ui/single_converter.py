"""
ui/single_converter.py
Modern single currency converter view with instant conversion, swap animation,
quick-amount pills, live exchange rate pills, and copy to clipboard.
"""

import threading
import customtkinter as ctk
from tkinter import messagebox
from typing import Callable, Optional

from currency_service import CurrencyService
from currency_data import (
    CURRENCY_INFO,
    get_currency_display_str,
    get_currency_flag,
    get_currency_name,
    get_currency_symbol,
)
from ui.currency_dialog import CurrencySelectDialog


class SingleConverter(ctk.CTkFrame):
    def __init__(self, parent, currency_service: CurrencyService, on_history_log: Optional[Callable] = None, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self.service = currency_service
        self.on_history_log = on_history_log

        self.from_currency = "USD"
        self.to_currency = "INR"
        self._is_converting = False

        self._build_ui()
        # Trigger initial conversion
        self.after(300, self.do_convert)

    def _build_ui(self):
        # Center container
        center_box = ctk.CTkFrame(self, fg_color="transparent")
        center_box.pack(fill="both", expand=True, padx=25, pady=15)

        # ---------------- Top: Amount Input & Quick Presets ----------------
        input_card = ctk.CTkFrame(center_box, corner_radius=14)
        input_card.pack(fill="x", pady=(0, 15), ipady=10)

        amt_label = ctk.CTkLabel(
            input_card,
            text="💵 Enter Amount to Convert",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        amt_label.pack(anchor="w", padx=20, pady=(10, 5))

        entry_row = ctk.CTkFrame(input_card, fg_color="transparent")
        entry_row.pack(fill="x", padx=20, pady=(0, 10))

        self.currency_symbol_lbl = ctk.CTkLabel(
            entry_row,
            text="$",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#3b82f6",
            width=30
        )
        self.currency_symbol_lbl.pack(side="left", padx=(0, 10))

        self.amount_entry = ctk.CTkEntry(
            entry_row,
            placeholder_text="Enter amount (e.g. 100)",
            height=48,
            font=ctk.CTkFont(size=20, weight="bold"),
            corner_radius=10
        )
        self.amount_entry.pack(side="left", fill="x", expand=True)
        self.amount_entry.insert(0, "100")
        self.amount_entry.bind("<KeyRelease>", self._on_amount_key)

        # Quick Add Pills
        pills_row = ctk.CTkFrame(input_card, fg_color="transparent")
        pills_row.pack(fill="x", padx=20, pady=(5, 5))

        ctk.CTkLabel(pills_row, text="Quick Add:", font=ctk.CTkFont(size=12), text_color="gray").pack(side="left", padx=(0, 8))

        for add_val in [10, 50, 100, 500, 1000]:
            btn = ctk.CTkButton(
                pills_row,
                text=f"+{add_val}",
                width=55,
                height=26,
                font=ctk.CTkFont(size=11),
                fg_color=("#e2e8f0", "#334155"),
                text_color=("#1e293b", "#f8fafc"),
                hover_color=("#cbd5e1", "#475569"),
                command=lambda v=add_val: self._add_to_amount(v)
            )
            btn.pack(side="left", padx=3)

        reset_btn = ctk.CTkButton(
            pills_row,
            text="Reset",
            width=55,
            height=26,
            font=ctk.CTkFont(size=11),
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self._reset_amount
        )
        reset_btn.pack(side="right")

        # ---------------- Middle: From & To Currencies with Swap ----------------
        selector_card = ctk.CTkFrame(center_box, corner_radius=14)
        selector_card.pack(fill="x", pady=(0, 15), ipady=8)

        cols_frame = ctk.CTkFrame(selector_card, fg_color="transparent")
        cols_frame.pack(fill="x", padx=20, pady=12)

        # FROM Box
        from_box = ctk.CTkFrame(cols_frame, corner_radius=10, fg_color=("#f1f5f9", "#1e293b"))
        from_box.pack(side="left", fill="both", expand=True, padx=(0, 10), pady=4, ipady=8)

        ctk.CTkLabel(from_box, text="FROM CURRENCY", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=12, pady=(6, 2))
        
        self.from_display_lbl = ctk.CTkLabel(
            from_box,
            text=f"{get_currency_flag(self.from_currency)}  {self.from_currency}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.from_display_lbl.pack(anchor="w", padx=12, pady=(0, 2))

        self.from_name_lbl = ctk.CTkLabel(
            from_box,
            text=get_currency_name(self.from_currency),
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.from_name_lbl.pack(anchor="w", padx=12, pady=(0, 6))

        change_from_btn = ctk.CTkButton(
            from_box,
            text="🔍 Select Currency",
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self._open_from_picker
        )
        change_from_btn.pack(fill="x", padx=12, pady=(0, 4))

        # SWAP Button
        swap_btn = ctk.CTkButton(
            cols_frame,
            text="⇄",
            width=46,
            height=46,
            font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="#6366f1",
            hover_color="#4f46e5",
            corner_radius=23,
            command=self.swap_currencies
        )
        swap_btn.pack(side="left", padx=5)

        # TO Box
        to_box = ctk.CTkFrame(cols_frame, corner_radius=10, fg_color=("#f1f5f9", "#1e293b"))
        to_box.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=4, ipady=8)

        ctk.CTkLabel(to_box, text="TO CURRENCY", font=ctk.CTkFont(size=11, weight="bold"), text_color="gray").pack(anchor="w", padx=12, pady=(6, 2))

        self.to_display_lbl = ctk.CTkLabel(
            to_box,
            text=f"{get_currency_flag(self.to_currency)}  {self.to_currency}",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.to_display_lbl.pack(anchor="w", padx=12, pady=(0, 2))

        self.to_name_lbl = ctk.CTkLabel(
            to_box,
            text=get_currency_name(self.to_currency),
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.to_name_lbl.pack(anchor="w", padx=12, pady=(0, 6))

        change_to_btn = ctk.CTkButton(
            to_box,
            text="🔍 Select Currency",
            height=30,
            font=ctk.CTkFont(size=12),
            fg_color="#10b981",
            hover_color="#059669",
            command=self._open_to_picker
        )
        change_to_btn.pack(fill="x", padx=12, pady=(0, 4))

        # ---------------- Bottom: Big Result Card ----------------
        self.result_card = ctk.CTkFrame(center_box, corner_radius=14, fg_color=("#f8fafc", "#0f172a"), border_width=2, border_color="#3b82f6")
        self.result_card.pack(fill="both", expand=True, ipady=12)

        self.res_subhead = ctk.CTkLabel(
            self.result_card,
            text="CONVERTED TOTAL",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color="gray"
        )
        self.res_subhead.pack(pady=(12, 2))

        self.result_amount_lbl = ctk.CTkLabel(
            self.result_card,
            text="--",
            font=ctk.CTkFont(size=34, weight="bold"),
            text_color="#10b981"
        )
        self.result_amount_lbl.pack(pady=4)

        # Exchange rate details
        self.rates_pill_frame = ctk.CTkFrame(self.result_card, fg_color="transparent")
        self.rates_pill_frame.pack(pady=6)

        self.rate_info_lbl = ctk.CTkLabel(
            self.rates_pill_frame,
            text="Exchange Rate: --",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#38bdf8"
        )
        self.rate_info_lbl.pack()

        self.inverse_rate_lbl = ctk.CTkLabel(
            self.rates_pill_frame,
            text="Inverse Rate: --",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.inverse_rate_lbl.pack(pady=(2, 0))

        # Action Buttons under Result
        actions_row = ctk.CTkFrame(self.result_card, fg_color="transparent")
        actions_row.pack(pady=(10, 10))

        self.convert_btn = ctk.CTkButton(
            actions_row,
            text="⚡ Convert Now",
            width=140,
            height=36,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self.do_convert
        )
        self.convert_btn.pack(side="left", padx=6)

        self.copy_btn = ctk.CTkButton(
            actions_row,
            text="📋 Copy Result",
            width=120,
            height=36,
            font=ctk.CTkFont(size=13),
            fg_color=("#cbd5e1", "#334155"),
            text_color=("#0f172a", "#f8fafc"),
            hover_color=("#94a3b8", "#475569"),
            command=self._copy_result
        )
        self.copy_btn.pack(side="left", padx=6)

    # -------------------------------------------------------------
    # UI Event Handlers
    # -------------------------------------------------------------
    def _add_to_amount(self, value: int):
        try:
            cur = float(self.amount_entry.get().replace(",", "").strip())
        except ValueError:
            cur = 0.0
        new_val = cur + value
        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, f"{new_val:g}")
        self.do_convert()

    def _reset_amount(self):
        self.amount_entry.delete(0, "end")
        self.amount_entry.insert(0, "1")
        self.do_convert()

    def _on_amount_key(self, event=None):
        # Auto convert after small delay or enter
        if event and event.keysym == "Return":
            self.do_convert()
        else:
            self.after(400, self._auto_convert_check)

    def _auto_convert_check(self):
        # Trigger conversion if amount is valid
        try:
            val = float(self.amount_entry.get().replace(",", "").strip())
            if val >= 0:
                self.do_convert()
        except ValueError:
            pass

    def swap_currencies(self):
        self.from_currency, self.to_currency = self.to_currency, self.from_currency
        self._update_currency_cards()
        self.do_convert()

    def _open_from_picker(self):
        CurrencySelectDialog(
            self.winfo_toplevel(),
            on_select=self._set_from_currency,
            title="Select Source Currency (FROM)",
            current_code=self.from_currency
        )

    def _open_to_picker(self):
        CurrencySelectDialog(
            self.winfo_toplevel(),
            on_select=self._set_to_currency,
            title="Select Target Currency (TO)",
            current_code=self.to_currency
        )

    def _set_from_currency(self, code: str):
        self.from_currency = code
        self._update_currency_cards()
        self.do_convert()

    def _set_to_currency(self, code: str):
        self.to_currency = code
        self._update_currency_cards()
        self.do_convert()

    def _update_currency_cards(self):
        self.currency_symbol_lbl.configure(text=get_currency_symbol(self.from_currency))
        self.from_display_lbl.configure(text=f"{get_currency_flag(self.from_currency)}  {self.from_currency}")
        self.from_name_lbl.configure(text=get_currency_name(self.from_currency))
        self.to_display_lbl.configure(text=f"{get_currency_flag(self.to_currency)}  {self.to_currency}")
        self.to_name_lbl.configure(text=get_currency_name(self.to_currency))

    def _copy_result(self):
        res_text = self.result_amount_lbl.cget("text")
        if res_text and res_text != "--":
            self.clipboard_clear()
            self.clipboard_append(res_text)
            messagebox.showinfo("Copied", f"Copied: {res_text}")

    # -------------------------------------------------------------
    # Async Conversion Execution
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
            self.result_amount_lbl.configure(text="Invalid Amount", text_color="#ef4444")
            return

        self._is_converting = True
        self.convert_btn.configure(text="⏳ Converting...", state="disabled")

        # Run conversion in background thread so UI stays fluid
        threading.Thread(
            target=self._run_conversion_thread,
            args=(amount, self.from_currency, self.to_currency),
            daemon=True
        ).start()

    def _run_conversion_thread(self, amount: float, from_curr: str, to_curr: str):
        res = self.service.convert(amount, from_curr, to_curr)
        # Schedule UI update on main thread
        self.after(0, self._apply_conversion_result, res)

    def _apply_conversion_result(self, res: dict):
        self._is_converting = False
        self.convert_btn.configure(text="⚡ Convert Now", state="normal")

        if not res.get("success"):
            self.result_amount_lbl.configure(text="Conversion Failed", text_color="#ef4444")
            self.rate_info_lbl.configure(text=res.get("error", "Error fetching rate"))
            return

        to_sym = get_currency_symbol(res["to_curr"])
        to_flag = get_currency_flag(res["to_curr"])
        converted = res["result"]
        rate = res["rate"]
        inv_rate = res["inverse_rate"]

        # Format number with commas and 2 to 4 decimal places
        if converted >= 1000:
            formatted_val = f"{converted:,.2f}"
        elif converted >= 1:
            formatted_val = f"{converted:,.4f}".rstrip("0").rstrip(".")
        else:
            formatted_val = f"{converted:,.6f}".rstrip("0").rstrip(".")

        self.result_amount_lbl.configure(
            text=f"{to_flag} {to_sym} {formatted_val} {res['to_curr']}",
            text_color="#10b981"
        )

        from_flag = get_currency_flag(res["from_curr"])
        self.rate_info_lbl.configure(
            text=f"1 {res['from_curr']} = {rate:,.4f} {res['to_curr']}"
        )
        self.inverse_rate_lbl.configure(
            text=f"1 {res['to_curr']} = {inv_rate:,.4f} {res['from_curr']}"
        )

        # Log to history
        if self.on_history_log:
            self.on_history_log(
                from_curr=res["from_curr"],
                to_curr=res["to_curr"],
                from_amt=res["amount"],
                to_amt=converted,
                rate=rate
            )
