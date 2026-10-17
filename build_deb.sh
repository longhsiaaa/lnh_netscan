#!/usr/bin/env bash
# ========================================================
# Script đóng gói file cài đặt .deb cho Ubuntu/Debian
# ========================================================
set -e

PKG_NAME="lnh-netscan"
VERSION="1.0.0"
ARCH="amd64"
DEB_DIR="dist/${PKG_NAME}_${VERSION}_${ARCH}"

echo "========================================================"
echo "🚀 Đang đóng gói installer .deb cho Ubuntu (${PKG_NAME}_${VERSION}_${ARCH}.deb)..."
echo "========================================================"

# 1. Biên dịch binary nếu chưa có
if [ ! -f "dist/LNH_NetScan" ]; then
    echo "🔨 Chưa có binary, đang chạy build_linux.sh..."
    bash build_linux.sh
fi

# 2. Tạo cấu trúc thư mục .deb
rm -rf "${DEB_DIR}"
mkdir -p "${DEB_DIR}/DEBIAN"
mkdir -p "${DEB_DIR}/usr/local/bin"
mkdir -p "${DEB_DIR}/usr/share/applications"

# 3. Copy binary
cp "dist/LNH_NetScan" "${DEB_DIR}/usr/local/bin/${PKG_NAME}"
chmod 755 "${DEB_DIR}/usr/local/bin/${PKG_NAME}"

# 4. Tạo file DEBIAN/control
cat << 'EOF' > "${DEB_DIR}/DEBIAN/control"
Package: lnh-netscan
Version: 1.0.0
Section: net
Priority: optional
Architecture: amd64
Maintainer: longhsiaaa <longtthbvnn@gmail.com>
Description: LNH NetScan - Fast, multi-threaded network scanner with modern Dark GUI
 LNH NetScan is a lightweight, high-performance network IP & ARP scanner
 inspired by SoftPerfect NetScan.
EOF

# 5. Tạo shortcut Desktop Entry
cat << 'EOF' > "${DEB_DIR}/usr/share/applications/lnh-netscan.desktop"
[Desktop Entry]
Name=LNH NetScan
Comment=Fast Multi-threaded Network Scanner
Exec=/usr/local/bin/lnh-netscan
Terminal=false
Type=Application
Categories=Network;Utility;
Keywords=network;scanner;ping;arp;ip;
EOF
chmod 644 "${DEB_DIR}/usr/share/applications/lnh-netscan.desktop"

# 6. Đóng gói .deb bằng dpkg-deb
dpkg-deb --build --root-owner-group "${DEB_DIR}"

echo "========================================================"
echo "✅ ĐÃ TẠO GÓI CÀI ĐẶT .DEB THÀNH CÔNG!"
echo "File cài đặt: ${DEB_DIR}.deb"
echo "Cài đặt bằng lệnh: sudo dpkg -i ${DEB_DIR}.deb"
echo "Hoặc click đúp vào file .deb để cài qua Ubuntu Software"
echo "========================================================"
