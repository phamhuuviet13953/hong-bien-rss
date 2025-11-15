#!/usr/bin/env python3
"""
Script tạo icon đơn giản cho Hong Bien RSS Tool
Yêu cầu: pip install pillow
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os

    # Tạo icon 256x256
    size = 256
    img = Image.new('RGB', (size, size), color='#1a1a2e')

    draw = ImageDraw.Draw(img)

    # Vẽ hình tròn
    circle_color = '#16213e'
    draw.ellipse([20, 20, size-20, size-20], fill=circle_color, outline='#0f3460', width=8)

    # Vẽ biểu tượng RSS (3 cung tròn)
    rss_color = '#e94560'

    # Chấm nhỏ ở góc dưới trái
    draw.ellipse([60, size-80, 80, size-60], fill=rss_color)

    # Cung 1
    draw.arc([50, size-180, 150, size-80], start=0, end=90, fill=rss_color, width=15)

    # Cung 2
    draw.arc([50, size-250, 220, size-80], start=0, end=90, fill=rss_color, width=15)

    # Text "RSS"
    try:
        # Thử dùng font có sẵn
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    except:
        try:
            font = ImageFont.truetype("arial.ttf", 60)
        except:
            font = ImageFont.load_default()

    text = "RSS"
    # Get text bounding box
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    text_x = (size - text_width) // 2
    text_y = 40

    draw.text((text_x, text_y), text, fill='#00d9ff', font=font)

    # Lưu icon
    # PNG
    img.save('icon.png', 'PNG')
    print("✅ Created: icon.png")

    # ICO (Windows)
    img.save('icon.ico', 'ICO')
    print("✅ Created: icon.ico")

    # Tạo các size khác cho icon
    for icon_size in [16, 32, 48, 64, 128]:
        icon_img = img.resize((icon_size, icon_size), Image.Resampling.LANCZOS)
        icon_img.save(f'icon_{icon_size}.png', 'PNG')
        print(f"✅ Created: icon_{icon_size}.png")

    print("\n🎨 Icon generation completed!")

except ImportError:
    print("❌ Pillow is not installed!")
    print("Run: pip install pillow")
except Exception as e:
    print(f"❌ Error: {e}")
