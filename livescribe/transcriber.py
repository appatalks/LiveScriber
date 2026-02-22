"""Speech-to-text via local faster-whisper."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Callable

import numpy as np

from livescribe.config import TranscriptionConfig


class Transcriber:
    """Transcribe audio via local faster-whisper."""

    def __init__(self, config: TranscriptionConfig):
        self.cfg = config
        self._local_model = None
        self._lock = threading.Lock()

    # ── Lazy model loading ─────────────────────────────────────────────────

    def _ensure_local_model(self):
        if self._local_model is None:
            from faster_whisper import WhisperModel

            self._local_model = WhisperModel(
                self.cfg.model_size,
                device=self.cfg.device,
                compute_type=self.cfg.compute_type,
            )

    # ── Public API ─────────────────────────────────────────────────────────

    def transcribe_file(
        self,
        audio_path: Path | str,
        on_segment: Callable[[str], None] | None = None,
    ) -> str:
        """Transcribe an audio file. Returns full transcript text."""
        return self._transcribe_local_file(Path(audio_path), on_segment)

    def transcribe_array(
        self,
        audio: np.ndarray,
        sample_rate: int = 16_000,
        on_segment: Callable[[str], None] | None = None,
    ) -> str:
        """Transcribe a numpy audio array (float32, mono)."""
        return self._transcribe_local_array(audio, sample_rate, on_segment)

    def transcribe_file_async(
        self,
        audio_path: Path | str,
        on_segment: Callable[[str], None] | None = None,
        on_complete: Callable[[str], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
    ) -> threading.Thread:
        """Run transcription in a background thread."""

        def _worker():
            try:
                result = self.transcribe_file(audio_path, on_segment=on_segment)
                if on_complete:
                    on_complete(result)
            except Exception as exc:
                if on_error:
                    on_error(exc)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        return t

    def transcribe_array_async(
        self,
        audio: np.ndarray,
        sample_rate: int = 16_000,
        on_segment: Callable[[str], None] | None = None,
        on_complete: Callable[[str], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
    ) -> threading.Thread:
        """Run transcription on a numpy array in a background thread."""

        def _worker():
            try:
                result = self.transcribe_array(audio, sample_rate, on_segment=on_segment)
                if on_complete:
                    on_complete(result)
            except Exception as exc:
                if on_error:
                    on_error(exc)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        return t

    # ── Local faster-whisper backend ───────────────────────────────────────

    def _transcribe_local_file(
        self, audio_path: Path, on_segment: Callable[[str], None] | None = None
    ) -> str:
        self._ensure_local_model()

        segments, info = self._local_model.transcribe(
            str(audio_path),
            beam_size=self.cfg.beam_size,
            language=self.cfg.language,
            vad_filter=self.cfg.vad_filter,
        )

        parts: list[str] = []
        for segment in segments:
            text = segment.text.strip()
            if text:
                parts.append(text)
                if on_segment:
                    on_segment(text)
        return "\n".join(parts)

    def _transcribe_local_array(
        self,
        audio: np.ndarray,
        sample_rate: int,
        on_segment: Callable[[str], None] | None = None,
    ) -> str:
        self._ensure_local_model()

        segments, info = self._local_model.transcribe(
            audio,
            beam_size=self.cfg.beam_size,
            language=self.cfg.language,
            vad_filter=self.cfg.vad_filter,
        )

        parts: list[str] = []
        for segment in segments:
            text = segment.text.strip()
            if text:
                parts.append(text)
                if on_segment:
                    on_segment(text)
        return "\n".join(parts)
