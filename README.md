# 📰 Hong Bien RSS Tool

Tool tự động gửi bài viết mới từ RSS feed (WordPress, blog, Facebook...) vào Telegram channel/group của bạn.

> 🎉 **NEW:** Phiên bản 2.0 với **Giao diện đồ họa (GUI)** hiện đại!

## ✨ Tính năng

- 🖥️ **Giao diện đồ họa dễ sử dụng** (CustomTkinter)
- 🔄 Tự động quét RSS feeds theo chu kỳ
- 🚫 Chống trùng lặp (không gửi bài đã gửi)
- ⚡ Tối ưu băng thông với ETag/Last-Modified
- 💾 Lưu trạng thái với SQLite
- 🔁 Tự động retry khi lỗi mạng
- 📊 Real-time monitoring và logs
- 🎨 Dark/Light mode
- 📝 Cấu hình dễ dàng qua GUI hoặc CLI

## 📋 Yêu cầu

- Python 3.8 trở lên
- Telegram Bot Token
- Chat ID của nhóm/kênh Telegram

## 🚀 Cài đặt nhanh

### Cách 1: Giao diện đồ họa (GUI) - Khuyến nghị ⭐

#### Linux/Mac
```bash
git clone https://github.com/phamhuuviet13953/hong-bien-rss.git
cd hong-bien-rss
chmod +x run-gui.sh
./run-gui.sh
```

#### Windows
```batch
git clone https://github.com/phamhuuviet13953/hong-bien-rss.git
cd hong-bien-rss
run-gui.bat
```

Script sẽ tự động:
- ✅ Tạo virtual environment
- ✅ Cài đặt dependencies
- ✅ Mở giao diện đồ họa

**Trong giao diện GUI:**
1. Vào tab "⚙️ Cấu hình"
2. Nhập Bot Token và Chat ID
3. Thêm RSS feeds (mỗi dòng một URL)
4. Bấm "💾 Lưu cấu hình"
5. Bấm "▶️ Bắt đầu"

### Cách 2: Giao diện dòng lệnh (CLI)

#### Linux/Mac
```bash
git clone https://github.com/phamhuuviet13953/hong-bien-rss.git
cd hong-bien-rss
./run.sh
```

#### Windows
```batch
git clone https://github.com/phamhuuviet13953/hong-bien-rss.git
cd hong-bien-rss
run.bat
```

### Cách 3: Manual (Nâng cao)

```bash
# 1. Clone repository
git clone https://github.com/phamhuuviet13953/hong-bien-rss.git
cd hong-bien-rss

# 2. Tạo virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# hoặc venv\Scripts\activate  # Windows

# 3. Cài đặt dependencies
pip install -r requirements.txt

# 4. Cấu hình (CLI)
python setup.py

# 5. Chạy
# GUI:
python gui.py
# hoặc CLI:
python rss_telegram.py
```

## 📝 Hướng dẫn chi tiết

### Lấy Telegram Bot Token

1. Mở Telegram và tìm **@BotFather**
2. Gửi lệnh `/newbot` để tạo bot mới
3. Đặt tên và username cho bot
4. Copy Bot Token (dạng: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Lấy Chat ID

#### Cách 1: Dùng getUpdates API

1. Thêm bot vào nhóm/kênh của bạn
2. Gửi tin nhắn bất kỳ trong nhóm
3. Truy cập URL:
   ```
   https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates
   ```
4. Tìm `"chat":{"id": -1001234567890}`
5. Copy số Chat ID (bao gồm dấu `-` nếu có)

#### Cách 2: Dùng bot @userinfobot

1. Thêm bot **@userinfobot** vào nhóm
2. Bot sẽ tự động gửi Chat ID
3. Copy Chat ID

#### Cách 3: Kênh công khai

Với kênh công khai, có thể dùng `@your_channel_username`

### Thêm RSS Feeds

#### RSS từ WordPress

Hầu hết blog WordPress có RSS tại:
```
https://example.com/feed/
https://example.com/rss/
https://example.com/wp-rss2.php
```

#### RSS từ Facebook

Do Facebook không cung cấp RSS trực tiếp, bạn có thể dùng:

**1. RSS Bridge** (Khuyến nghị)
- Tự host: https://github.com/RSS-Bridge/rss-bridge
- Public instance: https://rss-bridge.org/bridge01/
- Chọn "Facebook" bridge
- Nhập username/page ID
- Copy RSS feed URL

**2. Feed43**
- Truy cập: https://feed43.com
- Tạo custom RSS từ Facebook page

**3. RSS.app**
- Truy cập: https://rss.app
- Tạo RSS feed từ Facebook URL

⚠️ **Lưu ý:** Facebook thường chặn các service này, có thể không ổn định!

#### Các nguồn RSS khác

- YouTube channel: `https://www.youtube.com/feeds/videos.xml?channel_id=CHANNEL_ID`
- Reddit: `https://www.reddit.com/r/subreddit/.rss`
- Medium: `https://medium.com/feed/@username`
- Tumblr: `https://username.tumblr.com/rss`

## 🔧 Cấu hình nâng cao

### File cấu hình: `config.json`

```json
{
  "telegram": {
    "bot_token": "YOUR_BOT_TOKEN",
    "chat_id": "YOUR_CHAT_ID"
  },
  "feeds": [
    "https://example.com/feed/",
    "https://another-site.com/rss/"
  ],
  "settings": {
    "poll_interval": 90,
    "db_path": "rss_state.sqlite3"
  }
}
```

**Tham số:**
- `poll_interval`: Chu kỳ quét (giây), mặc định 90s
- `db_path`: Đường dẫn file database SQLite

### Chỉnh sửa format tin nhắn

Mở file `rss_telegram.py` và sửa hàm `format_message()`:

```python
def format_message(title: str, url: str, source: str) -> str:
    # Tùy chỉnh format ở đây
    return f"📰 <b><a href=\"{url}\">{title}</a></b>\n📌 Nguồn: <i>{source}</i>"
```

Hỗ trợ HTML tags:
- `<b>text</b>` - **Bold**
- `<i>text</i>` - *Italic*
- `<a href="url">text</a>` - Link
- `<code>text</code>` - Code

## 🖥️ Hướng dẫn sử dụng GUI

### Khởi động GUI

```bash
# Linux/Mac
./run-gui.sh

# Windows
run-gui.bat

# Hoặc trực tiếp
python gui.py
```

### Giao diện chính

GUI có 3 tab chính:

#### 1. ⚙️ Tab Cấu hình

**Cấu hình Telegram:**
- **Bot Token**: Nhập token từ @BotFather
- **Chat ID**: Nhập ID của nhóm/kênh
- **Test kết nối**: Kiểm tra cấu hình có đúng không

**RSS Feeds:**
- Thêm các RSS feed URLs (mỗi dòng một URL)
- Hỗ trợ nhiều nguồn cùng lúc

**Thiết lập:**
- **Chu kỳ quét**: Thời gian giữa các lần quét (giây)

**Lưu cấu hình:**
- Bấm "💾 Lưu cấu hình" để lưu thay đổi

#### 2. 📊 Tab Monitor

**Xem Logs real-time:**
- Hiển thị tất cả hoạt động của bot
- Tự động scroll (có thể tắt)
- Nút "🗑️ Xóa logs" để làm sạch

**Thông tin:**
- Trạng thái bot (Đang chạy/Dừng)
- Số bài đã gửi
- Số lỗi gặp phải

#### 3. ℹ️ Tab Thông tin

**Thông tin tool:**
- Phiên bản
- Hướng dẫn nhanh
- Links hữu ích

**Chuyển đổi giao diện:**
- Dark mode (mặc định)
- Light mode
- System (theo hệ thống)

### Control Panel

Ở dưới cùng của cửa sổ:

- **▶️ Bắt đầu**: Khởi động bot
- **⏹️ Dừng**: Dừng bot
- **Trạng thái**: Hiển thị trạng thái hiện tại
- **Thống kê**: Số bài đã gửi và lỗi

### Tính năng nổi bật

✅ **Show/Hide Token**: Ẩn/hiện Bot Token để bảo mật
✅ **Auto-scroll logs**: Tự động cuộn xuống log mới
✅ **Dark/Light mode**: Chuyển đổi giao diện dễ dàng
✅ **Real-time monitoring**: Xem hoạt động bot trực tiếp
✅ **Safe exit**: Xác nhận trước khi đóng khi bot đang chạy

### Shortcuts & Tips

**Tip 1**: Luôn test kết nối Telegram trước khi chạy bot
**Tip 2**: Kiểm tra logs tab để debug nếu có lỗi
**Tip 3**: Đặt chu kỳ quét >= 30 giây để tránh spam
**Tip 4**: Có thể chạy cả GUI và CLI cùng lúc (khác config)

## 🐳 Chạy với Docker

### Tạo Docker image

```bash
docker build -t hong-bien-rss .
```

### Chạy container

```bash
docker run -d \
  --name hong-bien-rss \
  -v $(pwd)/config.json:/app/config.json \
  -v $(pwd)/rss_state.sqlite3:/app/rss_state.sqlite3 \
  --restart unless-stopped \
  hong-bien-rss
```

### Xem logs

```bash
docker logs -f hong-bien-rss
```

### Dừng container

```bash
docker stop hong-bien-rss
```

## 🔄 Chạy như systemd service (Linux)

### 1. Tạo service file

```bash
sudo nano /etc/systemd/system/hong-bien-rss.service
```

Nội dung:
```ini
[Unit]
Description=Hong Bien RSS to Telegram Bot
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/hong-bien-rss
ExecStart=/path/to/venv/bin/python rss_telegram.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 2. Enable và start service

```bash
sudo systemctl daemon-reload
sudo systemctl enable hong-bien-rss
sudo systemctl start hong-bien-rss
```

### 3. Kiểm tra status

```bash
sudo systemctl status hong-bien-rss
```

### 4. Xem logs

```bash
sudo journalctl -u hong-bien-rss -f
```

## 🛠️ Troubleshooting

### Bot không gửi tin nhắn

1. Kiểm tra bot đã được thêm vào nhóm/kênh chưa
2. Với kênh, bot cần quyền **Post Messages**
3. Với nhóm riêng tư, đảm bảo Chat ID có dấu `-`
4. Chạy lại `python setup.py` để kiểm tra cấu hình

### Lỗi "403 Forbidden" từ Telegram

- Bot bị kick khỏi nhóm/kênh
- Bot không có quyền gửi tin nhắn
- Thêm lại bot và cấp quyền phù hợp

### RSS feed không hoạt động

1. Kiểm tra URL feed có đúng không (mở bằng trình duyệt)
2. Một số site chặn bot - thử thêm User-Agent khác
3. Feed có thể bị lỗi format - xem logs để biết chi tiết

### Database bị lock

Nếu chạy nhiều instance cùng lúc, SQLite có thể bị lock:
- Chỉ chạy 1 instance
- Hoặc dùng DB path khác nhau cho mỗi instance

### GUI không mở được

**Linux:**
- Cần cài đặt thêm: `sudo apt-get install python3-tk`
- Với Wayland: Thử chạy với XWayland

**macOS:**
- Cần cài đặt Tcl/Tk: `brew install python-tk`

**Windows:**
- Python từ python.org đã bao gồm Tkinter
- Nếu lỗi, cài lại Python và check "tcl/tk and IDLE"

## 📚 Cấu trúc project

```
hong-bien-rss/
├── gui.py                    # 🖥️  Giao diện đồ họa (NEW!)
├── rss_telegram.py           # 🤖 Bot chính (CLI)
├── setup.py                  # ⚙️  Script cấu hình CLI
├── run-gui.sh               # 🚀 Launcher GUI (Linux/Mac)
├── run-gui.bat              # 🚀 Launcher GUI (Windows)
├── run.sh                   # 🚀 Launcher CLI (Linux/Mac)
├── run.bat                  # 🚀 Launcher CLI (Windows)
├── create_icon.py           # 🎨 Script tạo icon
├── requirements.txt         # 📦 Dependencies
├── config.json.example      # 📝 Template cấu hình
├── config.json              # 🔒 Cấu hình (git ignored)
├── rss_state.sqlite3        # 💾 Database (git ignored)
├── Dockerfile               # 🐳 Docker build
├── docker-compose.yml       # 🐳 Docker compose
├── hong-bien-rss.desktop    # 🖼️  Linux desktop launcher
├── .gitignore              # 🚫 Git ignore rules
├── LICENSE                  # ⚖️  MIT License
├── README.md               # 📖 Hướng dẫn đầy đủ
└── QUICKSTART.md           # ⚡ Hướng dẫn nhanh
```

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Hãy:
1. Fork repository
2. Tạo branch mới (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Mở Pull Request

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết

## 🙏 Credits

- Developed by [@phamhuuviet13953](https://github.com/phamhuuviet13953)
- Powered by:
  - [feedparser](https://github.com/kurtmckee/feedparser)
  - [httpx](https://github.com/encode/httpx)
  - [aiosqlite](https://github.com/omnilib/aiosqlite)
  - [tenacity](https://github.com/jd/tenacity)

## 📞 Hỗ trợ

Nếu bạn gặp vấn đề hoặc có câu hỏi:
- Mở issue tại: https://github.com/phamhuuviet13953/hong-bien-rss/issues
- Hoặc liên hệ qua Telegram: @your_telegram

---

**Enjoy your automated RSS to Telegram bot! 🎉**
