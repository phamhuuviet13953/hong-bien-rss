# 🔧 Troubleshooting GUI - Hong Bien RSS Tool

## ❌ Lỗi: ModuleNotFoundError: No module named 'customtkinter.windows.widgets.core_rendering'

### Nguyên nhân:
Phiên bản customtkinter không tương thích hoặc cài đặt không đúng.

### Giải pháp nhanh:

#### Windows:
```batch
fix-gui.bat
```

#### Linux/Mac:
```bash
chmod +x fix-gui.sh
./fix-gui.sh
```

Script này sẽ:
1. ✅ Gỡ cài đặt customtkinter cũ
2. ✅ Cập nhật pip
3. ✅ Cài đặt lại customtkinter==5.2.2
4. ✅ Cài đặt tất cả dependencies

### Giải pháp manual:

#### Bước 1: Activate virtual environment

**Windows:**
```batch
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

#### Bước 2: Gỡ cài đặt customtkinter cũ

```bash
pip uninstall -y customtkinter
```

#### Bước 3: Cài đặt phiên bản cụ thể

```bash
pip install --upgrade --force-reinstall customtkinter==5.2.2
```

#### Bước 4: Cài đặt các dependencies khác

```bash
pip install darkdetect Pillow
pip install -r requirements.txt
```

#### Bước 5: Xóa marker file

**Windows:**
```batch
del venv\.gui_requirements_installed
```

**Linux/Mac:**
```bash
rm venv/.gui_requirements_installed
```

#### Bước 6: Chạy lại GUI

```bash
python gui.py
```

---

## ❌ Lỗi: _tkinter.TclError hoặc không mở được GUI

### Windows:
Python từ python.org đã bao gồm Tkinter. Nếu lỗi:
1. Cài lại Python từ https://www.python.org/
2. Khi cài đặt, check vào "tcl/tk and IDLE"
3. Chạy lại setup

### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install python3-tk python3-pil python3-pil.imagetk
```

### Linux (Fedora/RHEL):
```bash
sudo dnf install python3-tkinter python3-pillow
```

### macOS:
```bash
brew install python-tk
```

Sau đó chạy lại:
```bash
./fix-gui.sh
```

---

## ❌ Lỗi: ImportError: cannot import name 'ImageTk' from 'PIL'

### Giải pháp:
```bash
# Activate venv trước
pip uninstall Pillow
pip install --upgrade Pillow
```

---

## ❌ GUI mở được nhưng hiển thị lỗi hoặc trắng màn hình

### Kiểm tra:
1. **Logs**: Xem console có báo lỗi gì không
2. **Config file**: Đảm bảo `config.json` tồn tại hoặc để GUI tạo mới
3. **Permissions**: Kiểm tra quyền ghi file

### Thử chế độ debug:
```bash
python gui.py --debug
```

---

## ❌ Bot không chạy trong GUI

### Kiểm tra:
1. ✅ Đã lưu cấu hình chưa? (Bấm "💾 Lưu cấu hình")
2. ✅ Bot Token và Chat ID đúng chưa?
3. ✅ Có RSS feeds nào được thêm chưa?
4. ✅ Xem tab "📊 Monitor" để xem logs lỗi

### Test thủ công:
```bash
# Chạy bot CLI để test
python rss_telegram.py
```

Nếu CLI chạy được → vấn đề ở GUI
Nếu CLI cũng lỗi → vấn đề ở config/bot

---

## ❌ Lỗi khác

### Thu thập thông tin:
1. **Python version**: `python --version`
2. **OS**: Windows/Linux/macOS + version
3. **Lỗi đầy đủ**: Copy toàn bộ error message
4. **Installed packages**: `pip list`

### Tạo issue:
https://github.com/phamhuuviet13953/hong-bien-rss/issues

Bao gồm:
- 📝 Mô tả lỗi
- 💻 Thông tin hệ thống
- 📋 Full error traceback
- 🔄 Các bước để reproduce

---

## ✅ Tips chung

### Tip 1: Luôn dùng virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Tip 2: Cập nhật pip trước khi cài package
```bash
python -m pip install --upgrade pip
```

### Tip 3: Force reinstall nếu có vấn đề
```bash
pip install --upgrade --force-reinstall -r requirements.txt
```

### Tip 4: Xóa venv và tạo lại nếu cần
```bash
# Backup config trước!
rm -rf venv  # Linux/Mac
rmdir /s venv  # Windows

# Tạo lại
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Tip 5: Dùng CLI nếu GUI không hoạt động
GUI là optional. Bạn vẫn có thể dùng tool với CLI:
```bash
python setup.py    # Cấu hình
python rss_telegram.py  # Chạy bot
```

---

## 📞 Cần trợ giúp thêm?

- 📖 [README.md](README.md) - Hướng dẫn đầy đủ
- ⚡ [QUICKSTART.md](QUICKSTART.md) - Hướng dẫn nhanh
- 🐛 [GitHub Issues](https://github.com/phamhuuviet13953/hong-bien-rss/issues)

---

**Happy fixing! 🔧**
