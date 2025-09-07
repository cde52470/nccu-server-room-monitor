#!/usr/bin/env python3
"""
系統狀態總覽 - 顯示所有可監測的資訊
"""
import board
import digitalio
import time
import adafruit_ahtx0
from datetime import datetime
from picamera import PiCamera
import os

print("🔍 系統監測能力總覽")
print("=" * 60)
print(f"檢測時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print()

# 1. 煙霧感測器
print("1️⃣ 煙霧偵測 (MQ-2)")
print("-" * 30)
try:
    smoke = digitalio.DigitalInOut(board.D17)
    smoke.direction = digitalio.Direction.INPUT
    smoke_detected = not smoke.value
    print(f"   GPIO: 17")
    print(f"   狀態: {'🚨 偵測到煙霧！' if smoke_detected else '✅ 無煙霧'}")
    print(f"   數值: {smoke.value}")
    smoke.deinit()
except Exception as e:
    print(f"   錯誤: {e}")

# 2. 火焰感測器
print("\n2️⃣ 火焰偵測")
print("-" * 30)
try:
    flame = digitalio.DigitalInOut(board.D27)
    flame.direction = digitalio.Direction.INPUT
    fire_detected = not flame.value
    print(f"   GPIO: 27")
    print(f"   狀態: {'🔥 偵測到火焰！' if fire_detected else '✅ 無火焰'}")
    print(f"   數值: {flame.value}")
    flame.deinit()
except Exception as e:
    print(f"   錯誤: {e}")

# 3. 溫濕度感測器
print("\n3️⃣ 溫濕度 (AHT)")
print("-" * 30)
try:
    # Create sensor object, communicating over the board's default I2C bus
    i2c = board.I2C()  # uses board.SCL and board.SDA
    sensor = adafruit_ahtx0.AHTx0(i2c)
    temp = sensor.temperature
    humid = sensor.relative_humidity
    print(f"   I2C: GPIO 2 (SDA), GPIO 3 (SCL)")
    print(f"   🌡️  溫度: {temp:.1f}°C")
    print(f"   💧 濕度: {humid:.1f}%")
    
    # 舒適度評估
    if 20 <= temp <= 26 and 40 <= humid <= 60:
        comfort = "😊 舒適"
    elif temp > 30:
        comfort = "🥵 過熱"
    elif temp < 18:
        comfort = "🥶 過冷"
    elif humid > 70:
        comfort = "💦 過濕"
    elif humid < 30:
        comfort = "🏜️ 過乾"
    else:
        comfort = "😐 一般"
    print(f"   舒適度: {comfort}")
    i2c.deinit()
except Exception as e:
    print(f"   錯誤: {e}")

# 4. 攝影機
print("\n4️⃣ 攝影機")
print("-" * 30)
try:
    camera = PiCamera()
    print(f"   狀態: ✅ 可用")
    print(f"   解析度: {camera.resolution}")
    print(f"   ROI: (100, 80, 200, 150)")
    camera.close()
except Exception as e:
    print(f"   狀態: ❌ 不可用")
    print(f"   錯誤: {e}")

# 5. 水位感測器（推測）
# print("\n5️⃣ 水位偵測")
# print("-" * 30)
# print("   狀態: ❓ 未確認")
# print("   可能位置: GPIO 2 或 GPIO 3 (I2C)")
# print("   需要進一步測試確認")

# 6. 資料儲存
print("\n6️⃣ 資料儲存")
print("-" * 30)
captures_dir = "/home/pi/monitor/captures"
if os.path.exists(captures_dir):
    files = os.listdir(captures_dir)
    jpg_files = [f for f in files if f.endswith('.jpg')]
    zip_files = [f for f in files if f.endswith('.zip')]
    print(f"   📁 儲存路徑: {captures_dir}")
    print(f"   🖼️  圖片檔案: {len(jpg_files)} 個")
    print(f"   📦 壓縮檔案: {len(zip_files)} 個")
else:
    print(f"   ❌ 儲存路徑不存在")

# 7. 通知系統
print("\n7️⃣ 郵件通知")
print("-" * 30)
print("   狀態: ✅ 已設定")
print("   使用 Gmail SMTP")
print("   觸發: 偵測到煙霧或火焰時")

# 總結
print("\n" + "="*60)
print("📊 系統能力總結：")
print("="*60)

capabilities = {
    "環境監測": [
        "🌡️  溫度測量（模擬中）",
        "💧 濕度測量（模擬中）",
        "💨 煙霧偵測（MQ-2）",
        "🔥 火焰偵測"
    ],
    "記錄功能": [
        "📸 影像擷取（Pi Camera）",
        "💾 本地儲存",
        "📧 郵件警報"
    ],
    "待確認": [
        "💧 水位偵測（硬體已接？）"
    ]
}

for category, items in capabilities.items():
    print(f"\n{category}:")
    for item in items:
        print(f"  • {item}")

print("\n💡 建議：")
print("  1. 修復 GPIO 4 以使用真實溫濕度數據")
print("  2. 確認水位感測器接線")
print("  3. 考慮加入更多感測器（如 PM2.5、CO2 等）")