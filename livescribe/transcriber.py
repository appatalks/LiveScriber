"""Speech-to-text — GitHub Models (cloud Whisper) or local faster-whisper."""

from __future__ import annotations

import io
import threading
import wave
from pathlib import Path
from typing import Callable

import numpy as np

from livescribe.config import TranscriptionConfig


class Transcriber:
    """Transcribe audio via GitHub Models API or local faster-whisper."""

    def __init__(self, config: TranscriptionConfig):
        self.cfg = config
        self._local_model = None
        self._lock = threading.Lock()

    # ── Lazy local model loading ───────────────────────────────────────────

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
        if self.cfg.backend == "github":
            return self._transcribe_github_file(Path(audio_path), on_segment)
        return self._transcribe_local_file(Path(audio_path), on_segment)

    def transcribe_array(
        self,
        audio: np.ndarray,
        sample_rate: int = 16_000,
        on_segment: Callable[[str], None] | None = None,
    ) -> str:
        """Transcribe a numpy audio array (float32, mono)."""
        if self.cfg.backend == "github":
            return self._transcribe_github_array(audio, sample_rate, on_segment)
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

    # ── GitHub Models backend ──────────────────────────────────────────────

    def _get_github_client(self):
        from openai import OpenAI

        return OpenAI(
            base_url=self.cfg.github_base_url,
            api_key=self.cfg.github_token,
        )

    def _transcribe_github_file(
        self, audio_path: Path, on_segment: Callable[[str], None] | None = None
    ) -> str:
        """Send audio file to GitHub Models Whisper API."""
        client = self._get_github_client()

        with open(audio_path, "rb") as f:
            result = client.audio.transcriptions.create(
                model=self.cfg.github_model,
                file=f,
                language=self.cfg.language or "",
            )

        text = result.text.strip()
        if text and on_segment:
            # Emit the full text as a single segment (API returns all at once)
            on_segment(text)
        return text

    def _transcribe_github_array(
        self,
        audio: np.ndarray,
        sample_rate: int,
        on_segment: Callable[[str], None] | None = None,
    ) -> str:
        """Convert numpy array to WAV in-memory and send to GitHub Models."""
        client = self._get_github_client()

        # Write numpy audio to an in-memory WAV
        buf = io.BytesIO()
        audio_int16 = np.clip(audio * 32767, -32768, 32767).astype(np.int16)
        with wave.open(buf, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_int16.tobytes())
        buf.seek(0)
        buf.name = "audio.wav"  # OpenAI SDK needs a .name attribute

        result = client.audio.transcriptions.create(
            model=self.cfg.github_model,
            file=buf,
            language=self.cfg.language or "",
        )

        text = result.text.strip()
        if text and on_segment:
            on_segment(text)
        return text

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
