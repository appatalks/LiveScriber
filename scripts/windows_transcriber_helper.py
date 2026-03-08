"""Console helper entry point for packaged Windows transcription subprocesses."""

from livescribe.transcriber import _run_transcriber_cli


if __name__ == "__main__":
    raise SystemExit(_run_transcriber_cli())