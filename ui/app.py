import queue
import tkinter.messagebox as messagebox
from typing import Dict

import customtkinter as ctk

from scanner.network_utils import get_default_network, parse_ip_range
from scanner.ping_scanner import PingScanner
from ui import theme
from ui.result_table import ResultTable
from ui.scan_frame import ScanFrame


class NetScanApp(ctk.CTk):
    """
    Ứng dụng chính LNH NetScan - Network Scanner cho Windows & Linux.
    """

    def __init__(self):
        super().__init__()

        # Khởi tạo cửa sổ
        self.title("LNH NetScan - Network Scanner")
        self.geometry("1080x700")
        self.minsize(850, 520)

        # Cấu hình CustomTkinter
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.configure(fg_color=theme.BG_DARK)

        # Hàng đợi thông điệp giữa luồng quét và luồng giao diện chính (Thread-safe)
        self.msg_queue = queue.Queue()

        # Scanner engine
        self.scanner = PingScanner(max_workers=60, timeout_ms=400)
        self.current_alive_count = 0
        self.total_ips_to_scan = 0

        # Lấy thông tin mạng cục bộ
        self.local_ip, _, _, self.local_cidr = get_default_network()

        # Dựng giao diện
        self._build_header()
        self._build_main_content()
        self._build_footer()

        # Bắt đầu vòng lặp xử lý hàng đợi
        self._process_queue()


    def _build_header(self):
        """Thanh tiêu đề trên cùng với logo và thông tin mạng máy."""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(16, 10))

        # Tiêu đề ứng dụng
        title_box = ctk.CTkFrame(header_frame, fg_color="transparent")
        title_box.pack(side="left")

        lbl_logo = ctk.CTkLabel(
            title_box,
            text="⚡",
            font=("Segoe UI", 24),
            text_color=theme.ACCENT_PRIMARY,
        )
        lbl_logo.pack(side="left", padx=(0, 10))

        lbl_title = ctk.CTkLabel(
            title_box,
            text="LNH NetScan",
            font=theme.FONT_TITLE,
            text_color=theme.TEXT_PRIMARY,
        )
        lbl_title.pack(side="left")

        lbl_badge = ctk.CTkLabel(
            title_box,
            text="v1.0",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_MUTED,
        )
        lbl_badge.pack(side="left", padx=8, pady=(4, 0))

        # Thông tin IP máy hiện tại
        info_badge = ctk.CTkFrame(
            header_frame,
            fg_color=theme.BG_SURFACE,
            corner_radius=8,
            border_width=1,
            border_color=theme.BORDER_COLOR,
        )
        info_badge.pack(side="right")

        lbl_info = ctk.CTkLabel(
            info_badge,
            text=f"🌐 IP của bạn: {self.local_ip}  |  Subnet: {self.local_cidr}",
            font=theme.FONT_BODY,
            text_color=theme.TEXT_SECONDARY,
        )
        lbl_info.pack(padx=14, pady=6)

    def _build_main_content(self):
        """Khu vực nội dung chính: Bảng điều khiển quét và Bảng danh sách kết quả."""
        # Frame điều khiển quét
        self.scan_frame = ScanFrame(
            self,
            on_start_scan=self.start_scan,
            on_stop_scan=self.stop_scan,
        )
        self.scan_frame.pack(fill="x", padx=20, pady=(0, 12))

        # Bảng kết quả
        self.result_table = ResultTable(self)
        self.result_table.pack(fill="both", expand=True, padx=20, pady=(0, 8))

    def _build_footer(self):
        """Thanh trạng thái chân trang."""
        footer_frame = ctk.CTkFrame(self, fg_color="transparent")
        footer_frame.pack(fill="x", padx=20, pady=(0, 10))

        self.lbl_footer_status = ctk.CTkLabel(
            footer_frame,
            text="Trạng thái: Sẵn sàng  •  Quét đa luồng (60 luồng ICMP + ARP)",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_MUTED,
        )
        self.lbl_footer_status.pack(side="left")

        lbl_tips = ctk.CTkLabel(
            footer_frame,
            text="Mẹo: Click đúp vào dòng để mở Web • Chuột phải để sao chép hoặc Ping",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_MUTED,
        )
        lbl_tips.pack(side="right")

    def start_scan(self, range_str: str, threads: int = 60):
        """Xử lý bắt đầu quét dải IP."""
        ip_list = parse_ip_range(range_str)
        if not ip_list:
            messagebox.showwarning(
                "Định dạng IP không hợp lệ",
                "Vui lòng nhập dải IP hợp lệ!\n\nVí dụ:\n- 192.168.1.1 - 192.168.1.254\n- 192.168.1.1-254\n- 192.168.1.0/24",
            )
            return

        # Cảnh báo nếu dải quá lớn (ví dụ > 1024 IP)
        if len(ip_list) > 1024:
            confirm = messagebox.askyesno(
                "Cảnh báo dải IP lớn",
                f"Dải mạng này có {len(ip_list)} địa chỉ IP. Quá trình quét có thể mất nhiều thời gian.\nBạn có muốn tiếp tục không?",
            )
            if not confirm:
                return

        self.current_alive_count = 0
        self.total_ips_to_scan = len(ip_list)

        # Xóa kết quả cũ và cập nhật trạng thái
        self.result_table.clear()
        self.scan_frame.set_scanning_state(True)
        self.lbl_footer_status.configure(
            text=f"Trạng thái: Đang quét {len(ip_list)} địa chỉ IP..."
        )

        # Khởi chạy quét
        self.scanner.scan(
            ip_list=ip_list,
            on_result=self._on_host_found,
            on_progress=self._on_scan_progress,
            on_complete=self._on_scan_completed,
        )

    def stop_scan(self):
        """Hủy quét."""
        self.scanner.cancel()
        self.lbl_footer_status.configure(text="Trạng thái: Đang dừng quét...")

    # --- Giao tiếp đa luồng an toàn qua Message Queue ---

    def _process_queue(self):
        """Xử lý các sự kiện từ luồng quét gửi về giao diện."""
        try:
            while True:
                msg_type, data = self.msg_queue.get_nowait()
                if msg_type == "host_found":
                    self.current_alive_count += 1
                    self.result_table.add_result(data)
                elif msg_type == "progress":
                    scanned, total, current_ip = data
                    self.scan_frame.update_progress(
                        scanned, total, current_ip, self.current_alive_count
                    )
                elif msg_type == "completed":
                    alive_count, elapsed_time, was_cancelled = data
                    self.scan_frame.set_completed(
                        alive_count, self.total_ips_to_scan, elapsed_time, was_cancelled
                    )
                    msg = (
                        f"Đã dừng! Tìm thấy {alive_count} host trong {elapsed_time}s"
                        if was_cancelled
                        else f"Hoàn tất! Tìm thấy {alive_count} host trong {elapsed_time}s"
                    )
                    self.lbl_footer_status.configure(text=f"Trạng thái: {msg}")
        except queue.Empty:
            pass
        except Exception as e:
            print("Lỗi xử lý hàng đợi giao diện:", e)
        finally:
            # Lặp lại sau mỗi 40ms (~25 FPS) để giao diện mượt mà
            self.after(40, self._process_queue)

    def _on_host_found(self, host: Dict):
        self.msg_queue.put(("host_found", host))

    def _on_scan_progress(self, scanned: int, total: int, current_ip: str):
        self.msg_queue.put(("progress", (scanned, total, current_ip)))

    def _on_scan_completed(self, alive_count: int, elapsed_time: float, was_cancelled: bool):
        self.msg_queue.put(("completed", (alive_count, elapsed_time, was_cancelled)))

