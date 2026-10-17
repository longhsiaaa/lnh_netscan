"""Theme and styling configuration for LNH NetScan"""

# Color Palette (Dark Theme)
BG_DARK = "#12131C"          # Main Window Background
BG_SURFACE = "#1C1D2B"       # Panels / Frames Background
BG_CARD = "#24263A"          # Cards / Inputs Background
BG_HOVER = "#2E3048"         # Hover Background

BORDER_COLOR = "#343752"     # Border subtle

# Brand / Accents
ACCENT_PRIMARY = "#3B82F6"   # Modern Blue
ACCENT_HOVER = "#2563EB"
ACCENT_SUCCESS = "#10B981"   # Emerald Green (Alive)
ACCENT_DANGER = "#EF4444"    # Red (Stop / Cancel)
ACCENT_DANGER_HOVER = "#DC2626"
ACCENT_WARNING = "#F59E0B"   # Amber

# Typography Colors
TEXT_PRIMARY = "#F9FAFB"
TEXT_SECONDARY = "#9CA3AF"
TEXT_MUTED = "#6B7280"

# Table Specific
TABLE_BG = "#1A1B28"
TABLE_HEADER_BG = "#232538"
TABLE_ROW_ALT = "#1E2030"
TABLE_SELECTED = "#2D3748"

import sys

# Fonts
FONT_FAMILY = "Segoe UI" if sys.platform == "win32" else "DejaVu Sans"
FONT_MONO_FAMILY = "Consolas" if sys.platform == "win32" else "DejaVu Sans Mono"

FONT_TITLE = (FONT_FAMILY, 18, "bold")
FONT_SUBTITLE = (FONT_FAMILY, 12)
FONT_HEADING = (FONT_FAMILY, 13, "bold")
FONT_BODY = (FONT_FAMILY, 12)
FONT_BODY_BOLD = (FONT_FAMILY, 12, "bold")
FONT_MONO = (FONT_MONO_FAMILY, 11)
FONT_SMALL = (FONT_FAMILY, 10)
