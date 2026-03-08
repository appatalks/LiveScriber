"""Console helper entry point for packaged Windows transcription subprocesses."""

import os
os.environ.setdefault("HF_HUB_DISABLE_XET", "1")
os.environ.setdefault("HF_HUB_DISABLE_TELEMETRY", "1")

from livescribe.transcriber import _run_transcriber_cli


if __name__ == "__main__":
    raise SystemExit(_run_transcriber_cli())