"""
LNH NetScan - Fast Network Scanner for Windows & Linux
Inspired by SoftPerfect NetScan.
"""

import sys
from ui.app import NetScanApp


def main():
    app = NetScanApp()
    app.mainloop()


if __name__ == "__main__":
    main()
