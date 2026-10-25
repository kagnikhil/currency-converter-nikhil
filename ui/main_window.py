"""
ui/main_window.py
Minimal, clean desktop window for Currency Converter.
"""

import threading
import customtkinter as ctk
from tkinter import messagebox

from currency_service import CurrencyService
from ui.single_converter import SingleConverter
from ui.multi_converter import MultiConverter
from ui.matrix_view import MatrixView


class MainWindow(ctk.CTk):
    def __init__(self, currency_service: CurrencyService):
        super().__init__()
        self.service = currency_service

        # Configure Window
        self.title("Currency Converter")
        self.geometry("900x680")
        self.minsize(800, 600)

        # Clean default appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.current_theme = "dark"
        self._build_ui()
        self._update_status_bar()

    def _build_ui(self):
        # ---------------- 1. Clean Header Bar ----------------
        header_bar = ctk.CTkFrame(self, height=56, corner_radius=0, fg_color=("#f1f5f9", "#18181b"))
        header_bar.pack(fill="x", side="top")

        brand_frame = ctk.CTkFrame(header_bar, fg_color="transparent")
        brand_frame.pack(side="left", padx=20, pady=10)

        title_lbl = ctk.CTkLabel(
            brand_frame,
            text="Currency Converter",
            font=ctk.CTkFont(size=17, weight="bold"),
            text_color=("#0f172a", "#f4f4f5")
        )
        title_lbl.pack(side="left")

        self.status_badge = ctk.CTkLabel(
            brand_frame,
            text="• Live rates",
            font=ctk.CTkFont(size=12),
            text_color="#10b981"
        )
        self.status_badge.pack(side="left", padx=12)

        # Right Controls
        controls_frame = ctk.CTkFrame(header_bar, fg_color="transparent")
        controls_frame.pack(side="right", padx=20, pady=10)

        self.sync_btn = ctk.CTkButton(
            controls_frame,
            text="Sync",
            width=65,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color=("#e2e8f0", "#27272a"),
            text_color=("#0f172a", "#f4f4f5"),
            hover_color=("#cbd5e1", "#3f3f46"),
            command=self.refresh_all_rates
        )
        self.sync_btn.pack(side="left", padx=(0, 8))

        self.theme_btn = ctk.CTkButton(
            controls_frame,
            text="Light",
            width=65,
            height=28,
            font=ctk.CTkFont(size=12),
            fg_color=("#e2e8f0", "#27272a"),
            text_color=("#0f172a", "#f4f4f5"),
            hover_color=("#cbd5e1", "#3f3f46"),
            command=self.toggle_theme
        )
        self.theme_btn.pack(side="left")

        # ---------------- 2. Main Tab View ----------------
        self.tabview = ctk.CTkTabview(self, corner_radius=10)
        self.tabview.pack(fill="both", expand=True, padx=20, pady=(10, 10))

        tab_single = self.tabview.add("Convert")
        tab_multi = self.tabview.add("Multi-Currency")
        tab_matrix = self.tabview.add("Live Rates")

        # Single Converter
        self.single_view = SingleConverter(
            tab_single,
            currency_service=self.service
        )
        self.single_view.pack(fill="both", expand=True)

        # Multi Converter (5+ currencies)
        self.multi_view = MultiConverter(
            tab_multi,
            currency_service=self.service
        )
        self.multi_view.pack(fill="both", expand=True)

        # Rate Matrix
        self.matrix_view = MatrixView(
            tab_matrix,
            currency_service=self.service
        )
        self.matrix_view.pack(fill="both", expand=True)

        # ---------------- 3. Minimal Footer ----------------
        footer_bar = ctk.CTkFrame(self, height=26, corner_radius=0, fg_color=("#f1f5f9", "#18181b"))
        footer_bar.pack(fill="x", side="bottom")

        self.footer_left = ctk.CTkLabel(
            footer_bar,
            text="Open Exchange Rates • 166 Currencies",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        )
        self.footer_left.pack(side="left", padx=16, pady=3)

    def toggle_theme(self):
        if self.current_theme == "dark":
            ctk.set_appearance_mode("light")
            self.current_theme = "light"
            self.theme_btn.configure(text="Dark")
        else:
            ctk.set_appearance_mode("dark")
            self.current_theme = "dark"
            self.theme_btn.configure(text="Light")

    def refresh_all_rates(self):
        self.sync_btn.configure(text="Syncing...", state="disabled")
        threading.Thread(target=self._run_global_sync, daemon=True).start()

    def _run_global_sync(self):
        try:
            self.service.fetch_rates("USD", force_refresh=True)
        except Exception:
            pass
        self.after(0, self._on_sync_complete)

    def _on_sync_complete(self):
        self.sync_btn.configure(text="Sync", state="normal")
        self._update_status_bar()
        self.single_view.do_convert()
        self.multi_view.do_convert()
        self.matrix_view.load_matrix(force=False)
        messagebox.showinfo("Updated", "Rates synchronized successfully.")

    def _update_status_bar(self):
        if self.service.is_offline:
            self.status_badge.configure(
                text=f"• Offline ({self.service.last_updated})",
                text_color="#f59e0b"
            )
        else:
            self.status_badge.configure(
                text="• Live rates",
                text_color="#10b981"
            )
        self.after(15000, self._update_status_bar)
