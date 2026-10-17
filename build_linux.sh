#!/usr/bin/env bash
# ========================================================
# Script build Portable Binary & Archive cho Linux Ubuntu
# ========================================================
set -e

echo "========================================================"
echo "🚀 Đang đóng gói LNH NetScan cho Linux Ubuntu..."
echo "========================================================"

# Kiểm tra python3 và pip
if ! command -v python3 &> /dev/null; then
    echo "❌ Không tìm thấy python3! Hãy cài đặt: sudo apt update && sudo apt install -y python3 python3-pip python3-tk"
    exit 1
fi

# Cài đặt thư viện
echo "📦 Đang cài đặt thư viện phụ thuộc..."
python3 -m pip install -r requirements.txt pyinstaller

# Biên dịch bằng PyInstaller
echo "🔨 Đang biên dịch Portable binary..."
pyinstaller --clean -y LNH_NetScan.spec

chmod +x dist/LNH_NetScan

# Nén thành tar.gz
echo "📦 Đang nén file tar.gz..."
tar -czvf dist/LNH_NetScan_Linux_x64.tar.gz -C dist LNH_NetScan

echo "========================================================"
echo "✅ HOÀN THÀNH!"
echo "Binary portable: dist/LNH_NetScan"
echo "Gói tar.gz:      dist/LNH_NetScan_Linux_x64.tar.gz"
echo "========================================================"
