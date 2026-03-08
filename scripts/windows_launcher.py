"""PyInstaller launcher for the LiveScribe desktop app."""

import sys

from livescribe.main import main
from livescribe.transcriber import _run_transcriber_cli


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--transcriber-helper":
        del sys.argv[1]
        raise SystemExit(_run_transcriber_cli())

    main()