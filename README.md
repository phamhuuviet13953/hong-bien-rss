# 📰 Hong Bien RSS Tool

Tool tự động gửi bài viết mới từ RSS feed (WordPress, blog, Facebook...) vào Telegram channel/group của bạn.

## ✨ Tính năng

- 🔄 Tự động quét RSS feeds theo chu kỳ
- 🚫 Chống trùng lặp (không gửi bài đã gửi)
- ⚡ Tối ưu băng thông với ETag/Last-Modified
- 💾 Lưu trạng thái với SQLite
- 🔁 Tự động retry khi lỗi mạng
- 📝 Cấu hình dễ dàng qua giao diện CLI

## 📋 Yêu cầu

- Python 3.8 trở lên
- Telegram Bot Token
- Chat ID của nhóm/kênh Telegram

## 🚀 Cài đặt nhanh

### 1. Clone repository

```bash
git clone https://github.com/phamhuuviet13953/hong-bien-rss.git
cd hong-bien-rss
```

### 2. Tạo virtual environment (khuyến nghị)

```bash
# Linux/Mac
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình tool

```bash
python setup.py
```

Làm theo hướng dẫn trên màn hình để:
- Nhập Bot Token
- Nhập Chat ID
- Thêm RSS feeds

### 5. Chạy bot

```bash
python rss_telegram.py
```

Bot sẽ chạy liên tục và tự động gửi bài viết mới vào Telegram.

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

## 📚 Cấu trúc project

```
hong-bien-rss/
├── rss_telegram.py       # Bot chính
├── setup.py              # Script cấu hình
├── requirements.txt      # Dependencies
├── config.json.example   # Template cấu hình
├── config.json           # Cấu hình (git ignored)
├── rss_state.sqlite3     # Database (git ignored)
├── Dockerfile            # Docker build
├── .gitignore           # Git ignore rules
└── README.md            # File này
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
