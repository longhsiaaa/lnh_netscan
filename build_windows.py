"""
Script đóng gói tự động cho Windows (Portable .exe & ZIP)
"""
import os
import shutil
import subprocess
import sys
import zipfile

# Tự động chuyển output sang UTF-8 trên Windows console
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass


def build():
    print("=" * 60)
    print("🚀 Bắt đầu đóng gói LNH NetScan cho Windows...")
    print("=" * 60)

    # 1. Kiểm tra PyInstaller
    try:
        import PyInstaller
    except ImportError:
        print("❌ Chưa cài đặt pyinstaller. Đang cài đặt...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

    # 2. Chạy PyInstaller với spec file
    spec_file = "LNH_NetScan.spec"
    if not os.path.exists(spec_file):
        print(f"❌ Không tìm thấy {spec_file}!")
        return

    print("📦 Đang biên dịch file thực thi .exe độc lập...")
    cmd = [sys.executable, "-m", "PyInstaller", "--clean", "-y", spec_file]
    result = subprocess.run(cmd)

    if result.returncode != 0:
        print("❌ Quá trình biên dịch thất bại!")
        return

    exe_path = os.path.join("dist", "LNH_NetScan.exe")
    if not os.path.exists(exe_path):
        print(f"❌ Không tìm thấy file {exe_path} sau khi build!")
        return

    size_mb = os.path.getsize(exe_path) / (1024 * 1024)
    print(f"\n✅ Đã tạo thành công file Portable: {exe_path} ({size_mb:.2f} MB)")

    # 3. Tạo file ZIP portable tiện chia sẻ
    zip_path = os.path.join("dist", "LNH_NetScan_Portable_Win64.zip")
    print(f"📦 Đang nén thành file ZIP: {zip_path}...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        zf.write(exe_path, arcname="LNH_NetScan.exe")
        if os.path.exists("README.md"):
            zf.write("README.md", arcname="README.md")

    zip_size_mb = os.path.getsize(zip_path) / (1024 * 1024)
    print(f"✅ Đã tạo gói ZIP: {zip_path} ({zip_size_mb:.2f} MB)")
    print("\n🎉 HOÀN THÀNH! Bạn có thể gửi file trong thư mục 'dist/' cho người dùng.")


if __name__ == "__main__":
    build()
