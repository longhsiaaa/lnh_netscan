import ctypes
import ipaddress
import os
import re
import socket
import struct
import subprocess
import sys
import threading
from typing import List, Optional, Tuple


def get_local_ip() -> str:
    """Lấy IP cục bộ của máy hiện tại."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Không thực sự gửi gói tin ra ngoài, chỉ mở socket để OS chọn interface
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"
    finally:
        s.close()


def get_default_network() -> Tuple[str, str, str, str]:
    """
    Trả về thông tin mạng mặc định:
    (local_ip, start_ip, end_ip, cidr)
    Ví dụ: ('192.168.1.96', '192.168.1.1', '192.168.1.254', '192.168.1.0/24')
    """
    local_ip = get_local_ip()
    parts = local_ip.split(".")
    if len(parts) == 4 and parts[0] != "127":
        prefix = f"{parts[0]}.{parts[1]}.{parts[2]}"
        return local_ip, f"{prefix}.1", f"{prefix}.254", f"{prefix}.0/24"
    return local_ip, "192.168.1.1", "192.168.1.254", "192.168.1.0/24"


def parse_ip_range(text: str) -> List[str]:
    """
    Phân tích chuỗi đầu vào thành danh sách các địa chỉ IP.
    Hỗ trợ:
    - CIDR: '192.168.1.0/24'
    - Dải đầy đủ: '192.168.1.1 - 192.168.1.254'
    - Dải rút gọn: '192.168.1.1 - 254' hoặc '192.168.1.1-254'
    - IP đơn: '192.168.1.1'
    """
    text = text.strip()
    if not text:
        return []

    # Định dạng CIDR
    if "/" in text:
        try:
            net = ipaddress.ip_network(text, strict=False)
            return [str(ip) for ip in net.hosts()]
        except ValueError:
            return []

    # Định dạng dải với dấu '-'
    if "-" in text:
        parts = [p.strip() for p in text.split("-")]
        if len(parts) == 2:
            start_str, end_str = parts[0], parts[1]
            if "." not in end_str:
                # Dạng rút gọn: 192.168.1.1 - 254
                prefix = start_str.rsplit(".", 1)[0]
                end_str = f"{prefix}.{end_str}"
            try:
                start_ip = ipaddress.IPv4Address(start_str)
                end_ip = ipaddress.IPv4Address(end_str)
                if start_ip > end_ip:
                    start_ip, end_ip = end_ip, start_ip
                return [str(ipaddress.IPv4Address(i)) for i in range(int(start_ip), int(end_ip) + 1)]
            except ValueError:
                return []

    # IP đơn
    try:
        ip = ipaddress.IPv4Address(text)
        return [str(ip)]
    except ValueError:
        return []


def _get_mac_windows(ip_str: str) -> Optional[str]:
    """Lấy MAC address bằng Win32 SendARP API (nhẹ, nhanh, không cần quyền Admin)."""
    try:
        ip_bytes = socket.inet_aton(ip_str)
        dest_ip = struct.unpack("!I", ip_bytes)[0]
        dest_ip = socket.htonl(dest_ip)
        mac_addr = (ctypes.c_ubyte * 6)()
        mac_len = ctypes.c_ulong(6)
        res = ctypes.windll.iphlpapi.SendARP(
            dest_ip, 0, ctypes.byref(mac_addr), ctypes.byref(mac_len)
        )
        if res == 0:
            return ":".join(f"{b:02X}" for b in bytearray(mac_addr))
    except Exception:
        pass
    return None


def _get_mac_linux(ip_str: str) -> Optional[str]:
    """Lấy MAC address trên Linux bằng cách đọc /proc/net/arp hoặc ip neigh."""
    # 1. Đọc cache bảng ARP kernel (/proc/net/arp)
    try:
        if os.path.exists("/proc/net/arp"):
            with open("/proc/net/arp", "r", encoding="utf-8") as f:
                lines = f.readlines()
            for line in lines[1:]:
                parts = line.split()
                if len(parts) >= 4 and parts[0] == ip_str:
                    mac = parts[3].upper()
                    if mac != "00:00:00:00:00:00" and len(mac) == 17:
                        return mac
    except Exception:
        pass

    # 2. Gọi lệnh ip neigh show <ip>
    try:
        out = subprocess.check_output(
            ["ip", "neigh", "show", ip_str],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=0.3,
        )
        m = re.search(r"lladdr\s+([0-9a-fA-F:]{17})", out)
        if m:
            return m.group(1).upper()
    except Exception:
        pass

    # 3. Fallback: lệnh arp -n <ip>
    try:
        out = subprocess.check_output(
            ["arp", "-n", ip_str],
            text=True,
            stderr=subprocess.DEVNULL,
            timeout=0.3,
        )
        m = re.search(r"([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})", out)
        if m:
            return m.group(1).upper()
    except Exception:
        pass

    return None


def get_mac_address(ip_str: str) -> Optional[str]:
    """Lấy MAC address đa nền tảng (Windows & Linux/macOS)."""
    if sys.platform == "win32":
        return _get_mac_windows(ip_str)
    elif sys.platform.startswith("linux") or sys.platform == "darwin":
        return _get_mac_linux(ip_str)
    return None


def resolve_hostname(ip_str: str, timeout: float = 0.3) -> str:
    """Resolve IP thành hostname với timeout nhanh để tránh treo luồng mạng."""
    res = [""]

    def worker():
        try:
            host, _, _ = socket.gethostbyaddr(ip_str)
            res[0] = host
        except Exception:
            pass

    t = threading.Thread(target=worker, daemon=True)
    t.start()
    t.join(timeout=timeout)
    return res[0]

