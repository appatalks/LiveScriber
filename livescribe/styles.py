"""QSS stylesheets for the LiveScribe UI."""

DARK_THEME = """
/* ── Global ──────────────────────────────────────────────────────────── */
QWidget {
    background-color: #1e1e2e;
    color: #cdd6f4;
    font-family: "Segoe UI", "SF Pro Text", "Cantarell", sans-serif;
    font-size: 13px;
}

/* ── Title bar ───────────────────────────────────────────────────────── */
#titleBar {
    background-color: #181825;
    border-bottom: 1px solid #313244;
}

#titleLabel {
    color: #cdd6f4;
    font-size: 14px;
    font-weight: 600;
}

#btnMinimize, #btnClose {
    background: transparent;
    border: none;
    color: #6c7086;
    font-size: 16px;
    padding: 4px 10px;
    border-radius: 4px;
}

#btnMinimize:hover { background-color: #313244; color: #cdd6f4; }
#btnClose:hover    { background-color: #f38ba8; color: #1e1e2e; }

/* ── Record button ───────────────────────────────────────────────────── */
#recordBtn {
    background-color: #45475a;
    border: 3px solid #585b70;
    border-radius: 32px;
    min-width: 64px;
    min-height: 64px;
    max-width: 64px;
    max-height: 64px;
}

#recordBtn:hover {
    background-color: #585b70;
    border-color: #f38ba8;
}

#recordBtn[recording="true"] {
    background-color: #f38ba8;
    border-color: #f38ba8;
}

/* ── Timer label ─────────────────────────────────────────────────────── */
#timerLabel {
    color: #a6adc8;
    font-size: 22px;
    font-family: "JetBrains Mono", "Fira Code", monospace;
    font-weight: 500;
}

/* ── Status bar ──────────────────────────────────────────────────────── */
#statusLabel {
    color: #6c7086;
    font-size: 11px;
    padding: 2px 8px;
}

/* ── Toggle section headers ──────────────────────────────────────────── */
#sectionToggle {
    background-color: #181825;
    border: 1px solid #313244;
    border-radius: 6px;
    padding: 8px 12px;
    text-align: left;
    font-weight: 600;
    font-size: 12px;
    color: #cdd6f4;
}

#sectionToggle:hover {
    background-color: #1e1e2e;
    border-color: #45475a;
}

#sectionToggle:checked {
    border-color: #89b4fa;
    color: #89b4fa;
}

/* ── Text areas ──────────────────────────────────────────────────────── */
#transcriptArea, #summaryArea {
    background-color: #11111b;
    border: 1px solid #313244;
    border-radius: 6px;
    padding: 10px;
    font-size: 12px;
    line-height: 1.5;
    color: #cdd6f4;
    selection-background-color: #45475a;
}

/* ── Action buttons ──────────────────────────────────────────────────── */
#actionBtn {
    background-color: #89b4fa;
    color: #1e1e2e;
    border: none;
    border-radius: 6px;
    padding: 6px 16px;
    font-weight: 600;
    font-size: 12px;
}

#actionBtn:hover {
    background-color: #74c7ec;
}

#actionBtn:disabled {
    background-color: #45475a;
    color: #6c7086;
}

#secondaryBtn {
    background-color: transparent;
    color: #89b4fa;
    border: 1px solid #89b4fa;
    border-radius: 6px;
    padding: 6px 16px;
    font-weight: 600;
    font-size: 12px;
}

#secondaryBtn:hover {
    background-color: #1e1e2e;
}

/* ── Scrollbar ───────────────────────────────────────────────────────── */
QScrollBar:vertical {
    background: transparent;
    width: 8px;
    margin: 0;
}

QScrollBar::handle:vertical {
    background: #45475a;
    border-radius: 4px;
    min-height: 30px;
}

QScrollBar::handle:vertical:hover {
    background: #585b70;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    background: transparent;
}

/* ── Separator ───────────────────────────────────────────────────────── */
QFrame[frameShape="4"] {
    color: #313244;
}
"""

LIGHT_THEME = """
QWidget {
    background-color: #eff1f5;
    color: #4c4f69;
    font-family: "Segoe UI", "SF Pro Text", "Cantarell", sans-serif;
    font-size: 13px;
}

#titleBar { background-color: #e6e9ef; border-bottom: 1px solid #ccd0da; }
#titleLabel { color: #4c4f69; font-size: 14px; font-weight: 600; }

#btnMinimize, #btnClose {
    background: transparent; border: none; color: #8c8fa1;
    font-size: 16px; padding: 4px 10px; border-radius: 4px;
}
#btnMinimize:hover { background-color: #ccd0da; }
#btnClose:hover    { background-color: #d20f39; color: white; }

#recordBtn {
    background-color: #ccd0da; border: 3px solid #bcc0cc;
    border-radius: 32px; min-width: 64px; min-height: 64px; max-width: 64px; max-height: 64px;
}
#recordBtn:hover { background-color: #bcc0cc; border-color: #d20f39; }
#recordBtn[recording="true"] { background-color: #d20f39; border-color: #d20f39; }

#timerLabel { color: #6c6f85; font-size: 22px; font-family: monospace; font-weight: 500; }
#statusLabel { color: #8c8fa1; font-size: 11px; padding: 2px 8px; }

#sectionToggle {
    background-color: #e6e9ef; border: 1px solid #ccd0da; border-radius: 6px;
    padding: 8px 12px; text-align: left; font-weight: 600; font-size: 12px; color: #4c4f69;
}
#sectionToggle:hover { background-color: #dce0e8; }
#sectionToggle:checked { border-color: #1e66f5; color: #1e66f5; }

#transcriptArea, #summaryArea {
    background-color: #dce0e8; border: 1px solid #ccd0da; border-radius: 6px;
    padding: 10px; font-size: 12px; color: #4c4f69;
}

#actionBtn {
    background-color: #1e66f5; color: white; border: none; border-radius: 6px;
    padding: 6px 16px; font-weight: 600; font-size: 12px;
}
#actionBtn:hover { background-color: #2a6ef5; }
#actionBtn:disabled { background-color: #ccd0da; color: #8c8fa1; }

#secondaryBtn {
    background-color: transparent; color: #1e66f5; border: 1px solid #1e66f5;
    border-radius: 6px; padding: 6px 16px; font-weight: 600; font-size: 12px;
}
"""


def get_theme(name: str = "dark") -> str:
    return LIGHT_THEME if name == "light" else DARK_THEME
