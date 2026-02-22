"""Application configuration with sensible defaults."""

from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass, field, asdict
from pathlib import Path

# ── Paths ──────────────────────────────────────────────────────────────────────
APP_DIR = Path.home() / ".livescribe"
RECORDINGS_DIR = APP_DIR / "recordings"
CONFIG_PATH = APP_DIR / "config.json"


@dataclass
class AudioConfig:
    sample_rate: int = 16_000       # 16 kHz – Whisper's native rate
    channels: int = 1               # mono
    dtype: str = "float32"
    block_duration_ms: int = 30_000  # chunk size for streaming transcription
    capture_system_audio: bool = True  # also capture system audio output (speakers)


@dataclass
class TranscriptionConfig:
    backend: str = "local"            # local | github
    # Local faster-whisper settings
    model_size: str = "distil-large-v3"  # tiny | base | small | medium | large-v3 | distil-large-v3
    device: str = "auto"             # auto | cpu | cuda
    compute_type: str = "int8"       # int8 | float16 | float32
    language: str | None = None      # None = auto-detect
    beam_size: int = 5
    vad_filter: bool = False         # voice-activity-detection filter (can drop quiet audio)
    # GitHub Models settings (used when backend="github")
    github_token: str = ""
    github_model: str = "openai/whisper-large-v3-turbo"  # Whisper on GitHub Models
    github_base_url: str = "https://models.inference.ai.azure.com"


@dataclass
class SummarizerConfig:
    backend: str = "github"          # github | ollama | openai
    # GitHub Models settings (free with Copilot subscription)
    github_token: str = ""           # same token as transcription
    github_model: str = "gpt-5-chat"
    github_base_url: str = "https://models.inference.ai.azure.com"
    # Ollama settings
    ollama_url: str = "http://localhost:11434"
    ollama_model: str = "llama3"
    # OpenAI settings (direct, not via GitHub)
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    # Prompt
    system_prompt: str = (
        "You are a professional meeting note-taker. Given a transcript, produce a structured summary. "
        "Include: 1) A brief overview (2-3 sentences), 2) Key discussion points as bullet points, "
        "3) Decisions made, 4) Action items with owners if mentioned. "
        "Be concise and factual. Do NOT ask questions, add commentary, or include anything "
        "not discussed in the transcript. Output only the summary."
    )


@dataclass
class UIConfig:
    window_width: int = 420
    window_height: int = 620
    opacity: float = 0.95
    always_on_top: bool = True
    theme: str = "dark"              # dark | light


@dataclass
class AppConfig:
    audio: AudioConfig = field(default_factory=AudioConfig)
    transcription: TranscriptionConfig = field(default_factory=TranscriptionConfig)
    summarizer: SummarizerConfig = field(default_factory=SummarizerConfig)
    ui: UIConfig = field(default_factory=UIConfig)

    # ── Persistence ────────────────────────────────────────────────────────

    def save(self) -> None:
        APP_DIR.mkdir(parents=True, exist_ok=True)
        CONFIG_PATH.write_text(json.dumps(asdict(self), indent=2))

    @classmethod
    def load(cls) -> "AppConfig":
        cfg = cls()
        if CONFIG_PATH.exists():
            try:
                data = json.loads(CONFIG_PATH.read_text())
                cfg.audio = AudioConfig(**data.get("audio", {}))
                cfg.transcription = TranscriptionConfig(**data.get("transcription", {}))
                cfg.summarizer = SummarizerConfig(**data.get("summarizer", {}))
                cfg.ui = UIConfig(**data.get("ui", {}))
            except Exception:
                pass  # fall back to defaults
        # Env-var overrides
        if key := os.environ.get("GITHUB_TOKEN"):
            cfg.transcription.github_token = key
            cfg.summarizer.github_token = key
        if key := os.environ.get("OPENAI_API_KEY"):
            cfg.summarizer.openai_api_key = key

        # Auto-detect token from gh CLI if still empty
        if not cfg.transcription.github_token:
            if token := _get_gh_cli_token():
                cfg.transcription.github_token = token
                cfg.summarizer.github_token = token

        return cfg


def _get_gh_cli_token() -> str | None:
    """Try to retrieve a GitHub token from the gh CLI."""
    gh = shutil.which("gh")
    if not gh:
        return None
    try:
        result = subprocess.run(
            [gh, "auth", "token"],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            token = result.stdout.strip()
            if token:
                return token
    except Exception:
        pass
    return None
