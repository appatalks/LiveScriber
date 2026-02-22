"""Speech-to-text via local faster-whisper with chunked processing for long recordings."""

from __future__ import annotations

import threading
from pathlib import Path
from typing import Callable

import numpy as np

from livescribe.config import TranscriptionConfig


class Transcriber:
    """Transcribe audio via local faster-whisper. Splits long audio into chunks."""

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

    def transcribe_array(
        self,
        audio: np.ndarray,
        sample_rate: int = 16_000,
        on_segment: Callable[[str], None] | None = None,
    ) -> str:
        """Transcribe a numpy audio array, chunking if long."""
        self._ensure_local_model()

        total_seconds = audio.size / sample_rate
        chunk_seconds = self.cfg.chunk_minutes * 60

        # Short audio — process directly
        if total_seconds <= chunk_seconds * 1.2:
            return self._transcribe_chunk(audio, on_segment)

        # Long audio — split into overlapping chunks and process sequentially
        overlap_seconds = 5  # 5-second overlap to avoid cutting mid-sentence
        chunk_samples = int(chunk_seconds * sample_rate)
        overlap_samples = int(overlap_seconds * sample_rate)
        step = chunk_samples - overlap_samples

        total_chunks = max(1, int(np.ceil((audio.size - overlap_samples) / step)))
        all_parts: list[str] = []

        if on_segment:
            on_segment(f"[Chunked: {total_chunks} segments, ~{total_seconds/60:.0f} min total]")

        for i in range(total_chunks):
            start = i * step
            end = min(start + chunk_samples, audio.size)
            chunk = audio[start:end]

            chunk_mins = start / sample_rate / 60
            if on_segment:
                on_segment(f"\n--- [{chunk_mins:.0f}:{chunk_mins % 1 * 60:02.0f}] chunk {i + 1}/{total_chunks} ---")

            text = self._transcribe_chunk(chunk, on_segment)
            if text:
                all_parts.append(text)

        return "\n".join(all_parts)

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

    # ── Internal ───────────────────────────────────────────────────────────

    def _transcribe_chunk(
        self,
        audio: np.ndarray,
        on_segment: Callable[[str], None] | None = None,
    ) -> str:
        """Transcribe a single chunk of audio."""
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
