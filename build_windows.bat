@echo off
title Build LNH NetScan for Windows
cd /d "%~dp0"
echo ========================================================
echo  Dong goi LNH NetScan thanh file .exe Portable & ZIP
echo ========================================================
echo.
python build_windows.py
echo.
pause
