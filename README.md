# ⚡ LNH NetScan - Fast Network Scanner for Windows & Linux

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows%2011%20%7C%20Ubuntu%20Linux-0078D6.svg)](https://github.com/longhsiaaa/lnh_netscan)
[![GUI](https://img.shields.io/badge/GUI-CustomTkinter-blueviolet.svg)](https://github.com/TomSchimansky/CustomTkinter)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Ứng dụng quét mạng (network scanner) tốc độ cao, đa luồng, hỗ trợ đa nền tảng (**Windows 11** & **Linux Ubuntu**) với giao diện Dark Mode hiện đại, lấy cảm hứng từ **SoftPerfect NetScan**.

*A fast, lightweight, multi-threaded cross-platform network scanner for **Windows 11** & **Ubuntu Linux** featuring a sleek modern Dark UI, inspired by **SoftPerfect NetScan**.*

---

## 📥 Tải về bản thành phẩm / Direct Downloads (v1.0.0)

[![Download Installer](https://img.shields.io/badge/Download-Installer%20(.exe)-0078D6?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/longhsiaaa/lnh_netscan/releases/download/v1.0.0/LNH_NetScan_Setup_v1.0.0.exe)
[![Download Portable](https://img.shields.io/badge/Download-Portable%20(.exe)-28A745?style=for-the-badge&logo=windows&logoColor=white)](https://github.com/longhsiaaa/lnh_netscan/releases/download/v1.0.0/LNH_NetScan.exe)
[![Download ZIP](https://img.shields.io/badge/Download-Portable%20(.zip)-6F42C1?style=for-the-badge&logo=files&logoColor=white)](https://github.com/longhsiaaa/lnh_netscan/releases/download/v1.0.0/LNH_NetScan_Portable_Win64.zip)

| Phiên bản / Edition | Định dạng | Dung lượng | Mô tả / Description | Link tải trực tiếp |
| :--- | :---: | :---: | :--- | :---: |
| **Windows Installer** | `.exe` | ~33 MB | Bộ cài đặt Windows Setup Wizard, tự tạo shortcut Desktop & gỡ cài đặt | [**Tải Installer (.exe)**](https://github.com/longhsiaaa/lnh_netscan/releases/download/v1.0.0/LNH_NetScan_Setup_v1.0.0.exe) |
| **Windows Portable** | `.exe` | ~31 MB | Bản chạy ngay 1 file duy nhất, không cần cài đặt, không cần Python | [**Tải Portable (.exe)**](https://github.com/longhsiaaa/lnh_netscan/releases/download/v1.0.0/LNH_NetScan.exe) |
| **Windows Portable (.zip)** | `.zip` | ~31 MB | Gói nén chứa file thực thi và tài liệu hướng dẫn | [**Tải ZIP**](https://github.com/longhsiaaa/lnh_netscan/releases/download/v1.0.0/LNH_NetScan_Portable_Win64.zip) |
| **Linux Ubuntu** | `.deb` / binary | - | Đóng gói nhanh bằng `./build_deb.sh` hoặc `./build_linux.sh` | [**Xem hướng dẫn**](#-trên-linux-ubuntu) |

👉 **Trang phát hành chính thức:** [https://github.com/longhsiaaa/lnh_netscan/releases](https://github.com/longhsiaaa/lnh_netscan/releases)

---

## 🌐 Languages / Ngôn ngữ
- [Tiếng Việt](#-ti%E1%BA%BFng-vi%E1%BB%87t)
- [English](#-english)

---

<a name="-tiếng-việt"></a>
## 🇻🇳 TIẾNG VIỆT

### 🌟 Tính năng nổi bật

- **Quét Ping đa luồng siêu tốc (Multi-threaded)**: Quét song song 60 luồng cực nhanh kết hợp ICMP Ping và ARP probe.
- **Hỗ trợ đa nền tảng (Cross-platform)**: Tự động thích ứng trên cả **Windows 11** (qua Win32 `SendARP` API) và **Linux Ubuntu** (qua kernel ARP cache `/proc/net/arp` & `ip neigh`).
- **Phát hiện máy bật tường lửa (Firewall Bypass)**: Phát hiện chính xác các thiết bị trong cùng mạng LAN ngay cả khi thiết bị đó bật tường lửa chặn Ping ICMP.
- **Tự động nhận diện mạng**: Tự động lấy IP của máy tính và đề xuất dải mạng Subnet tương ứng (ví dụ: `192.168.1.1 - 192.168.1.254`).
- **Phân giải tên máy (Hostname) & MAC**:
  - Tự động lấy tên máy tính trong mạng qua reverse DNS.
  - Lấy địa chỉ MAC phần cứng của từng card mạng.
  - Đo thời gian phản hồi độ trễ (Latency ms).
- **Giao diện Dark Mode hiện đại**: Thiết kế với CustomTkinter trực quan, bo góc tinh tế, êm mắt.
- **Lọc & Tìm kiếm tức thì**: Lọc danh sách kết quả ngay khi gõ theo IP, Hostname hoặc MAC.
- **Sắp xếp thông minh**: Sắp xếp cột IP theo thứ tự số học chuẩn (thay vì chuỗi text đơn thuần).
- **Menu chuột phải tiện ích**:
  - Sao chép nhanh IP, MAC, Hostname vào Clipboard.
  - Mở giao diện Web (`http://<ip>`) bằng trình duyệt mặc định (click đúp hoặc qua menu).
  - Mở cửa sổ Ping liên tục trong Terminal / CMD.
- **Xuất báo cáo CSV**: Xuất danh sách thiết bị quét được ra file `.csv` hỗ trợ mở trực tiếp bằng Microsoft Excel / LibreOffice.

---

### 🚀 Hướng dẫn Cài đặt & Chạy từ mã nguồn

#### 1. Trên Windows 11:
```bash
# Clone repository
git clone https://github.com/longhsiaaa/lnh_netscan.git
cd lnh_netscan

# Cài đặt thư viện
pip install -r requirements.txt

# Chạy ứng dụng
python main.py
```
*(Hoặc click đúp vào file `LNH_NetScan.bat` để chạy nhanh không hiện màn hình đen cmd).*

#### 2. Trên Linux Ubuntu / Debian:
```bash
# Cài đặt thư viện Python Tkinter hệ thống (nếu chưa có)
sudo apt update
sudo apt install -y python3 python3-pip python3-tk

# Clone repository
git clone https://github.com/longhsiaaa/lnh_netscan.git
cd lnh_netscan

# Cài đặt thư viện
pip3 install -r requirements.txt

# Chạy ứng dụng
python3 main.py
```

---

### 📦 Hướng dẫn Đóng gói thành phẩm (Portable & Installer)

#### A. Trên Windows 11:

1. **Bản Portable (1 file `.exe` duy nhất chạy ngay không cần cài Python)**:
   - Cách 1: Click đúp vào file **`build_windows.bat`**.
   - Cách 2: Chạy lệnh:
     ```bash
     python build_windows.py
     ```
   - Thành phẩm được lưu trong thư mục `dist/`:
     - `dist/LNH_NetScan.exe` (File chạy độc lập).
     - `dist/LNH_NetScan_Portable_Win64.zip` (Gói nén portable tiện gửi cho người dùng).

2. **Bản Cài đặt (Setup Installer với Desktop Icon & Uninstaller)**:
   - Cài đặt phần mềm **[Inno Setup](https://jrsoftware.org/isdl.php)** (miễn phí).
   - Nhấp chuột phải vào file **`installer_windows.iss`** chọn **Compile**.
   - Trình biên dịch sẽ tạo file cài đặt chuyên nghiệp `dist/LNH_NetScan_Setup_v1.0.0.exe`.

#### B. Trên Linux Ubuntu:

1. **Bản Portable Binary**:
   - Cấp quyền và chạy script:
     ```bash
     chmod +x build_linux.sh
     ./build_linux.sh
     ```
   - Thành phẩm: `dist/LNH_NetScan` (chạy ngay bằng `./dist/LNH_NetScan`) và `dist/LNH_NetScan_Linux_x64.tar.gz`.

2. **Bản Gói Cài đặt (.deb) cho Ubuntu**:
   - Cấp quyền và chạy script:
     ```bash
     chmod +x build_deb.sh
     ./build_deb.sh
     ```
   - Thành phẩm: `dist/lnh-netscan_1.0.0_amd64.deb`.
   - Cài đặt vào hệ thống:
     ```bash
     sudo dpkg -i dist/lnh-netscan_1.0.0_amd64.deb
     ```
     *(Sau khi cài, ứng dụng sẽ có biểu tượng trong menu Application của Ubuntu).*

---

### 💡 Hướng dẫn sử dụng

1. **Nhập dải IP cần quét**:
   - Dải đầy đủ: `192.168.1.1 - 192.168.1.254`
   - Dải rút gọn: `192.168.1.1 - 254` hoặc `192.168.1.1-254`
   - Ký hiệu CIDR: `192.168.1.0/24`
   - IP đơn: `192.168.1.1`
   - Bấm **"Tự nhận dải"** để ứng dụng tự điền dải mạng LAN hiện tại của máy.
2. **Bắt đầu quét**: Bấm nút **"▶ Bắt đầu quét"** (hoặc bấm **"⏹ Dừng quét"** bất cứ lúc nào).
3. **Thao tác kết quả**:
   - **Click đúp vào dòng**: Tự động mở giao diện cấu hình Web của thiết bị (`http://<ip>`).
   - **Chuột phải vào dòng**: Sao chép IP, MAC, Hostname hoặc mở cửa sổ Ping liên tục.
   - **Ô tìm kiếm**: Gõ IP, tên máy hoặc MAC để lọc dữ liệu theo thời gian thực.
   - **Xuất CSV**: Bấm nút **"📥 Xuất CSV"** để lưu file.

---
---

<a name="-english"></a>
## 🇬🇧 ENGLISH

### 🌟 Key Features

- **Blazing Fast Multi-threaded Ping Sweep**: Concurrent scanning using 60 threads combining ICMP Ping and ARP probes.
- **Cross-Platform Support**: Works seamlessly on both **Windows 11** (via Win32 `SendARP` API) and **Ubuntu Linux** (via kernel ARP cache `/proc/net/arp` and `ip neigh`).
- **Firewall Bypass on LAN**: Reliably discovers active devices even when ICMP Ping is blocked by local firewalls.
- **Auto Network Detection**: Automatically detects local IP and calculates the recommended subnet range (e.g. `192.168.1.1 - 192.168.1.254`).
- **Hostname & MAC Resolution**:
  - Resolves network device hostnames via reverse DNS.
  - Detects hardware MAC addresses.
  - Measures latency response time in milliseconds.
- **Modern Dark UI**: Clean, eye-friendly dark design built with CustomTkinter.
- **Live Search & Filter**: Real-time filtering by IP, Hostname, or MAC address as you type.
- **Smart Column Sorting**: Sorts IP addresses by true numerical octets rather than simple string comparison.
- **Context Menu Utilities**:
  - Quick copy for IP, MAC, and Hostname.
  - Open device web interface (`http://<ip>`) in default browser.
  - Open continuous ping window in Terminal / CMD.
- **CSV Data Export**: Export results to `.csv` compatible with Microsoft Excel and LibreOffice Calc.

---

### 🚀 Installation & Running from Source

#### 1. On Windows 11:
```bash
git clone https://github.com/longhsiaaa/lnh_netscan.git
cd lnh_netscan
pip install -r requirements.txt
python main.py
```
*(Or double-click `LNH_NetScan.bat` for a console-free launch).*

#### 2. On Ubuntu Linux:
```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-tk
git clone https://github.com/longhsiaaa/lnh_netscan.git
cd lnh_netscan
pip3 install -r requirements.txt
python3 main.py
```

---

### 📦 Packaging into Portable & Installer Builds

#### A. On Windows 11:

1. **Portable Executable (`.exe`)**:
   - Double click `build_windows.bat`, or run:
     ```bash
     python build_windows.py
     ```
   - Generated files located in `dist/`:
     - `dist/LNH_NetScan.exe` (Single standalone executable).
     - `dist/LNH_NetScan_Portable_Win64.zip` (Portable ZIP package).

2. **Setup Installer**:
   - Install **[Inno Setup](https://jrsoftware.org/isdl.php)**.
   - Right-click `installer_windows.iss` and select **Compile**.
   - The installer `dist/LNH_NetScan_Setup_v1.0.0.exe` will be generated with Start Menu & Desktop shortcuts.

#### B. On Ubuntu Linux:

1. **Portable Binary**:
   ```bash
   chmod +x build_linux.sh
   ./build_linux.sh
   ```
   - Output: `dist/LNH_NetScan` & `dist/LNH_NetScan_Linux_x64.tar.gz`.

2. **Debian Package (`.deb`)**:
   ```bash
   chmod +x build_deb.sh
   ./build_deb.sh
   ```
   - Output: `dist/lnh-netscan_1.0.0_amd64.deb`.
   - Install with: `sudo dpkg -i dist/lnh-netscan_1.0.0_amd64.deb`

---

## 📁 Project Structure

```
lnh_netscan/
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies (customtkinter)
├── LNH_NetScan.spec            # PyInstaller spec configuration
├── build_windows.py            # Windows build script (exe & zip)
├── build_windows.bat           # 1-Click Windows build launcher
├── build_linux.sh              # Linux portable build script
├── build_deb.sh                # Ubuntu .deb installer packager
├── installer_windows.iss       # Inno Setup Windows installer script
├── scanner/
│   ├── __init__.py
│   ├── network_utils.py        # Cross-platform ARP, Hostname, IP logic
│   └── ping_scanner.py         # Multi-threaded ping sweep engine
└── ui/
    ├── __init__.py
    ├── app.py                  # Main CustomTkinter window & event queue
    ├── scan_frame.py           # IP range input & progress controls
    ├── result_table.py         # Results treeview, sort, search, context menu
    └── theme.py                # Dark theme palette & cross-platform fonts
```

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
