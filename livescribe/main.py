"""LiveScribe entry point — launch the floating window."""

from __future__ import annotations

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(
        prog="livescribe",
        description="Floating desktop app for meeting transcription & summarization",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Whisper model size for local backend: tiny, base, small, medium, large-v3",
    )
    parser.add_argument(
        "--backend",
        choices=["github", "ollama", "openai", "local"],
        default=None,
        help="Backend for transcription & summarization (default: github)",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="GitHub personal access token (or set GITHUB_TOKEN env var)",
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
    from livescribe.config import AppConfig

    config = AppConfig.load()

    # Apply CLI overrides
    if args.model:
        config.transcription.model_size = args.model
    if args.backend:
        if args.backend == "local":
            config.transcription.backend = "local"
            config.summarizer.backend = "ollama"
        elif args.backend == "github":
            config.transcription.backend = "github"
            config.summarizer.backend = "github"
        elif args.backend == "openai":
            config.transcription.backend = "github"  # still use Whisper via API
            config.summarizer.backend = "openai"
        elif args.backend == "ollama":
            config.transcription.backend = "local"
            config.summarizer.backend = "ollama"
    if args.token:
        config.transcription.github_token = args.token
        config.summarizer.github_token = args.token
    if args.theme:
        config.ui.theme = args.theme
    if args.no_on_top:
        config.ui.always_on_top = False

    # Launch GUI
    from livescribe.app import run_app

    run_app(config)


if __name__ == "__main__":
    main()
