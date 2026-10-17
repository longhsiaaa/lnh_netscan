import customtkinter as ctk
from typing import Callable

from scanner.network_utils import get_default_network
from ui import theme


class ScanFrame(ctk.CTkFrame):
    """
    Frame điều khiển quét dải IP, hiển thị thanh tiến trình và thông số thống kê.
    """

    def __init__(
        self,
        master,
        on_start_scan: Callable[[str, int], None],
        on_stop_scan: Callable[[], None],
        **kwargs,
    ):
        super().__init__(master, fg_color=theme.BG_SURFACE, corner_radius=10, **kwargs)

        self.on_start_scan = on_start_scan
        self.on_stop_scan = on_stop_scan
        self.is_scanning = False

        self._build_ui()
        self.auto_detect_range()

    def _build_ui(self):
        # Grid layout configuration
        self.columnconfigure(1, weight=1)

        # 1. Hàng nhập dải IP
        lbl_range = ctk.CTkLabel(
            self,
            text="IP Range:",
            font=theme.FONT_HEADING,
            text_color=theme.TEXT_PRIMARY,
        )
        lbl_range.grid(row=0, column=0, padx=(16, 8), pady=(14, 8), sticky="w")

        # Entry dải IP
        self.entry_range = ctk.CTkEntry(
            self,
            placeholder_text="e.g. 192.168.1.1 - 192.168.1.254 hoặc 192.168.1.0/24",
            font=theme.FONT_MONO,
            height=36,
            fg_color=theme.BG_CARD,
            border_color=theme.BORDER_COLOR,
            text_color=theme.TEXT_PRIMARY,
        )
        self.entry_range.grid(row=0, column=1, padx=(0, 10), pady=(14, 8), sticky="ew")

        # Nút Auto Detect
        btn_detect = ctk.CTkButton(
            self,
            text="Tự nhận dải",
            width=100,
            height=36,
            font=theme.FONT_BODY,
            fg_color=theme.BG_CARD,
            hover_color=theme.BG_HOVER,
            border_width=1,
            border_color=theme.BORDER_COLOR,
            text_color=theme.TEXT_PRIMARY,
            command=self.auto_detect_range,
        )
        btn_detect.grid(row=0, column=2, padx=(0, 10), pady=(14, 8))

        # Nút Bắt đầu / Dừng quét
        self.btn_scan = ctk.CTkButton(
            self,
            text="▶ Bắt đầu quét",
            width=130,
            height=36,
            font=theme.FONT_BODY_BOLD,
            fg_color=theme.ACCENT_PRIMARY,
            hover_color=theme.ACCENT_HOVER,
            command=self._on_btn_scan_clicked,
        )
        self.btn_scan.grid(row=0, column=3, padx=(0, 16), pady=(14, 8))

        # 2. Thanh tiến trình và thông tin trạng thái
        progress_container = ctk.CTkFrame(self, fg_color="transparent")
        progress_container.grid(row=1, column=0, columnspan=4, padx=16, pady=(4, 14), sticky="ew")
        progress_container.columnconfigure(0, weight=1)

        self.progress_bar = ctk.CTkProgressBar(
            progress_container,
            height=8,
            corner_radius=4,
            fg_color=theme.BG_CARD,
            progress_color=theme.ACCENT_PRIMARY,
        )
        self.progress_bar.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        self.progress_bar.set(0)

        # Label trạng thái đang quét
        self.lbl_status = ctk.CTkLabel(
            progress_container,
            text="Sẵn sàng quét mạng",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_SECONDARY,
        )
        self.lbl_status.grid(row=1, column=0, sticky="w")

        # Label thống kê kết quả
        self.lbl_stats = ctk.CTkLabel(
            progress_container,
            text="Tìm thấy: 0 | Đã quét: 0 | Thời gian: 0.0s",
            font=theme.FONT_SMALL,
            text_color=theme.TEXT_MUTED,
        )
        self.lbl_stats.grid(row=1, column=1, sticky="e")

    def auto_detect_range(self):
        """Tự động phát hiện dải mạng cục bộ của máy."""
        _, start_ip, end_ip, _ = get_default_network()
        self.entry_range.delete(0, "end")
        self.entry_range.insert(0, f"{start_ip} - {end_ip}")

    def _on_btn_scan_clicked(self):
        if not self.is_scanning:
            ip_range_text = self.entry_range.get().strip()
            if not ip_range_text:
                return
            self.on_start_scan(ip_range_text, 60)
        else:
            self.on_stop_scan()

    def set_scanning_state(self, scanning: bool):
        """Cập nhật giao diện theo trạng thái đang quét hay dừng."""
        self.is_scanning = scanning
        if scanning:
            self.btn_scan.configure(
                text="⏹ Dừng quét",
                fg_color=theme.ACCENT_DANGER,
                hover_color=theme.ACCENT_DANGER_HOVER,
            )
            self.entry_range.configure(state="disabled")
            self.progress_bar.set(0)
            self.lbl_status.configure(text="Đang chuẩn bị quét...")
        else:
            self.btn_scan.configure(
                text="▶ Bắt đầu quét",
                fg_color=theme.ACCENT_PRIMARY,
                hover_color=theme.ACCENT_HOVER,
            )
            self.entry_range.configure(state="normal")

    def update_progress(self, scanned: int, total: int, current_ip: str, alive_count: int):
        """Cập nhật thanh tiến trình theo số IP đã quét."""
        if total > 0:
            fraction = scanned / total
            self.progress_bar.set(fraction)
            self.lbl_status.configure(
                text=f"Đang quét: {current_ip} ({scanned}/{total} - {int(fraction * 100)}%)"
            )
            self.lbl_stats.configure(
                text=f"Tìm thấy: {alive_count} | Đã quét: {scanned}/{total}"
            )

    def set_completed(self, alive_count: int, total: int, elapsed_time: float, was_cancelled: bool):
        """Hiển thị thông báo khi quét xong hoặc bị dừng."""
        self.set_scanning_state(False)
        self.progress_bar.set(1.0 if not was_cancelled else self.progress_bar.get())
        status_text = "Đã dừng quét" if was_cancelled else "Quét hoàn tất"
        self.lbl_status.configure(
            text=f"✓ {status_text}! Phát hiện {alive_count} thiết bị hoạt động."
        )
        self.lbl_stats.configure(
            text=f"Tìm thấy: {alive_count} host | Tổng: {total} | Thời gian: {elapsed_time}s"
        )
