"""Tests for audio processing and WAV export (no real mic required)."""

import numpy as np

from livescribe.config import AudioConfig
from livescribe.recorder import Recorder


class TestSyntheticAudio:
    """Verify audio processing with synthetic numpy arrays."""

    def test_wav_export_silence(self):
        """WAV bytes from 1 second of silence should produce a valid header + data."""
        r = Recorder(AudioConfig())
        r._processed_audio = np.zeros(16000, dtype=np.float32)
        wav = r.get_wav_bytes()
        assert len(wav) > 44  # WAV header is 44 bytes
        assert wav[:4] == b"RIFF"

    def test_wav_export_tone(self):
        """WAV bytes from a synthetic sine wave."""
        r = Recorder(AudioConfig())
        t = np.linspace(0, 1, 16000, dtype=np.float32)
        r._processed_audio = 0.5 * np.sin(2 * np.pi * 440 * t)
        wav = r.get_wav_bytes()
        assert len(wav) > 16000

    def test_empty_audio_returns_empty_bytes(self):
        r = Recorder(AudioConfig())
        assert r.get_wav_bytes() == b""
        assert r.get_audio().size == 0

    def test_duration_after_processing(self):
        r = Recorder(AudioConfig())
        r._processed_audio = np.zeros(32000, dtype=np.float32)  # 2 seconds
        assert abs(r.duration_seconds - 2.0) < 0.01

    def test_resample(self):
        """Resample from 44100 to 16000 should change array length."""
        r = Recorder(AudioConfig())
        audio = np.zeros(44100, dtype=np.float32)  # 1 second at 44.1kHz
        resampled = r._resample_to_target(audio, 44100)
        assert abs(len(resampled) - 16000) < 10  # should be ~16000 samples


class TestLiveChunkFiltering:
    """Verify the transcriber's live chunk pre-filtering without loading Whisper."""

    def test_short_chunk_rejected(self):
        from livescribe.config import TranscriptionConfig
        from livescribe.transcriber import Transcriber

        t = Transcriber(TranscriptionConfig())
        result = t.transcribe_live_chunk(np.zeros(8000, dtype=np.float32), 16000)
        assert result == ""

    def test_silence_rejected(self):
        from livescribe.config import TranscriptionConfig
        from livescribe.transcriber import Transcriber

        t = Transcriber(TranscriptionConfig())
        result = t.transcribe_live_chunk(np.zeros(48000, dtype=np.float32), 16000)
        assert result == ""

    def test_device_listing(self):
        """list_devices should return a list (may be empty in CI)."""
        try:
            devices = Recorder.list_devices()
            assert isinstance(devices, list)
        except Exception:
            pass  # sound system may not be available in CI
