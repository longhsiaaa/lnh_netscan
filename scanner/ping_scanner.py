import concurrent.futures
import re
import subprocess
import sys
import threading
import time
from typing import Callable, Dict, List, Optional

from scanner.network_utils import get_mac_address, resolve_hostname


class PingScanner:
    """
    Bộ quét dải mạng song song sử dụng ICMP Ping và ARP.
    Tối ưu cho Windows, không nháy cửa sổ cmd.
    """

    def __init__(self, max_workers: int = 60, timeout_ms: int = 400):
        self.max_workers = max_workers
        self.timeout_ms = timeout_ms
        self._cancel_event = threading.Event()
        self._is_scanning = False
        self._lock = threading.Lock()

    @property
    def is_scanning(self) -> bool:
        return self._is_scanning

    def cancel(self):
        """Hủy quá trình quét hiện tại."""
        self._cancel_event.set()

    def scan(
        self,
        ip_list: List[str],
        on_result: Callable[[Dict], None],
        on_progress: Callable[[int, int, str], None],
        on_complete: Callable[[int, float, bool], None],
    ):
        """
        Bắt đầu quét danh sách IP trong background thread.

        :param ip_list: Danh sách các IP cần quét
        :param on_result: Callback khi phát hiện 1 host đang hoạt động (alive)
        :param on_progress: Callback cập nhật tiến độ (scanned_count, total_count, current_ip)
        :param on_complete: Callback khi quét hoàn tất (total_alive, elapsed_time, was_cancelled)
        """
        worker_thread = threading.Thread(
            target=self._run_scan,
            args=(ip_list, on_result, on_progress, on_complete),
            daemon=True,
        )
        worker_thread.start()

    def _run_scan(
        self,
        ip_list: List[str],
        on_result: Callable[[Dict], None],
        on_progress: Callable[[int, int, str], None],
        on_complete: Callable[[int, float, bool], None],
    ):
        try:
            self._cancel_event.clear()
            self._is_scanning = True
            total = len(ip_list)
            scanned_count = 0
            alive_count = 0
            start_time = time.time()

            creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

            def check_one_host(ip: str) -> Optional[Dict]:
                if self._cancel_event.is_set():
                    return None

                # 1. ARP probe (rất nhanh trên LAN)
                mac = get_mac_address(ip)

                # 2. Ping ICMP để kiểm tra sống & đo response time
                if sys.platform == "win32":
                    ping_cmd = ["ping", "-n", "1", "-w", str(self.timeout_ms), ip]
                else:
                    timeout_sec = max(1, int(self.timeout_ms / 1000))
                    ping_cmd = ["ping", "-c", "1", "-W", str(timeout_sec), ip]

                p = subprocess.run(
                    ping_cmd,
                    capture_output=True,
                    text=True,
                    creationflags=creationflags,
                )

                is_ping_ok = p.returncode == 0

                # Trên Linux: sau khi gửi ping, kernel có thể đã cập nhật bảng ARP
                if not mac:
                    mac = get_mac_address(ip)

                is_alive = is_ping_ok or (mac is not None)

                if not is_alive:
                    return None

                # Xác định thời gian phản hồi
                response_time: Optional[int] = None
                if is_ping_ok:
                    m = re.search(r"time[<=]?\s*([0-9\.]+)\s*ms", p.stdout, re.IGNORECASE)
                    if m:
                        try:
                            response_time = int(round(float(m.group(1))))
                        except ValueError:
                            response_time = 0
                    elif "time<1ms" in p.stdout.lower() or "time<1 ms" in p.stdout.lower():
                        response_time = 0
                elif mac:
                    # Phản hồi qua ARP nhưng ICMP bị chặn bởi Firewall
                    response_time = 0

                # Lấy hostname nếu host đang sống
                hostname = resolve_hostname(ip)

                return {
                    "ip": ip,
                    "alive": True,
                    "hostname": hostname or "-",
                    "mac": mac or "-",
                    "response_time": f"{response_time} ms" if response_time is not None else "<1 ms",
                    "status": "Alive",
                }

            with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                future_to_ip = {executor.submit(check_one_host, ip): ip for ip in ip_list}

                for future in concurrent.futures.as_completed(future_to_ip):
                    ip = future_to_ip[future]
                    if self._cancel_event.is_set():
                        break

                    try:
                        res = future.result()
                        with self._lock:
                            scanned_count += 1
                            if res is not None:
                                alive_count += 1
                                on_result(res)
                            on_progress(scanned_count, total, ip)
                    except Exception:
                        with self._lock:
                            scanned_count += 1
                            on_progress(scanned_count, total, ip)

            elapsed_time = round(time.time() - start_time, 2)
            was_cancelled = self._cancel_event.is_set()
            self._is_scanning = False
            on_complete(alive_count, elapsed_time, was_cancelled)
        except Exception as e:
            import traceback
            traceback.print_exc()
            self._is_scanning = False

