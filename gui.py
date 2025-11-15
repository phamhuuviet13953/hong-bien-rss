#!/usr/bin/env python3
"""
Hong Bien RSS Tool - GUI Application
Giao diện đồ họa cho RSS to Telegram bot
"""

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, scrolledtext
import json
import os
import threading
import queue
import asyncio
import logging
from datetime import datetime
from typing import Optional
import sys

# Import bot modules
import rss_telegram

# Cấu hình CustomTkinter
ctk.set_appearance_mode("dark")  # Modes: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Themes: "blue" (default), "green", "dark-blue"

CONFIG_FILE = "config.json"

class TextHandler(logging.Handler):
    """Handler để ghi logs vào text widget"""
    def __init__(self, text_widget, log_queue):
        super().__init__()
        self.text_widget = text_widget
        self.log_queue = log_queue

    def emit(self, record):
        msg = self.format(record)
        self.log_queue.put(msg)

class HongBienRSSGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Cấu hình cửa sổ chính
        self.title("Hong Bien RSS Tool")
        self.geometry("900x700")

        # Icon (nếu có)
        try:
            self.iconbitmap("icon.ico")
        except:
            pass

        # Biến trạng thái
        self.bot_running = False
        self.bot_thread = None
        self.config = self.load_config()
        self.log_queue = queue.Queue()
        self.stats = {"sent": 0, "errors": 0}

        # Setup UI
        self.setup_ui()

        # Setup logging
        self.setup_logging()

        # Start log updater
        self.update_logs()

        # Protocol khi đóng cửa sổ
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def load_config(self):
        """Load cấu hình từ file"""
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass

        # Config mặc định
        return {
            "telegram": {
                "bot_token": "",
                "chat_id": ""
            },
            "feeds": [],
            "settings": {
                "poll_interval": 90,
                "db_path": "rss_state.sqlite3"
            }
        }

    def save_config(self):
        """Lưu cấu hình vào file"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            return True
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu cấu hình: {e}")
            return False

    def setup_ui(self):
        """Thiết lập giao diện"""

        # ===== HEADER =====
        header_frame = ctk.CTkFrame(self, height=80, corner_radius=0)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            header_frame,
            text="📰 Hong Bien RSS Tool",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=20)

        # ===== MAIN CONTENT =====
        main_frame = ctk.CTkFrame(self, corner_radius=0)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Tabview
        self.tabview = ctk.CTkTabview(main_frame)
        self.tabview.pack(fill="both", expand=True)

        # Tạo tabs
        self.tabview.add("⚙️ Cấu hình")
        self.tabview.add("📊 Monitor")
        self.tabview.add("ℹ️ Thông tin")

        # Setup các tabs
        self.setup_config_tab()
        self.setup_monitor_tab()
        self.setup_info_tab()

        # ===== CONTROL PANEL =====
        control_frame = ctk.CTkFrame(self, height=100)
        control_frame.pack(fill="x", padx=10, pady=10)
        control_frame.pack_propagate(False)

        # Status
        self.status_label = ctk.CTkLabel(
            control_frame,
            text="⚪ Chưa chạy",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.status_label.pack(pady=5)

        # Buttons
        button_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=5)

        self.start_button = ctk.CTkButton(
            button_frame,
            text="▶️ Bắt đầu",
            command=self.start_bot,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="green",
            hover_color="darkgreen"
        )
        self.start_button.pack(side="left", padx=5, expand=True)

        self.stop_button = ctk.CTkButton(
            button_frame,
            text="⏹️ Dừng",
            command=self.stop_bot,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="red",
            hover_color="darkred",
            state="disabled"
        )
        self.stop_button.pack(side="left", padx=5, expand=True)

        # Stats
        stats_frame = ctk.CTkFrame(control_frame, fg_color="transparent")
        stats_frame.pack(fill="x", padx=20, pady=5)

        self.stats_label = ctk.CTkLabel(
            stats_frame,
            text="Đã gửi: 0 | Lỗi: 0",
            font=ctk.CTkFont(size=12)
        )
        self.stats_label.pack()

    def setup_config_tab(self):
        """Tab cấu hình"""
        tab = self.tabview.tab("⚙️ Cấu hình")

        # Scrollable frame
        scroll_frame = ctk.CTkScrollableFrame(tab)
        scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # ===== TELEGRAM CONFIG =====
        telegram_frame = ctk.CTkFrame(scroll_frame)
        telegram_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            telegram_frame,
            text="📱 Cấu hình Telegram",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=10, pady=10)

        # Bot Token
        ctk.CTkLabel(telegram_frame, text="Bot Token:", anchor="w").pack(fill="x", padx=10, pady=(5,0))
        self.token_entry = ctk.CTkEntry(
            telegram_frame,
            placeholder_text="123456789:ABCdefGHIjklMNOpqrsTUVwxyz",
            show="*"
        )
        self.token_entry.pack(fill="x", padx=10, pady=(0,10))
        self.token_entry.insert(0, self.config["telegram"].get("bot_token", ""))

        # Show/Hide token button
        show_token_btn = ctk.CTkButton(
            telegram_frame,
            text="👁️ Hiện/Ẩn Token",
            command=self.toggle_token_visibility,
            width=150,
            height=30,
            font=ctk.CTkFont(size=12)
        )
        show_token_btn.pack(padx=10, pady=(0,10))

        # Chat ID
        ctk.CTkLabel(telegram_frame, text="Chat ID:", anchor="w").pack(fill="x", padx=10, pady=(5,0))
        self.chatid_entry = ctk.CTkEntry(
            telegram_frame,
            placeholder_text="-1001234567890 hoặc @channel_username"
        )
        self.chatid_entry.pack(fill="x", padx=10, pady=(0,10))
        self.chatid_entry.insert(0, self.config["telegram"].get("chat_id", ""))

        # Test Connection
        test_btn = ctk.CTkButton(
            telegram_frame,
            text="🔍 Test kết nối Telegram",
            command=self.test_telegram_connection,
            width=200,
            height=35,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        test_btn.pack(padx=10, pady=(0,10))

        # ===== RSS FEEDS =====
        feeds_frame = ctk.CTkFrame(scroll_frame)
        feeds_frame.pack(fill="both", expand=True, padx=10, pady=10)

        ctk.CTkLabel(
            feeds_frame,
            text="📰 RSS Feeds",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=10, pady=10)

        # Feed list
        self.feeds_textbox = ctk.CTkTextbox(feeds_frame, height=150)
        self.feeds_textbox.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Load feeds
        feeds_text = "\n".join(self.config.get("feeds", []))
        self.feeds_textbox.insert("1.0", feeds_text)

        ctk.CTkLabel(
            feeds_frame,
            text="💡 Mỗi dòng một RSS feed URL",
            font=ctk.CTkFont(size=11),
            text_color="gray"
        ).pack(anchor="w", padx=10, pady=(0,5))

        # ===== SETTINGS =====
        settings_frame = ctk.CTkFrame(scroll_frame)
        settings_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkLabel(
            settings_frame,
            text="⚙️ Thiết lập",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=10, pady=10)

        # Poll interval
        interval_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        interval_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(interval_frame, text="Chu kỳ quét (giây):", width=150).pack(side="left", padx=5)

        self.interval_entry = ctk.CTkEntry(interval_frame, width=100)
        self.interval_entry.pack(side="left", padx=5)
        self.interval_entry.insert(0, str(self.config["settings"].get("poll_interval", 90)))

        # ===== SAVE BUTTON =====
        save_btn = ctk.CTkButton(
            scroll_frame,
            text="💾 Lưu cấu hình",
            command=self.save_config_from_ui,
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2B7A0B",
            hover_color="#1F5A08"
        )
        save_btn.pack(pady=20)

    def setup_monitor_tab(self):
        """Tab monitor"""
        tab = self.tabview.tab("📊 Monitor")

        # Logs
        ctk.CTkLabel(
            tab,
            text="📋 Logs",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(anchor="w", padx=10, pady=10)

        # Log textbox
        self.log_textbox = ctk.CTkTextbox(tab, font=ctk.CTkFont(family="Courier", size=11))
        self.log_textbox.pack(fill="both", expand=True, padx=10, pady=(0,10))

        # Buttons
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)

        clear_btn = ctk.CTkButton(
            btn_frame,
            text="🗑️ Xóa logs",
            command=self.clear_logs,
            width=120
        )
        clear_btn.pack(side="left", padx=5)

        auto_scroll_var = ctk.BooleanVar(value=True)
        auto_scroll_check = ctk.CTkCheckBox(
            btn_frame,
            text="Auto-scroll",
            variable=auto_scroll_var
        )
        auto_scroll_check.pack(side="left", padx=20)
        self.auto_scroll_var = auto_scroll_var

    def setup_info_tab(self):
        """Tab thông tin"""
        tab = self.tabview.tab("ℹ️ Thông tin")

        info_frame = ctk.CTkScrollableFrame(tab)
        info_frame.pack(fill="both", expand=True, padx=10, pady=10)

        info_text = """
        🔧 Hong Bien RSS Tool
        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        📌 Phiên bản: 2.0.0 (GUI Edition)

        📝 Mô tả:
        Tool tự động gửi bài viết mới từ RSS feeds
        vào Telegram channel/group của bạn.

        ✨ Tính năng:
        • Giao diện đồ họa dễ sử dụng
        • Hỗ trợ nhiều RSS feeds
        • Chống trùng lặp bài viết
        • Tự động retry khi lỗi
        • Dark/Light mode
        • Real-time monitoring

        🔗 Hướng dẫn:

        1️⃣ Cấu hình Telegram:
           - Lấy Bot Token từ @BotFather
           - Lấy Chat ID từ nhóm/kênh

        2️⃣ Thêm RSS Feeds:
           - WordPress: domain.com/feed/
           - YouTube: youtube.com/feeds/...
           - Facebook: Dùng RSS Bridge

        3️⃣ Lưu cấu hình và bấm Bắt đầu!

        ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

        👨‍💻 Developer: @phamhuuviet13953
        📦 GitHub: github.com/phamhuuviet13953/hong-bien-rss
        📄 License: MIT

        💡 Cần trợ giúp?
        Xem README.md hoặc mở issue trên GitHub
        """

        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        info_label.pack(padx=20, pady=20)

        # Theme switcher
        theme_frame = ctk.CTkFrame(info_frame)
        theme_frame.pack(fill="x", padx=20, pady=10)

        ctk.CTkLabel(
            theme_frame,
            text="🎨 Giao diện:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=10, pady=5)

        theme_options = ["Dark", "Light", "System"]
        self.theme_var = ctk.StringVar(value="Dark")

        for theme in theme_options:
            ctk.CTkRadioButton(
                theme_frame,
                text=theme,
                variable=self.theme_var,
                value=theme,
                command=self.change_theme
            ).pack(anchor="w", padx=30, pady=2)

    def toggle_token_visibility(self):
        """Toggle hiển thị token"""
        if self.token_entry.cget("show") == "*":
            self.token_entry.configure(show="")
        else:
            self.token_entry.configure(show="*")

    def test_telegram_connection(self):
        """Test kết nối Telegram"""
        token = self.token_entry.get().strip()
        chat_id = self.chatid_entry.get().strip()

        if not token or not chat_id:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập Bot Token và Chat ID!")
            return

        # TODO: Implement actual test
        messagebox.showinfo("Test", f"Testing connection...\nToken: {token[:20]}...\nChat ID: {chat_id}")

    def save_config_from_ui(self):
        """Lưu cấu hình từ UI"""
        try:
            # Get values
            token = self.token_entry.get().strip()
            chat_id = self.chatid_entry.get().strip()
            feeds_text = self.feeds_textbox.get("1.0", "end-1c").strip()
            feeds = [f.strip() for f in feeds_text.split("\n") if f.strip()]

            try:
                interval = int(self.interval_entry.get().strip())
                if interval < 10:
                    messagebox.showwarning("Cảnh báo", "Chu kỳ quét phải >= 10 giây!")
                    return
            except ValueError:
                messagebox.showerror("Lỗi", "Chu kỳ quét phải là số!")
                return

            # Update config
            self.config["telegram"]["bot_token"] = token
            self.config["telegram"]["chat_id"] = chat_id
            self.config["feeds"] = feeds
            self.config["settings"]["poll_interval"] = interval

            # Save
            if self.save_config():
                messagebox.showinfo("Thành công", "✅ Đã lưu cấu hình!")
                self.log_message("✅ Cấu hình đã được lưu thành công")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu cấu hình: {e}")

    def change_theme(self):
        """Đổi theme"""
        theme = self.theme_var.get()
        ctk.set_appearance_mode(theme)
        self.log_message(f"🎨 Đã đổi theme sang: {theme}")

    def setup_logging(self):
        """Setup logging handler"""
        # Create custom handler
        self.log_handler = TextHandler(self.log_textbox, self.log_queue)
        self.log_handler.setFormatter(
            logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
        )

        # Get root logger
        root_logger = logging.getLogger()
        root_logger.addHandler(self.log_handler)
        root_logger.setLevel(logging.INFO)

    def log_message(self, message):
        """Thêm message vào log"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_msg = f"[{timestamp}] {message}\n"
        self.log_queue.put(log_msg)

    def update_logs(self):
        """Update logs từ queue"""
        try:
            while True:
                msg = self.log_queue.get_nowait()
                self.log_textbox.insert("end", msg)

                # Auto scroll
                if self.auto_scroll_var.get():
                    self.log_textbox.see("end")
        except queue.Empty:
            pass

        # Schedule next update
        self.after(100, self.update_logs)

    def clear_logs(self):
        """Xóa logs"""
        self.log_textbox.delete("1.0", "end")
        self.log_message("📋 Logs đã được xóa")

    def update_status(self, status_text, color="gray"):
        """Cập nhật status"""
        icon = {
            "gray": "⚪",
            "green": "🟢",
            "red": "🔴",
            "yellow": "🟡"
        }.get(color, "⚪")

        self.status_label.configure(text=f"{icon} {status_text}")

    def update_stats(self):
        """Cập nhật thống kê"""
        self.stats_label.configure(
            text=f"Đã gửi: {self.stats['sent']} | Lỗi: {self.stats['errors']}"
        )

    def start_bot(self):
        """Bắt đầu bot"""
        if self.bot_running:
            messagebox.showinfo("Thông báo", "Bot đang chạy!")
            return

        # Validate config
        if not os.path.exists(CONFIG_FILE):
            messagebox.showwarning("Cảnh báo", "Chưa có cấu hình! Vui lòng lưu cấu hình trước.")
            return

        # Start bot in thread
        self.bot_running = True
        self.bot_thread = threading.Thread(target=self.run_bot, daemon=True)
        self.bot_thread.start()

        # Update UI
        self.start_button.configure(state="disabled")
        self.stop_button.configure(state="normal")
        self.update_status("Đang chạy", "green")
        self.log_message("🚀 Bot đã được khởi động")

    def stop_bot(self):
        """Dừng bot"""
        if not self.bot_running:
            return

        self.bot_running = False

        # Update UI
        self.start_button.configure(state="normal")
        self.stop_button.configure(state="disabled")
        self.update_status("Đã dừng", "red")
        self.log_message("⏹️ Bot đã được dừng")

    def run_bot(self):
        """Chạy bot (trong thread riêng)"""
        try:
            # Reload config
            rss_telegram.config = rss_telegram.load_config()
            rss_telegram.BOT_TOKEN = rss_telegram.config["telegram"]["bot_token"]
            rss_telegram.CHAT_ID = rss_telegram.config["telegram"]["chat_id"]
            rss_telegram.FEEDS = rss_telegram.config.get("feeds", [])
            rss_telegram.POLL_INTERVAL = rss_telegram.config["settings"].get("poll_interval", 90)

            # Validate
            rss_telegram.validate_config()

            # Run async main
            asyncio.run(self.bot_main_loop())

        except Exception as e:
            self.log_message(f"❌ Lỗi: {e}")
            self.stats["errors"] += 1
            self.update_stats()
            self.stop_bot()

    async def bot_main_loop(self):
        """Bot main loop"""
        async with rss_telegram.open_db() as db:
            async with rss_telegram.httpx.AsyncClient(
                follow_redirects=True,
                headers={"User-Agent": "rss-telegram/2.0"}
            ) as session:
                while self.bot_running:
                    tasks = [
                        rss_telegram.process_feed(db, session, url)
                        for url in rss_telegram.FEEDS
                    ]
                    await asyncio.gather(*tasks)

                    # Update stats (simplified - would need actual implementation)
                    self.after(0, self.update_stats)

                    # Wait
                    for _ in range(rss_telegram.POLL_INTERVAL):
                        if not self.bot_running:
                            break
                        await asyncio.sleep(1)

    def on_closing(self):
        """Xử lý khi đóng cửa sổ"""
        if self.bot_running:
            if messagebox.askokcancel("Thoát", "Bot đang chạy. Bạn có muốn dừng và thoát?"):
                self.stop_bot()
                self.destroy()
        else:
            self.destroy()

def main():
    """Main function"""
    app = HongBienRSSGUI()
    app.mainloop()

if __name__ == "__main__":
    main()
