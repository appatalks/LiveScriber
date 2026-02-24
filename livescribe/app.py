"""Main floating window application."""

from __future__ import annotations

import sys
from pathlib import Path

from PyQt6.QtCore import (
    Qt,
    QPoint,
    QTimer,
    QEvent,
    QRect,
    pyqtSignal,
    pyqtSlot,
    QSize,
)
from PyQt6.QtGui import QIcon, QPainter, QColor, QFont
from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QTextEdit,
    QFrame,
    QSizePolicy,
    QFileDialog,
    QMessageBox,
    QDialog,
    QComboBox,
    QCheckBox,
    QSlider,
    QFormLayout,
    QDialogButtonBox,
    QLineEdit,
    QGroupBox,
)

from livescribe.config import AppConfig
from livescribe.recorder import Recorder
from livescribe.transcriber import Transcriber
from livescribe.summarizer import Summarizer
from livescribe.styles import get_theme


class RecordButton(QPushButton):
    """Circular record button with animated inner dot."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("recordBtn")
        self.setFixedSize(64, 64)
        self.setCheckable(True)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self._recording = False

    def set_recording(self, state: bool):
        self._recording = state
        self.setProperty("recording", "true" if state else "false")
        self.style().unpolish(self)
        self.style().polish(self)
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        if self._recording:
            # Draw a white square (stop icon)
            painter.setBrush(QColor("#1e1e2e"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(22, 22, 20, 20, 3, 3)
        else:
            # Draw a red circle (record icon)
            painter.setBrush(QColor("#f38ba8"))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(18, 18, 28, 28)

        painter.end()


class CollapsibleSection(QWidget):
    """A toggleable section with a header button and content area."""

    def __init__(self, title: str, object_name: str, editable: bool = False, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)

        # Toggle button
        self.toggle_btn = QPushButton(f"▶  {title}")
        self.toggle_btn.setObjectName("sectionToggle")
        self.toggle_btn.setCheckable(True)
        self.toggle_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.toggle_btn.toggled.connect(self._on_toggle)
        layout.addWidget(self.toggle_btn)

        # Content area
        self.content = QTextEdit()
        self.content.setObjectName(object_name)
        self.content.setReadOnly(not editable)
        self.content.setMinimumHeight(80)
        self.content.setMaximumHeight(250)
        self.content.setVisible(False)
        self.content.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        layout.addWidget(self.content)

        self._title = title

    def _on_toggle(self, checked: bool):
        self.content.setVisible(checked)
        arrow = "▼" if checked else "▶"
        self.toggle_btn.setText(f"{arrow}  {self._title}")

    def set_text(self, text: str):
        self.content.setPlainText(text)

    def append_text(self, text: str):
        self.content.moveCursor(self.content.textCursor().MoveOperation.End)
        self.content.insertPlainText(text + "\n")
        self.content.moveCursor(self.content.textCursor().MoveOperation.End)

    def clear(self):
        self.content.clear()

    def expand(self):
        self.toggle_btn.setChecked(True)


class SettingsDialog(QDialog):
    """Settings dialog with key user-facing options."""

    def __init__(self, config: AppConfig, parent=None):
        super().__init__(parent)
        self.cfg = config
        self.setWindowTitle("LiveScribe Settings")
        self.setMinimumWidth(380)

        layout = QVBoxLayout(self)
        layout.setSpacing(12)

        # ── Transcription settings ─────────────────────────────────────
        tx_group = QGroupBox("Transcription")
        tx_form = QFormLayout(tx_group)

        self.model_combo = QComboBox()
        self.model_combo.addItems([
            "distil-large-v3", "large-v3", "medium", "small", "base", "tiny",
        ])
        self.model_combo.setCurrentText(config.transcription.model_size)
        tx_form.addRow("Whisper model:", self.model_combo)

        self.lang_edit = QLineEdit(config.transcription.language or "")
        self.lang_edit.setPlaceholderText("auto-detect (leave empty)")
        tx_form.addRow("Language:", self.lang_edit)

        layout.addWidget(tx_group)

        # ── Summarization settings ─────────────────────────────────────
        sum_group = QGroupBox("Summarization")
        sum_form = QFormLayout(sum_group)

        self.sum_backend_combo = QComboBox()
        self.sum_backend_combo.addItems(["copilot", "ollama", "openai"])
        self.sum_backend_combo.setCurrentText(config.summarizer.backend)
        self.sum_backend_combo.currentTextChanged.connect(self._on_backend_changed)
        sum_form.addRow("Backend:", self.sum_backend_combo)

        self.copilot_model_combo = QComboBox()
        self.copilot_model_combo.addItems([
            "claude-sonnet-4.5", "claude-sonnet-4", "claude-haiku-4.5",
            "gpt-5", "gpt-5.1", "gpt-5.1-codex-mini", "gpt-5.1-codex",
            "gemini-3-pro-preview",
        ])
        self.copilot_model_combo.setCurrentText(config.summarizer.copilot_model)
        sum_form.addRow("Copilot model:", self.copilot_model_combo)

        self.prompt_edit = QTextEdit()
        self.prompt_edit.setPlainText(config.summarizer.system_prompt)
        self.prompt_edit.setMaximumHeight(100)
        sum_form.addRow("System prompt:", self.prompt_edit)

        layout.addWidget(sum_group)

        # ── Local server (Ollama / LM Studio) ────────────────────────
        local_group = QGroupBox("Local Server (Ollama / LM Studio)")
        local_form = QFormLayout(local_group)

        self.ollama_url_edit = QLineEdit(config.summarizer.ollama_url)
        self.ollama_url_edit.setPlaceholderText("http://localhost:11434")
        local_form.addRow("Server URL:", self.ollama_url_edit)

        ollama_row = QHBoxLayout()
        self.ollama_model_combo = QComboBox()
        self.ollama_model_combo.setEditable(True)
        self.ollama_model_combo.setMinimumWidth(200)
        if config.summarizer.ollama_model:
            self.ollama_model_combo.addItem(config.summarizer.ollama_model)
            self.ollama_model_combo.setCurrentText(config.summarizer.ollama_model)
        ollama_row.addWidget(self.ollama_model_combo)

        self.fetch_btn = QPushButton("Fetch")
        self.fetch_btn.setFixedWidth(60)
        self.fetch_btn.clicked.connect(self._fetch_models)
        ollama_row.addWidget(self.fetch_btn)
        local_form.addRow("Model:", ollama_row)

        layout.addWidget(local_group)

        # ── API Keys ──────────────────────────────────────────────────
        keys_group = QGroupBox("API Keys")
        keys_form = QFormLayout(keys_group)

        self.openai_key_edit = QLineEdit(config.summarizer.openai_api_key)
        self.openai_key_edit.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_key_edit.setPlaceholderText("sk-... (for OpenAI backend)")
        keys_form.addRow("OpenAI key:", self.openai_key_edit)

        layout.addWidget(keys_group)

        # ── Audio settings ─────────────────────────────────────────────
        audio_group = QGroupBox("Audio")
        audio_form = QFormLayout(audio_group)

        self.capture_sys = QCheckBox("Capture system audio (speakers)")
        self.capture_sys.setChecked(config.audio.capture_system_audio)
        audio_form.addRow(self.capture_sys)

        layout.addWidget(audio_group)

        # ── UI settings ───────────────────────────────────────────────
        ui_group = QGroupBox("Appearance")
        ui_form = QFormLayout(ui_group)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["dark", "light"])
        self.theme_combo.setCurrentText(config.ui.theme)
        ui_form.addRow("Theme:", self.theme_combo)

        self.on_top_check = QCheckBox("Always on top")
        self.on_top_check.setChecked(config.ui.always_on_top)
        ui_form.addRow(self.on_top_check)

        self.opacity_slider = QSlider(Qt.Orientation.Horizontal)
        self.opacity_slider.setRange(50, 100)
        self.opacity_slider.setValue(int(config.ui.opacity * 100))
        ui_form.addRow("Opacity:", self.opacity_slider)

        layout.addWidget(ui_group)

        # ── Buttons ────────────────────────────────────────────────────
        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Save | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _save(self):
        """Apply settings to config and persist."""
        self.cfg.transcription.model_size = self.model_combo.currentText()
        lang = self.lang_edit.text().strip()
        self.cfg.transcription.language = lang if lang else None

        self.cfg.summarizer.backend = self.sum_backend_combo.currentText()
        self.cfg.summarizer.copilot_model = self.copilot_model_combo.currentText()
        self.cfg.summarizer.system_prompt = self.prompt_edit.toPlainText().strip()
        self.cfg.summarizer.ollama_url = self.ollama_url_edit.text().strip()
        self.cfg.summarizer.ollama_model = self.ollama_model_combo.currentText().strip()
        self.cfg.summarizer.openai_api_key = self.openai_key_edit.text().strip()

        self.cfg.audio.capture_system_audio = self.capture_sys.isChecked()

        self.cfg.ui.theme = self.theme_combo.currentText()
        self.cfg.ui.always_on_top = self.on_top_check.isChecked()
        self.cfg.ui.opacity = self.opacity_slider.value() / 100.0

        self.cfg.save()
        self.accept()

    def _on_backend_changed(self, backend: str):
        """Show/hide relevant fields based on backend selection."""
        pass  # all fields visible for now

    def _fetch_models(self):
        """Fetch available models from the local server."""
        import requests
        url = self.ollama_url_edit.text().strip()
        if not url:
            return

        self.fetch_btn.setText("…")
        self.fetch_btn.setEnabled(False)
        models = []

        try:
            # Try OpenAI-compatible /v1/models (LM Studio, vLLM, etc.)
            resp = requests.get(f"{url}/v1/models", timeout=5)
            if resp.status_code == 200:
                for m in resp.json().get("data", []):
                    models.append(m.get("id", ""))
        except Exception:
            pass

        if not models:
            try:
                # Try Ollama API /api/tags
                resp = requests.get(f"{url}/api/tags", timeout=5)
                if resp.status_code == 200:
                    for m in resp.json().get("models", []):
                        models.append(m.get("name", ""))
            except Exception:
                pass

        self.fetch_btn.setText("Fetch")
        self.fetch_btn.setEnabled(True)

        if models:
            current = self.ollama_model_combo.currentText()
            self.ollama_model_combo.clear()
            self.ollama_model_combo.addItems(models)
            if current in models:
                self.ollama_model_combo.setCurrentText(current)
            else:
                self.ollama_model_combo.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Fetch Models", f"Could not connect to {url}")


class LiveScribeWindow(QWidget):
    """Main floating window."""

    # Signals for thread-safe UI updates
    _sig_segment = pyqtSignal(str)
    _sig_transcription_done = pyqtSignal(str)
    _sig_transcription_error = pyqtSignal(str)
    _sig_summary_done = pyqtSignal(str)
    _sig_summary_error = pyqtSignal(str)

    def __init__(self, config: AppConfig):
        super().__init__()
        self.cfg = config
        self._drag_pos: QPoint | None = None

        # ── Backend components ─────────────────────────────────────────
        self.recorder = Recorder(config.audio)
        self.transcriber = Transcriber(config.transcription)
        self.summarizer = Summarizer(config.summarizer)

        self._transcript_text = ""

        # ── Session history (in-memory) ────────────────────────────────
        self._history: list[dict] = []  # [{"transcript": str, "summary": str, "timestamp": str, "duration": float}]
        self._history_idx: int = -1     # -1 = current/new session

        # ── Window setup ───────────────────────────────────────────────
        flags = Qt.WindowType.FramelessWindowHint
        if config.ui.always_on_top:
            flags |= Qt.WindowType.WindowStaysOnTopHint
        self.setWindowFlags(flags)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, False)
        self.setWindowOpacity(config.ui.opacity)
        self.setMinimumWidth(320)
        self.setMinimumHeight(300)
        self.resize(config.ui.window_width, config.ui.window_height)

        # Edge resize state
        self._resize_edge: str | None = None
        self._resize_start_pos: QPoint | None = None
        self._resize_start_geo: QRect | None = None
        self._edge_margin = 8  # pixels from edge to trigger resize
        self.setMouseTracking(True)
        self.installEventFilter(self)

        # ── Build UI ───────────────────────────────────────────────────
        self._build_ui()
        self._connect_signals()

        # Install event filter on all child widgets for edge resize
        self._install_filter_recursive(self)

        # ── Timer for recording duration ───────────────────────────────
        self._timer = QTimer(self)
        self._timer.setInterval(500)
        self._timer.timeout.connect(self._update_timer)

        # Apply theme
        self.setStyleSheet(get_theme(config.ui.theme))

    # ── UI Construction ────────────────────────────────────────────────────

    def _install_filter_recursive(self, widget):
        """Install the event filter on all child widgets for edge resize."""
        for child in widget.findChildren(QWidget):
            child.setMouseTracking(True)
            child.installEventFilter(self)

    def _build_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(4, 4, 4, 4)  # resize grip margin
        root.setSpacing(0)

        # ── Custom title bar ───────────────────────────────────────────
        title_bar = QWidget()
        title_bar.setObjectName("titleBar")
        title_bar.setFixedHeight(40)
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(12, 0, 4, 0)

        title_label = QLabel("LiveScribe")
        title_label.setObjectName("titleLabel")
        tb_layout.addWidget(title_label)

        tb_layout.addStretch()

        btn_settings = QPushButton("⚙")
        btn_settings.setObjectName("btnMinimize")
        btn_settings.setFixedSize(32, 32)
        btn_settings.setToolTip("Settings")
        btn_settings.clicked.connect(self._open_settings)
        tb_layout.addWidget(btn_settings)

        btn_minimize = QPushButton("─")
        btn_minimize.setObjectName("btnMinimize")
        btn_minimize.setFixedSize(32, 32)
        btn_minimize.clicked.connect(self.showMinimized)
        tb_layout.addWidget(btn_minimize)

        btn_close = QPushButton("✕")
        btn_close.setObjectName("btnClose")
        btn_close.setFixedSize(32, 32)
        btn_close.clicked.connect(self.close)
        tb_layout.addWidget(btn_close)

        root.addWidget(title_bar)

        # ── Content area ───────────────────────────────────────────────
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(16, 16, 16, 12)
        cl.setSpacing(12)

        # Record button + timer
        rec_layout = QVBoxLayout()
        rec_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rec_layout.setSpacing(8)

        self.record_btn = RecordButton()
        self.record_btn.clicked.connect(self._toggle_recording)
        rec_layout.addWidget(self.record_btn, alignment=Qt.AlignmentFlag.AlignCenter)

        self.timer_label = QLabel("00:00")
        self.timer_label.setObjectName("timerLabel")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        rec_layout.addWidget(self.timer_label)

        cl.addLayout(rec_layout)

        # Separator
        sep = QFrame()
        sep.setFrameShape(QFrame.Shape.HLine)
        cl.addWidget(sep)

        # History navigation
        hist_row = QHBoxLayout()
        hist_row.setSpacing(4)

        self.btn_hist_prev = QPushButton("◀")
        self.btn_hist_prev.setObjectName("secondaryBtn")
        self.btn_hist_prev.setFixedWidth(32)
        self.btn_hist_prev.setEnabled(False)
        self.btn_hist_prev.setToolTip("Previous session")
        self.btn_hist_prev.clicked.connect(self._hist_prev)
        hist_row.addWidget(self.btn_hist_prev)

        self.hist_label = QLabel("New session")
        self.hist_label.setObjectName("statusLabel")
        self.hist_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        hist_row.addWidget(self.hist_label)

        self.btn_hist_next = QPushButton("▶")
        self.btn_hist_next.setObjectName("secondaryBtn")
        self.btn_hist_next.setFixedWidth(32)
        self.btn_hist_next.setToolTip("Next / New session")
        self.btn_hist_next.clicked.connect(self._hist_next)
        hist_row.addWidget(self.btn_hist_next)

        cl.addLayout(hist_row)

        # Transcript section
        self.transcript_section = CollapsibleSection("Transcription", "transcriptArea")
        cl.addWidget(self.transcript_section)

        # Summary section
        self.summary_section = CollapsibleSection("Summary & Notes", "summaryArea", editable=True)
        cl.addWidget(self.summary_section)

        # Action buttons
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self.btn_transcribe = QPushButton("Transcribe")
        self.btn_transcribe.setObjectName("actionBtn")
        self.btn_transcribe.setEnabled(False)
        self.btn_transcribe.clicked.connect(self._start_transcription)
        btn_row.addWidget(self.btn_transcribe)

        self.btn_summarize = QPushButton("Summarize")
        self.btn_summarize.setObjectName("actionBtn")
        self.btn_summarize.setEnabled(False)
        self.btn_summarize.clicked.connect(self._start_summarization)
        btn_row.addWidget(self.btn_summarize)

        cl.addLayout(btn_row)

        # Secondary buttons row
        btn_row2 = QHBoxLayout()
        btn_row2.setSpacing(8)

        self.btn_import = QPushButton("Import Audio")
        self.btn_import.setObjectName("secondaryBtn")
        self.btn_import.clicked.connect(self._import_audio)
        btn_row2.addWidget(self.btn_import)

        self.btn_copy = QPushButton("Copy All")
        self.btn_copy.setObjectName("secondaryBtn")
        self.btn_copy.clicked.connect(self._copy_all)
        btn_row2.addWidget(self.btn_copy)

        self.btn_save = QPushButton("Save MD")
        self.btn_save.setObjectName("secondaryBtn")
        self.btn_save.clicked.connect(self._save_markdown)
        btn_row2.addWidget(self.btn_save)

        cl.addLayout(btn_row2)

        cl.addStretch()

        # Status
        backend_label = self.cfg.summarizer.backend.capitalize()
        self.status_label = QLabel(f"Ready — {backend_label} summarizer")
        self.status_label.setObjectName("statusLabel")
        cl.addWidget(self.status_label)

        root.addWidget(content)

    def _connect_signals(self):
        self._sig_segment.connect(self._on_segment)
        self._sig_transcription_done.connect(self._on_transcription_done)
        self._sig_transcription_error.connect(self._on_transcription_error)
        self._sig_summary_done.connect(self._on_summary_done)
        self._sig_summary_error.connect(self._on_summary_error)

    # ── Window dragging & edge resizing ─────────────────────────────────

    def _edge_at(self, global_pos) -> str | None:
        """Return which edge/corner the global mouse pos is near, or None."""
        m = self._edge_margin
        geo = self.geometry()
        x, y = global_pos.x(), global_pos.y()

        on_left = x < geo.left() + m
        on_right = x > geo.right() - m
        on_top = y < geo.top() + m
        on_bottom = y > geo.bottom() - m

        if on_top and on_left:     return "tl"
        if on_top and on_right:    return "tr"
        if on_bottom and on_left:  return "bl"
        if on_bottom and on_right: return "br"
        if on_left:   return "l"
        if on_right:  return "r"
        if on_top:    return "t"
        if on_bottom: return "b"
        return None

    _CURSOR_MAP = {
        "l": Qt.CursorShape.SizeHorCursor,
        "r": Qt.CursorShape.SizeHorCursor,
        "t": Qt.CursorShape.SizeVerCursor,
        "b": Qt.CursorShape.SizeVerCursor,
        "tl": Qt.CursorShape.SizeFDiagCursor,
        "br": Qt.CursorShape.SizeFDiagCursor,
        "tr": Qt.CursorShape.SizeBDiagCursor,
        "bl": Qt.CursorShape.SizeBDiagCursor,
    }

    def eventFilter(self, obj, event):
        """Intercept mouse events from child widgets for edge resizing."""
        if event.type() == QEvent.Type.MouseMove:
            global_pos = event.globalPosition().toPoint()

            # Active resize drag
            if self._resize_edge and event.buttons() & Qt.MouseButton.LeftButton:
                self._do_resize(global_pos)
                return True

            # Hover cursor update
            edge = self._edge_at(global_pos)
            if edge:
                self.setCursor(self._CURSOR_MAP[edge])
            else:
                self.unsetCursor()

        elif event.type() == QEvent.Type.MouseButtonPress:
            if event.button() == Qt.MouseButton.LeftButton:
                global_pos = event.globalPosition().toPoint()
                edge = self._edge_at(global_pos)
                if edge:
                    self._resize_edge = edge
                    self._resize_start_pos = global_pos
                    self._resize_start_geo = QRect(self.geometry())
                    return True

        elif event.type() == QEvent.Type.MouseButtonRelease:
            if self._resize_edge:
                self._resize_edge = None
                return True

        return super().eventFilter(obj, event)

    def _do_resize(self, global_pos: QPoint):
        """Apply resize based on current drag."""
        delta = global_pos - self._resize_start_pos
        geo = QRect(self._resize_start_geo)
        e = self._resize_edge

        if "r" in e: geo.setRight(self._resize_start_geo.right() + delta.x())
        if "b" in e: geo.setBottom(self._resize_start_geo.bottom() + delta.y())
        if "l" in e: geo.setLeft(self._resize_start_geo.left() + delta.x())
        if "t" in e: geo.setTop(self._resize_start_geo.top() + delta.y())

        if geo.width() < self.minimumWidth():
            if "l" in e: geo.setLeft(geo.right() - self.minimumWidth())
            else: geo.setRight(geo.left() + self.minimumWidth())
        if geo.height() < self.minimumHeight():
            if "t" in e: geo.setTop(geo.bottom() - self.minimumHeight())
            else: geo.setBottom(geo.top() + self.minimumHeight())

        self.setGeometry(geo)

    def mousePressEvent(self, event):
        if event.button() != Qt.MouseButton.LeftButton:
            return
        global_pos = event.globalPosition().toPoint()
        edge = self._edge_at(global_pos)
        if edge:
            self._resize_edge = edge
            self._resize_start_pos = global_pos
            self._resize_start_geo = QRect(self.geometry())
        elif event.position().y() < 44:
            self._drag_pos = event.globalPosition().toPoint() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event):
        global_pos = event.globalPosition().toPoint()
        if self._resize_edge and event.buttons() & Qt.MouseButton.LeftButton:
            self._do_resize(global_pos)
            return
        if self._drag_pos and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_pos)
            return
        edge = self._edge_at(global_pos)
        if edge:
            self.setCursor(self._CURSOR_MAP[edge])
        else:
            self.unsetCursor()

    def mouseReleaseEvent(self, event):
        self._drag_pos = None
        self._resize_edge = None

    # ── Recording ──────────────────────────────────────────────────────────

    @pyqtSlot()
    def _toggle_recording(self):
        # Debounce — ignore rapid clicks (< 500ms apart)
        import time
        now = time.monotonic()
        if hasattr(self, "_last_toggle_time") and now - self._last_toggle_time < 0.5:
            return
        self._last_toggle_time = now

        if self.recorder.is_recording:
            self._stop_recording()
        else:
            # Don't auto-start a new recording right after stopping
            # (user must have audio or be on a fresh session)
            self._start_recording()

    def _start_recording(self):
        try:
            self._hist_new_session()
            self.recorder.start()
            self.record_btn.set_recording(True)
            self._timer.start()
            self.status_label.setText("Recording…")
            self.btn_transcribe.setEnabled(False)
            self.btn_summarize.setEnabled(False)
        except Exception as exc:
            self.status_label.setText(f"Mic error: {exc}")

    def _stop_recording(self):
        try:
            self.recorder.stop()
            self.record_btn.set_recording(False)
            self._timer.stop()
            duration = int(self.recorder.duration_seconds)
            mins, secs = divmod(duration, 60)
            self.status_label.setText(f"Recorded {mins}:{secs:02d} (in memory)")
            self.btn_transcribe.setEnabled(True)
        except Exception as exc:
            self.status_label.setText(f"Stop error: {exc}")

    @pyqtSlot()
    def _update_timer(self):
        secs = int(self.recorder.duration_seconds)
        mins, secs = divmod(secs, 60)
        self.timer_label.setText(f"{mins:02d}:{secs:02d}")

    # ── Transcription ──────────────────────────────────────────────────────

    @pyqtSlot()
    def _start_transcription(self):
        if not self.recorder.has_audio:
            self.status_label.setText("No recording to transcribe")
            return

        self.btn_transcribe.setEnabled(False)
        self.transcript_section.clear()
        self.transcript_section.expand()
        self.status_label.setText("Transcribing… (this may take a moment)")

        audio = self.recorder.get_audio()
        self.transcriber.transcribe_array_async(
            audio,
            sample_rate=self.recorder.cfg.sample_rate,
            on_segment=lambda t: self._sig_segment.emit(t),
            on_complete=lambda t: self._sig_transcription_done.emit(t),
            on_error=lambda e: self._sig_transcription_error.emit(str(e)),
        )

    def _transcribe_imported(self, path: Path):
        self.btn_transcribe.setEnabled(False)
        self.transcript_section.clear()
        self.transcript_section.expand()
        self.status_label.setText("Transcribing imported audio…")

        self.transcriber.transcribe_file_async(
            path,
            on_segment=lambda t: self._sig_segment.emit(t),
            on_complete=lambda t: self._sig_transcription_done.emit(t),
            on_error=lambda e: self._sig_transcription_error.emit(str(e)),
        )

    @pyqtSlot(str)
    def _on_segment(self, text: str):
        self.transcript_section.append_text(text)

    @pyqtSlot(str)
    def _on_transcription_done(self, text: str):
        self._transcript_text = text
        self.btn_transcribe.setEnabled(True)
        self.btn_summarize.setEnabled(True)
        self.status_label.setText("Transcription complete")
        self._hist_save_current()

    @pyqtSlot(str)
    def _on_transcription_error(self, error: str):
        self.btn_transcribe.setEnabled(True)
        self.status_label.setText(f"Transcription error: {error}")

    # ── Summarization ──────────────────────────────────────────────────────

    @pyqtSlot()
    def _start_summarization(self):
        if not self._transcript_text:
            self.status_label.setText("Transcribe first before summarizing")
            return

        self.btn_summarize.setEnabled(False)
        self.summary_section.clear()
        self.summary_section.expand()
        self.status_label.setText("Generating summary…")

        self.summarizer.summarize_async(
            self._transcript_text,
            on_complete=lambda s: self._sig_summary_done.emit(s),
            on_error=lambda e: self._sig_summary_error.emit(str(e)),
        )

    @pyqtSlot(str)
    def _on_summary_done(self, summary: str):
        self.summary_section.set_text(summary)
        self.btn_summarize.setEnabled(True)
        self.status_label.setText("Summary ready")
        # Auto-save current session to history
        self._hist_save_current()

    @pyqtSlot(str)
    def _on_summary_error(self, error: str):
        self.btn_summarize.setEnabled(True)
        self.status_label.setText(f"Summary error: {error}")

    # ── Session history ────────────────────────────────────────────────────

    def _hist_save_current(self):
        """Save current transcript + summary as a history entry."""
        import datetime

        transcript = self._transcript_text
        summary = self.summary_section.content.toPlainText()
        if not transcript and not summary:
            return

        entry = {
            "transcript": transcript,
            "summary": summary,
            "timestamp": datetime.datetime.now().strftime("%H:%M"),
            "duration": self.recorder.duration_seconds,
        }

        # If viewing history, update that entry; otherwise append new
        if self._history_idx >= 0 and self._history_idx < len(self._history):
            self._history[self._history_idx] = entry
        else:
            self._history.append(entry)
            self._history_idx = len(self._history) - 1

        self._hist_update_nav()

    @pyqtSlot()
    def _hist_prev(self):
        if self._history_idx > 0:
            self._history_idx -= 1
            self._hist_show(self._history_idx)
        elif self._history_idx >= len(self._history) and len(self._history) > 0:
            # On "new session", go to last saved
            self._history_idx = len(self._history) - 1
            self._hist_show(self._history_idx)

    @pyqtSlot()
    def _hist_next(self):
        if self._history_idx < len(self._history) - 1:
            # Navigate to next saved session
            self._history_idx += 1
            self._hist_show(self._history_idx)
        else:
            # At the end (or past it) — create new session
            self._hist_new_session()

    def _hist_show(self, idx: int):
        """Display a history entry."""
        entry = self._history[idx]
        self._transcript_text = entry["transcript"]
        self.transcript_section.set_text(entry["transcript"])
        if entry["transcript"]:
            self.transcript_section.expand()
        self.summary_section.set_text(entry["summary"])
        if entry["summary"]:
            self.summary_section.expand()

        self.btn_transcribe.setEnabled(False)
        self.btn_summarize.setEnabled(bool(entry["transcript"]))
        self._hist_update_nav()

    def _hist_update_nav(self):
        """Update history nav buttons and label."""
        total = len(self._history)
        idx = self._history_idx

        if total == 0 or idx >= total:
            # New/empty session
            label = f"New  ({total} saved)" if total > 0 else "New session"
            self.hist_label.setText(label)
            self.btn_hist_prev.setEnabled(total > 0)
            self.btn_hist_next.setEnabled(False)  # already on new
            self.btn_hist_next.setToolTip("New session")
            return

        entry = self._history[idx]
        self.hist_label.setText(f"{idx + 1}/{total}  •  {entry['timestamp']}")
        self.btn_hist_prev.setEnabled(idx > 0)
        self.btn_hist_next.setEnabled(True)  # always enabled: next or new
        if idx == total - 1:
            self.btn_hist_next.setToolTip("New session")
        else:
            self.btn_hist_next.setToolTip("Next session")

    def _hist_new_session(self):
        """Start a fresh session, preserving history."""
        # Save current if it has content
        if self._transcript_text or self.summary_section.content.toPlainText():
            self._hist_save_current()

        # Reset to new
        self._transcript_text = ""
        self.transcript_section.clear()
        self.summary_section.clear()
        self._history_idx = len(self._history)  # past the end = "new"
        self.timer_label.setText("00:00")
        self._hist_update_nav()

    # ── Utility actions ────────────────────────────────────────────────────

    @pyqtSlot()
    def _import_audio(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Import Audio File",
            str(Path.home()),
            "Audio Files (*.wav *.mp3 *.m4a *.ogg *.flac *.webm);;All Files (*)",
        )
        if path:
            self.status_label.setText(f"Imported: {Path(path).name}")
            self._transcribe_imported(Path(path))

    @pyqtSlot()
    def _copy_all(self):
        clipboard = QApplication.clipboard()
        parts = []
        if self._transcript_text:
            parts.append("## Transcript\n" + self._transcript_text)
        summary = self.summary_section.content.toPlainText()
        if summary:
            parts.append("## Summary\n" + summary)

        if parts:
            clipboard.setText("\n\n".join(parts))
            self.status_label.setText("Copied to clipboard")
        else:
            self.status_label.setText("Nothing to copy")

    @pyqtSlot()
    def _save_markdown(self):
        """Save transcript and summary as a Markdown file."""
        import datetime

        parts: list[str] = []
        ts = datetime.datetime.now()
        parts.append(f"# LiveScribe Notes — {ts.strftime('%B %d, %Y %H:%M')}\n")

        if self._transcript_text:
            parts.append("## Transcript\n")
            parts.append(self._transcript_text + "\n")

        summary = self.summary_section.content.toPlainText()
        if summary:
            parts.append("## Summary\n")
            parts.append(summary + "\n")

        if len(parts) <= 1:
            self.status_label.setText("Nothing to save")
            return

        # Recording info
        duration = int(self.recorder.duration_seconds)
        if duration > 0:
            mins, secs = divmod(duration, 60)
            parts.append("---\n")
            parts.append(f"*Duration: {mins}m {secs}s*\n")

        default_name = f"livescribe_{ts.strftime('%Y%m%d_%H%M%S')}.md"
        from livescribe.config import APP_DIR
        notes_dir = APP_DIR / "notes"
        notes_dir.mkdir(parents=True, exist_ok=True)

        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Notes as Markdown",
            str(notes_dir / default_name),
            "Markdown Files (*.md);;All Files (*)",
        )
        if path:
            Path(path).write_text("\n".join(parts), encoding="utf-8")
            self.status_label.setText(f"Saved: {Path(path).name}")

    # ── Settings ───────────────────────────────────────────────────────────

    @pyqtSlot()
    def _open_settings(self):
        from livescribe.styles import get_theme

        dialog = SettingsDialog(self.cfg, parent=self)
        dialog.setStyleSheet(self.styleSheet())
        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Apply theme change immediately
            self.setStyleSheet(get_theme(self.cfg.ui.theme))
            self.setWindowOpacity(self.cfg.ui.opacity)

            # Reload transcriber with new model if changed
            self.transcriber = Transcriber(self.cfg.transcription)
            self.summarizer = Summarizer(self.cfg.summarizer)

            # Update always-on-top
            flags = Qt.WindowType.FramelessWindowHint
            if self.cfg.ui.always_on_top:
                flags |= Qt.WindowType.WindowStaysOnTopHint
            self.setWindowFlags(flags)
            self.show()  # re-show after setWindowFlags

            backend_label = self.cfg.summarizer.backend.capitalize()
            self.status_label.setText(f"Settings saved — {backend_label} summarizer")


def run_app(config: AppConfig | None = None):
    """Launch the LiveScribe floating window."""
    if config is None:
        config = AppConfig.load()

    app = QApplication(sys.argv)
    app.setApplicationName("LiveScribe")

    window = LiveScribeWindow(config)
    window.show()

    sys.exit(app.exec())
