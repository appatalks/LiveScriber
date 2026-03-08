"""Speech-to-text via local faster-whisper with chunked processing for long recordings."""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import tempfile
import threading
import wave
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

            try:
                self._local_model = WhisperModel(
                    self.cfg.model_size,
                    device=self.cfg.device,
                    compute_type=self.cfg.compute_type,
                )
            except Exception as exc:
                if not self._should_fallback_to_cpu(exc):
                    raise

                # On Windows and other CPU-only systems, auto/cuda can select a GPU
                # backend that is installed without the required CUDA runtime DLLs.
                self._local_model = WhisperModel(
                    self.cfg.model_size,
                    device="cpu",
                    compute_type="int8",
                )

    def _should_fallback_to_cpu(self, error: Exception) -> bool:
        """Return True when model init should retry on CPU instead of failing."""
        if self.cfg.device not in {"auto", "cuda"}:
            return False

        message = str(error).lower()
        cuda_markers = (
            "cublas",
            "cudnn",
            "cudart",
            "cuda",
            "cannot be loaded",
            "load library failed",
        )
        return any(marker in message for marker in cuda_markers)

    # ── Public API ─────────────────────────────────────────────────────────

    def transcribe_live_chunk(self, audio: np.ndarray, sample_rate: int = 16_000) -> str:
        """Transcribe a short audio chunk for live streaming. Always in-process.

        Not supported on Windows where transcription is isolated in a helper
        subprocess to avoid Qt/native library conflicts in the GUI process.
        """
        if self._should_use_subprocess():
            return ""

        if audio.size < sample_rate * 2:  # skip chunks under 2 seconds
            return ""

        # Skip near-total silence
        peak = np.max(np.abs(audio))
        if peak < 0.002:
            return ""

        self._ensure_local_model()
        try:
            segments, _ = self._local_model.transcribe(
                audio,
                beam_size=3,  # balance speed vs accuracy for live
                language=self.cfg.language,
                vad_filter=False,  # we pre-filter silence; let Whisper see everything
            )
            parts = [s.text.strip() for s in segments if s.text.strip()]
            return " ".join(parts)
        except Exception as exc:
            print(f"[Transcriber/live] {exc}")
            return ""

    def transcribe_file(
        self,
        audio_path: Path | str,
        on_segment: Callable[[str], None] | None = None,
    ) -> str:
        """Transcribe an audio file. Returns full transcript text."""
        if self._should_use_subprocess():
            if on_segment:
                on_segment("[Starting Windows transcription helper...]")
            return self._transcribe_file_subprocess(audio_path)

        return self._transcribe_file_inprocess(audio_path, on_segment)

    def _transcribe_file_inprocess(
        self,
        audio_path: Path | str,
        on_segment: Callable[[str], None] | None = None,
    ) -> str:
        self._ensure_local_model()

        segments, info = self._transcribe_segments(str(audio_path))

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
        if self._should_use_subprocess():
            if on_segment:
                on_segment("[Starting Windows transcription helper...]")
            return self._transcribe_array_subprocess(audio, sample_rate)

        return self._transcribe_array_inprocess(audio, sample_rate, on_segment)

    def _transcribe_array_inprocess(
        self,
        audio: np.ndarray,
        sample_rate: int = 16_000,
        on_segment: Callable[[str], None] | None = None,
    ) -> str:
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
        segments, info = self._transcribe_segments(audio)

        parts: list[str] = []
        for segment in segments:
            text = segment.text.strip()
            if text:
                parts.append(text)
                if on_segment:
                    on_segment(text)
        return "\n".join(parts)

    def _transcribe_segments(self, audio_input):
        """Run faster-whisper transcription and retry on CPU if CUDA runtime is unavailable."""
        try:
            return self._local_model.transcribe(
                audio_input,
                beam_size=self.cfg.beam_size,
                language=self.cfg.language,
                vad_filter=self.cfg.vad_filter,
            )
        except Exception as exc:
            if not self._should_fallback_to_cpu(exc):
                raise

            from faster_whisper import WhisperModel

            self._local_model = WhisperModel(
                self.cfg.model_size,
                device="cpu",
                compute_type="int8",
            )
            return self._local_model.transcribe(
                audio_input,
                beam_size=self.cfg.beam_size,
                language=self.cfg.language,
                vad_filter=self.cfg.vad_filter,
            )

    def _should_use_subprocess(self) -> bool:
        """Return True when transcription should run in an isolated helper process."""
        return (
            platform.system() == "Windows"
            and os.environ.get("LIVESCRIBE_TRANSCRIBE_SUBPROCESS") != "1"
        )

    def _transcribe_file_subprocess(self, audio_path: Path | str) -> str:
        """Transcribe using a clean Python subprocess to avoid Qt/native library conflicts."""
        payload = self._run_subprocess(["--input-file", str(audio_path)])
        return payload["text"]

    def _transcribe_array_subprocess(self, audio: np.ndarray, sample_rate: int) -> str:
        """Write audio to a temporary WAV file and transcribe it in a helper subprocess."""
        temp_path = self._write_temp_wav(audio, sample_rate)
        try:
            payload = self._run_subprocess(["--input-file", str(temp_path)])
            return payload["text"]
        finally:
            try:
                temp_path.unlink(missing_ok=True)
            except Exception:
                pass

    def _run_subprocess(self, extra_args: list[str]) -> dict:
        """Execute the transcription helper and return its JSON payload."""
        command = self._build_subprocess_command()
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as handle:
            output_path = Path(handle.name)

        command.extend(["--output-file", str(output_path)])
        if self.cfg.language:
            command.extend(["--language", self.cfg.language])
        if self.cfg.vad_filter:
            command.append("--vad-filter")
        command.extend(extra_args)

        env = os.environ.copy()
        env["LIVESCRIBE_TRANSCRIBE_SUBPROCESS"] = "1"
        env.setdefault("HF_HUB_DISABLE_SYMLINKS_WARNING", "1")

        creationflags = getattr(subprocess, "CREATE_NO_WINDOW", 0) if platform.system() == "Windows" else 0

        try:
            result = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.PIPE,
                text=True,
                env=env,
                creationflags=creationflags,
            )
            if result.returncode != 0:
                message = result.stderr.strip() or (
                    f"Transcription helper failed with exit code {result.returncode}"
                )
                raise RuntimeError(message)

            try:
                return json.loads(output_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError as exc:
                raise RuntimeError("Transcription helper returned invalid output") from exc
        finally:
            try:
                output_path.unlink(missing_ok=True)
            except Exception:
                pass

    def _build_subprocess_command(self) -> list[str]:
        """Build a helper command that works for both Python source runs and frozen app bundles."""
        if getattr(sys, "frozen", False):
            helper_exe = Path(sys.executable).with_name("LiveScribeTranscriber.exe")
            if helper_exe.exists():
                command = [str(helper_exe)]
            else:
                command = [sys.executable, "--transcriber-helper"]
        else:
            command = [sys.executable, "-m", "livescribe.transcriber"]

        command.extend(
            [
                "--model-size",
                self.cfg.model_size,
                "--device",
                self.cfg.device,
                "--compute-type",
                self.cfg.compute_type,
                "--beam-size",
                str(self.cfg.beam_size),
                "--chunk-minutes",
                str(self.cfg.chunk_minutes),
            ]
        )
        return command

    @staticmethod
    def _write_temp_wav(audio: np.ndarray, sample_rate: int) -> Path:
        """Persist a mono WAV to a temp file for subprocess transcription."""
        audio_int16 = np.clip(audio * 32767, -32768, 32767).astype(np.int16)
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as handle:
            temp_path = Path(handle.name)

        with wave.open(str(temp_path), "wb") as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_int16.tobytes())

        return temp_path


def _run_transcriber_cli() -> int:
    """Helper CLI used for isolated transcription on Windows."""
    parser = argparse.ArgumentParser(prog="python -m livescribe.transcriber")
    parser.add_argument("--output-file", required=True)
    parser.add_argument("--input-file", required=True)
    parser.add_argument("--model-size", required=True)
    parser.add_argument("--device", required=True)
    parser.add_argument("--compute-type", required=True)
    parser.add_argument("--beam-size", required=True, type=int)
    parser.add_argument("--chunk-minutes", required=True, type=int)
    parser.add_argument("--language", default=None)
    parser.add_argument("--vad-filter", action="store_true")
    args = parser.parse_args()

    config = TranscriptionConfig(
        model_size=args.model_size,
        device=args.device,
        compute_type=args.compute_type,
        language=args.language,
        beam_size=args.beam_size,
        vad_filter=args.vad_filter,
        chunk_minutes=args.chunk_minutes,
    )
    transcriber = Transcriber(config)
    text = transcriber._transcribe_file_inprocess(args.input_file)
    Path(args.output_file).write_text(json.dumps({"text": text}), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(_run_transcriber_cli())
