import csv
import ipaddress
import os
import shutil
import subprocess
import sys
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from typing import Dict, List, Optional
import webbrowser

import customtkinter as ctk

from ui import theme


class ResultTable(ctk.CTkFrame):
    """
    Bảng hiển thị kết quả quét mạng với giao diện Dark mode,
    hỗ trợ sắp xếp cột, lọc kết quả, menu chuột phải và xuất CSV.
    """

    def __init__(self, master, **kwargs):
        super().__init__(master, fg_color=theme.BG_SURFACE, corner_radius=10, **kwargs)

        self._raw_results: List[Dict] = []
        self._sort_reverse: Dict[str, bool] = {}

        self._setup_styles()
        self._build_header_controls()
        self._build_treeview()
        self._build_context_menu()

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Cấu hình Treeview
        style.configure(
            "NetScan.Treeview",
            background=theme.TABLE_BG,
            foreground=theme.TEXT_PRIMARY,
            fieldbackground=theme.TABLE_BG,
            rowheight=30,
            font=theme.FONT_BODY,
            borderwidth=0,
        )
        style.map(
            "NetScan.Treeview",
            background=[("selected", theme.TABLE_SELECTED)],
            foreground=[("selected", theme.TEXT_PRIMARY)],
        )

        # Cấu hình tiêu đề cột (Headings)
        style.configure(
            "NetScan.Treeview.Heading",
            background=theme.TABLE_HEADER_BG,
            foreground=theme.TEXT_PRIMARY,
            font=theme.FONT_HEADING,
            relief="flat",
            padding=(6, 6),
            borderwidth=0,
        )
        style.map(
            "NetScan.Treeview.Heading",
            background=[("active", theme.BG_HOVER)],
        )

    def _build_header_controls(self):
        """Thanh công cụ bên trên bảng (Tìm kiếm, Xuất CSV, Xóa)."""
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=16, pady=(12, 8))

        # Ô tìm kiếm
        self.search_entry = ctk.CTkEntry(
            top_bar,
            placeholder_text="🔍 Tìm kiếm nhanh theo IP, Hostname, MAC...",
            font=theme.FONT_BODY,
            height=32,
            width=280,
            fg_color=theme.BG_CARD,
            border_color=theme.BORDER_COLOR,
            text_color=theme.TEXT_PRIMARY,
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self._on_filter_changed)

        # Nút Xóa kết quả
        btn_clear = ctk.CTkButton(
            top_bar,
            text="🗑 Xóa bảng",
            width=90,
            height=32,
            font=theme.FONT_BODY,
            fg_color=theme.BG_CARD,
            hover_color=theme.BG_HOVER,
            border_width=1,
            border_color=theme.BORDER_COLOR,
            text_color=theme.TEXT_PRIMARY,
            command=self.clear,
        )
        btn_clear.pack(side="right", padx=(8, 0))

        # Nút Xuất CSV
        btn_export = ctk.CTkButton(
            top_bar,
            text="📥 Xuất CSV",
            width=100,
            height=32,
            font=theme.FONT_BODY,
            fg_color=theme.BG_CARD,
            hover_color=theme.BG_HOVER,
            border_width=1,
            border_color=theme.BORDER_COLOR,
            text_color=theme.TEXT_PRIMARY,
            command=self.export_csv,
        )
        btn_export.pack(side="right")

        # Label đếm số thiết bị
        self.lbl_count = ctk.CTkLabel(
            top_bar,
            text="0 thiết bị",
            font=theme.FONT_HEADING,
            text_color=theme.ACCENT_SUCCESS,
        )
        self.lbl_count.pack(side="right", padx=16)

    def _build_treeview(self):
        """Khung chứa bảng Treeview và thanh cuộn."""
        table_container = ctk.CTkFrame(self, fg_color=theme.TABLE_BG, corner_radius=6)
        table_container.pack(fill="both", expand=True, padx=16, pady=(0, 14))

        columns = ("index", "ip", "hostname", "mac", "status", "response_time")
        self.tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            style="NetScan.Treeview",
            selectmode="extended",
        )

        col_defs = [
            ("index", "#", 45, "center"),
            ("ip", "Địa chỉ IP", 140, "center"),
            ("hostname", "Tên thiết bị (Hostname)", 220, "w"),
            ("mac", "Địa chỉ MAC", 160, "center"),
            ("status", "Trạng thái", 100, "center"),
            ("response_time", "Thời gian phản hồi", 130, "center"),
        ]

        for col_id, heading, width, align in col_defs:
            self.tree.heading(
                col_id,
                text=heading,
                command=lambda c=col_id: self._sort_column(c),
            )
            self.tree.column(col_id, width=width, anchor=align, minwidth=40)

        # Thanh cuộn dọc
        scrollbar = ttk.Scrollbar(table_container, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Cấu hình màu xen kẽ giữa các dòng
        self.tree.tag_configure("even", background=theme.TABLE_BG)
        self.tree.tag_configure("odd", background=theme.TABLE_ROW_ALT)

    def _build_context_menu(self):
        """Menu chuột phải cho từng dòng."""
        self.context_menu = tk.Menu(self, tearoff=0, bg=theme.BG_CARD, fg=theme.TEXT_PRIMARY, activebackground=theme.BG_HOVER, activeforeground=theme.TEXT_PRIMARY)
        self.context_menu.add_command(label="Sao chép Địa chỉ IP", command=self._copy_ip)
        self.context_menu.add_command(label="Sao chép Địa chỉ MAC", command=self._copy_mac)
        self.context_menu.add_command(label="Sao chép Hostname", command=self._copy_hostname)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Mở giao diện Web (HTTP)", command=self._open_in_browser)
        self.context_menu.add_command(label="Ping liên tục (CMD)", command=self._ping_cmd)

        self.tree.bind("<Button-3>", self._show_context_menu)
        self.tree.bind("<Double-1>", lambda event: self._open_in_browser())

    def add_result(self, host: Dict):
        """Thêm một kết quả host vừa quét được."""
        self._raw_results.append(host)
        self._render_row(len(self._raw_results), host)
        self._update_count()

    def _render_row(self, index: int, host: Dict):
        tag = "even" if index % 2 == 0 else "odd"
        status_display = "● Đang hoạt động"
        self.tree.insert(
            "",
            "end",
            values=(
                index,
                host.get("ip", ""),
                host.get("hostname", "-"),
                host.get("mac", "-"),
                status_display,
                host.get("response_time", "-"),
            ),
            tags=(tag,),
        )

    def clear(self):
        """Xóa trắng bảng."""
        self._raw_results.clear()
        for item in self.tree.get_children():
            self.tree.delete(item)
        self._update_count()

    def _update_count(self):
        count = len(self._raw_results)
        self.lbl_count.configure(text=f"{count} thiết bị")

    def _on_filter_changed(self, event=None):
        """Lọc danh sách theo từ khóa tìm kiếm."""
        query = self.search_entry.get().strip().lower()
        for item in self.tree.get_children():
            self.tree.delete(item)

        idx = 1
        for host in self._raw_results:
            ip = str(host.get("ip", "")).lower()
            hostname = str(host.get("hostname", "")).lower()
            mac = str(host.get("mac", "")).lower()

            if not query or (query in ip or query in hostname or query in mac):
                self._render_row(idx, host)
                idx += 1

    def _sort_column(self, col: str):
        """Sắp xếp các dòng theo cột."""
        reverse = self._sort_reverse.get(col, False)
        self._sort_reverse[col] = not reverse

        def get_sort_key(host: Dict):
            if col == "ip":
                try:
                    return ipaddress.IPv4Address(host.get("ip", "0.0.0.0"))
                except ValueError:
                    return ipaddress.IPv4Address("0.0.0.0")
            elif col == "response_time":
                rt_str = str(host.get("response_time", ""))
                digits = "".join(ch for ch in rt_str if ch.isdigit())
                return int(digits) if digits else -1
            elif col == "index":
                return 0
            return str(host.get(col, "")).lower()

        self._raw_results.sort(key=get_sort_key, reverse=reverse)

        # Vẽ lại bảng
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, host in enumerate(self._raw_results, start=1):
            self._render_row(i, host)

    def _get_selected_row(self) -> Optional[tuple]:
        selected = self.tree.selection()
        if not selected:
            return None
        return self.tree.item(selected[0])["values"]

    def _show_context_menu(self, event):
        row_id = self.tree.identify_row(event.y)
        if row_id:
            self.tree.selection_set(row_id)
            self.context_menu.tk_popup(event.x_root, event.y_root)

    def _copy_to_clipboard(self, text: str):
        self.clipboard_clear()
        self.clipboard_append(text)

    def _copy_ip(self):
        row = self._get_selected_row()
        if row and len(row) > 1:
            self._copy_to_clipboard(str(row[1]))

    def _copy_mac(self):
        row = self._get_selected_row()
        if row and len(row) > 3:
            self._copy_to_clipboard(str(row[3]))

    def _copy_hostname(self):
        row = self._get_selected_row()
        if row and len(row) > 2:
            self._copy_to_clipboard(str(row[2]))

    def _open_in_browser(self):
        row = self._get_selected_row()
        if row and len(row) > 1:
            ip = row[1]
            webbrowser.open(f"http://{ip}")

    def _ping_cmd(self):
        row = self._get_selected_row()
        if row and len(row) > 1:
            ip = str(row[1])
            if sys.platform == "win32":
                subprocess.Popen(f'cmd /c start "Ping {ip}" ping {ip} -t', shell=True)
            elif sys.platform.startswith("linux"):
                opened = False
                for term in [
                    "gnome-terminal",
                    "x-terminal-emulator",
                    "konsole",
                    "xfce4-terminal",
                    "mate-terminal",
                    "xterm",
                ]:
                    if shutil.which(term):
                        if term == "gnome-terminal":
                            subprocess.Popen([term, "--", "ping", ip])
                        else:
                            subprocess.Popen([term, "-e", f"ping {ip}"])
                        opened = True
                        break
                if not opened:
                    try:
                        subprocess.Popen(["x-terminal-emulator", "-e", f"ping {ip}"])
                    except Exception:
                        pass
            elif sys.platform == "darwin":
                subprocess.Popen(
                    ["osascript", "-e", f'tell app "Terminal" to do script "ping {ip}"']
                )

    def export_csv(self):
        """Xuất danh sách kết quả ra file CSV."""
        if not self._raw_results:
            messagebox.showinfo("Thông báo", "Chưa có kết quả quét để xuất!")
            return

        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("Tất cả tập tin", "*.*")],
            title="Lưu danh sách thiết bị quét được",
        )
        if not filepath:
            return

        try:
            with open(filepath, mode="w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f)
                writer.writerow(["STT", "Địa chỉ IP", "Hostname", "Địa chỉ MAC", "Trạng thái", "Phản hồi"])
                for i, h in enumerate(self._raw_results, start=1):
                    writer.writerow([
                        i,
                        h.get("ip", ""),
                        h.get("hostname", ""),
                        h.get("mac", ""),
                        h.get("status", ""),
                        h.get("response_time", ""),
                    ])
            messagebox.showinfo("Thành công", f"Đã xuất {len(self._raw_results)} thiết bị vào:\n{filepath}")
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể lưu file: {e}")
