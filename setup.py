#!/usr/bin/env python3
"""
Script cấu hình cho Hong Bien RSS Tool
Chạy script này để thiết lập bot token, chat ID và RSS feeds
"""

import json
import os
import sys

CONFIG_FILE = "config.json"
CONFIG_EXAMPLE = "config.json.example"

def clear_screen():
    """Xóa màn hình console"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """In header của tool"""
    print("=" * 60)
    print("🔧 HONG BIEN RSS TOOL - CẤU HÌNH")
    print("=" * 60)
    print()

def load_existing_config():
    """Đọc config hiện tại nếu có"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Lỗi khi đọc config cũ: {e}")

    # Nếu không có config, dùng example
    if os.path.exists(CONFIG_EXAMPLE):
        try:
            with open(CONFIG_EXAMPLE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
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

def get_input(prompt, default=None, required=True):
    """Lấy input từ người dùng"""
    if default:
        full_prompt = f"{prompt} [{default}]: "
    else:
        full_prompt = f"{prompt}: "

    while True:
        value = input(full_prompt).strip()

        if value:
            return value
        elif default:
            return default
        elif not required:
            return ""
        else:
            print("❌ Giá trị này là bắt buộc! Vui lòng nhập lại.")

def setup_telegram(config):
    """Cấu hình Telegram Bot"""
    print("\n📱 CẤU HÌNH TELEGRAM BOT")
    print("-" * 60)
    print("Hướng dẫn lấy Bot Token:")
    print("  1. Mở @BotFather trên Telegram")
    print("  2. Gửi /newbot hoặc /mybots")
    print("  3. Copy token (dạng: 123456789:ABCdefGHIjklMNOpqrsTUVwxyz)")
    print()

    current_token = config["telegram"].get("bot_token", "")
    if current_token and current_token != "YOUR_BOT_TOKEN_HERE":
        print(f"Token hiện tại: {current_token[:20]}...")

    bot_token = get_input("Nhập Bot Token", current_token if current_token != "YOUR_BOT_TOKEN_HERE" else None)

    print("\nHướng dẫn lấy Chat ID:")
    print("  1. Thêm bot vào nhóm/kênh của bạn")
    print("  2. Gửi tin nhắn bất kỳ trong nhóm")
    print("  3. Truy cập: https://api.telegram.org/bot<TOKEN>/getUpdates")
    print("     (thay <TOKEN> bằng bot token của bạn)")
    print("  4. Tìm 'chat':{'id': -1001234567890}")
    print("     Với kênh công khai có thể dùng: @your_channel")
    print()

    current_chat_id = config["telegram"].get("chat_id", "")
    if current_chat_id and current_chat_id != "YOUR_CHAT_ID_HERE":
        print(f"Chat ID hiện tại: {current_chat_id}")

    chat_id = get_input("Nhập Chat ID", current_chat_id if current_chat_id != "YOUR_CHAT_ID_HERE" else None)

    config["telegram"]["bot_token"] = bot_token
    config["telegram"]["chat_id"] = chat_id

def setup_feeds(config):
    """Cấu hình RSS feeds"""
    print("\n📰 CẤU HÌNH RSS FEEDS")
    print("-" * 60)
    print("Bạn có thể thêm:")
    print("  • RSS Feed URLs (ví dụ: https://example.com/feed/)")
    print("  • Facebook page (sẽ hướng dẫn cách lấy RSS)")
    print()

    feeds = config.get("feeds", [])

    if feeds:
        print("Feed hiện tại:")
        for i, feed in enumerate(feeds, 1):
            print(f"  {i}. {feed}")
        print()

    print("Chọn hành động:")
    print("  1. Thêm feed mới")
    print("  2. Xóa feed")
    print("  3. Xóa tất cả và nhập lại")
    print("  4. Giữ nguyên")

    choice = get_input("\nNhập lựa chọn (1-4)", "4", required=False)

    if choice == "1":
        # Thêm feed mới
        while True:
            feed_url = get_input("\nNhập RSS Feed URL (Enter để kết thúc)", required=False)
            if not feed_url:
                break

            if feed_url not in feeds:
                feeds.append(feed_url)
                print(f"✅ Đã thêm: {feed_url}")
            else:
                print(f"⚠️  Feed này đã có trong danh sách!")

    elif choice == "2":
        # Xóa feed
        if not feeds:
            print("❌ Không có feed nào để xóa!")
        else:
            try:
                idx = int(get_input("Nhập số thứ tự feed cần xóa", required=False))
                if 1 <= idx <= len(feeds):
                    removed = feeds.pop(idx - 1)
                    print(f"✅ Đã xóa: {removed}")
                else:
                    print("❌ Số thứ tự không hợp lệ!")
            except ValueError:
                print("❌ Vui lòng nhập số!")

    elif choice == "3":
        # Xóa tất cả và nhập lại
        feeds = []
        print("\n📝 Nhập danh sách feed mới (Enter để kết thúc):")
        while True:
            feed_url = get_input(f"Feed #{len(feeds) + 1}", required=False)
            if not feed_url:
                break
            feeds.append(feed_url)

    config["feeds"] = feeds

def setup_settings(config):
    """Cấu hình các thiết lập khác"""
    print("\n⚙️  CẤU HÌNH NÂNG CAO")
    print("-" * 60)

    settings = config.get("settings", {})

    current_interval = settings.get("poll_interval", 90)
    print(f"Chu kỳ quét hiện tại: {current_interval} giây")

    change = get_input("Bạn có muốn thay đổi? (y/n)", "n", required=False).lower()

    if change == 'y':
        while True:
            try:
                interval = int(get_input("Nhập chu kỳ quét (giây)", str(current_interval)))
                if interval > 0:
                    settings["poll_interval"] = interval
                    break
                else:
                    print("❌ Chu kỳ phải lớn hơn 0!")
            except ValueError:
                print("❌ Vui lòng nhập số!")

    config["settings"] = settings

def save_config(config):
    """Lưu config vào file"""
    try:
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except Exception as e:
        print(f"❌ Lỗi khi lưu config: {e}")
        return False

def show_summary(config):
    """Hiển thị tóm tắt cấu hình"""
    print("\n" + "=" * 60)
    print("📋 TÓM TẮT CẤU HÌNH")
    print("=" * 60)

    # Telegram
    bot_token = config["telegram"]["bot_token"]
    chat_id = config["telegram"]["chat_id"]
    print(f"\n📱 Telegram Bot:")
    print(f"   Token: {bot_token[:20]}...{bot_token[-10:] if len(bot_token) > 30 else ''}")
    print(f"   Chat ID: {chat_id}")

    # Feeds
    feeds = config.get("feeds", [])
    print(f"\n📰 RSS Feeds ({len(feeds)}):")
    if feeds:
        for i, feed in enumerate(feeds, 1):
            print(f"   {i}. {feed}")
    else:
        print("   (Chưa có feed nào)")

    # Settings
    settings = config.get("settings", {})
    print(f"\n⚙️  Thiết lập:")
    print(f"   Chu kỳ quét: {settings.get('poll_interval', 90)} giây")
    print(f"   Database: {settings.get('db_path', 'rss_state.sqlite3')}")
    print()

def facebook_rss_guide():
    """Hướng dẫn lấy RSS từ Facebook"""
    print("\n" + "=" * 60)
    print("📘 HƯỚNG DẪN LẤY RSS TỪ FACEBOOK PAGE")
    print("=" * 60)
    print("""
Do Facebook không cung cấp RSS trực tiếp, bạn có thể sử dụng:

1. RSS Bridge (Tự host hoặc public instance):
   • Trang chủ: https://github.com/RSS-Bridge/rss-bridge
   • Public instances: https://rss-bridge.org/bridge01/
   • Chọn "Facebook" bridge
   • Nhập username/page ID
   • Copy RSS feed URL

2. Feed43 (https://feed43.com):
   • Tạo custom RSS từ bất kỳ trang web nào
   • Free với giới hạn updates

3. Các service khác:
   • Feedwind
   • FetchRSS
   • RSS.app

Lưu ý: Facebook thường chặn các service này, có thể không ổn định!
""")
    input("\nẤn Enter để tiếp tục...")

def main():
    """Chương trình chính"""
    clear_screen()
    print_header()

    # Đọc config hiện tại
    config = load_existing_config()

    # Menu chính
    while True:
        print("\n📋 MENU CẤU HÌNH:")
        print("  1. Cấu hình Telegram Bot")
        print("  2. Quản lý RSS Feeds")
        print("  3. Cài đặt nâng cao")
        print("  4. Xem hướng dẫn Facebook RSS")
        print("  5. Xem tóm tắt cấu hình")
        print("  6. Lưu và thoát")
        print("  7. Thoát không lưu")

        choice = get_input("\nNhập lựa chọn (1-7)", "6", required=False)

        if choice == "1":
            setup_telegram(config)
        elif choice == "2":
            setup_feeds(config)
        elif choice == "3":
            setup_settings(config)
        elif choice == "4":
            facebook_rss_guide()
        elif choice == "5":
            show_summary(config)
        elif choice == "6":
            # Lưu và thoát
            show_summary(config)
            confirm = get_input("\n💾 Lưu cấu hình này? (y/n)", "y", required=False).lower()

            if confirm == 'y':
                if save_config(config):
                    print("\n✅ Đã lưu cấu hình thành công!")
                    print(f"📁 File: {CONFIG_FILE}")
                    print("\n🚀 Chạy bot bằng lệnh: python rss_telegram.py")
                    return 0
                else:
                    print("\n❌ Không thể lưu cấu hình!")
                    return 1
        elif choice == "7":
            print("\n👋 Thoát không lưu!")
            return 0
        else:
            print("❌ Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n👋 Đã hủy!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Lỗi: {e}")
        sys.exit(1)
