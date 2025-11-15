# 🚀 Hướng dẫn nhanh - Quick Start

## Cài đặt trong 5 phút ⚡

### Linux / macOS

```bash
# 1. Clone repository
git clone https://github.com/phamhuuviet13953/hong-bien-rss.git
cd hong-bien-rss

# 2. Chạy script tự động
./run.sh
```

Script sẽ tự động:
- ✅ Tạo virtual environment
- ✅ Cài đặt dependencies
- ✅ Chạy wizard cấu hình
- ✅ Start bot

### Windows

```batch
# 1. Clone repository
git clone https://github.com/phamhuuviet13953/hong-bien-rss.git
cd hong-bien-rss

# 2. Double-click file run.bat
# hoặc chạy trong Command Prompt:
run.bat
```

---

## Lấy thông tin cần thiết 📝

### 1. Bot Token (2 phút)

1. Mở Telegram → Tìm **@BotFather**
2. Gửi `/newbot`
3. Đặt tên bot (ví dụ: "My RSS Bot")
4. Đặt username (ví dụ: "myrss_bot")
5. Copy token (dạng: `123456:ABCdef...`)

### 2. Chat ID (2 phút)

**Cách dễ nhất:**

1. Thêm bot vào nhóm/kênh
2. Gửi tin nhắn bất kỳ
3. Mở trình duyệt, truy cập:
   ```
   https://api.telegram.org/bot<TOKEN>/getUpdates
   ```
   (thay `<TOKEN>` bằng bot token của bạn)
4. Tìm `"chat":{"id": -1001234567890}`
5. Copy số `-1001234567890`

**Với kênh công khai:**

Chỉ cần dùng: `@your_channel`

### 3. RSS Feed URL (1 phút)

**WordPress:**
```
https://your-site.com/feed/
```

**YouTube:**
```
https://www.youtube.com/feeds/videos.xml?channel_id=UC...
```

**Facebook:**
Dùng RSS Bridge: https://rss-bridge.org/bridge01/

---

## Cấu hình 🔧

Khi chạy lần đầu, tool sẽ hỏi:

1. **Bot Token**: Paste token từ BotFather
2. **Chat ID**: Paste Chat ID của nhóm/kênh
3. **RSS Feeds**: Nhập URL feed (có thể thêm nhiều)
4. **Chu kỳ quét**: Để mặc định 90s hoặc tùy chỉnh

Xong! Tool sẽ bắt đầu chạy 🎉

---

## Chạy nền 24/7 🔄

### Docker (Khuyến nghị)

```bash
# 1. Build image
docker-compose build

# 2. Start container
docker-compose up -d

# 3. Xem logs
docker-compose logs -f
```

### Linux systemd

```bash
# Xem hướng dẫn chi tiết trong README.md
sudo systemctl enable hong-bien-rss
sudo systemctl start hong-bien-rss
```

---

## Troubleshooting 🔧

### Bot không gửi tin

- ✅ Kiểm tra bot đã trong nhóm/kênh chưa
- ✅ Bot có quyền "Post Messages" chưa
- ✅ Chat ID có dấu `-` nếu là nhóm riêng tư

### Lỗi config

```bash
# Chạy lại setup
python setup.py
```

### RSS không hoạt động

- ✅ Mở feed URL bằng browser kiểm tra
- ✅ Xem logs để biết lỗi cụ thể

---

## Cần trợ giúp? 💬

- 📖 [README.md](README.md) - Hướng dẫn đầy đủ
- 🐛 [Issues](https://github.com/phamhuuviet13953/hong-bien-rss/issues) - Báo lỗi
- 💡 [Discussions](https://github.com/phamhuuviet13953/hong-bien-rss/discussions) - Hỏi đáp

---

**Happy RSS feeding! 🎉**
