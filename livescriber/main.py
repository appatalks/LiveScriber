"""LiveScriber entry point — launch the floating window."""

from __future__ import annotations

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="livescriber",
        description="Floating desktop app for meeting transcription & summarization",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Whisper model size for local backend: tiny, base, small, medium, large-v3",
    )
    parser.add_argument(
        "--backend",
        choices=["copilot", "local", "ollama-like", "ollama", "openai"],
        default=None,
        help="Summarization backend (default: local)",
    )
    parser.add_argument(
        "--theme",
        choices=["dark", "light"],
        default=None,
        help="UI theme (default: dark)",
    )
    parser.add_argument(
        "--no-on-top",
        action="store_true",
        help="Disable always-on-top window behavior",
    )

    args = parser.parse_args()

    # Load config (persisted or defaults)
    from livescriber.config import AppConfig

    config = AppConfig.load()

    # Apply CLI overrides
    if args.model:
        config.transcription.model_size = args.model
    if args.backend:
        config.summarizer.backend = "ollama-like" if args.backend == "ollama" else args.backend
    if args.theme:
        config.ui.theme = args.theme
    if args.no_on_top:
        config.ui.always_on_top = False

    # Launch GUI
    from livescriber.app import run_app

    run_app(config)


if __name__ == "__main__":
    main()
