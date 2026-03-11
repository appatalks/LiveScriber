"""PyInstaller launcher for the LiveScriber desktop app."""

import sys

from livescriber.main import main
from livescriber.transcriber import _run_transcriber_cli


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--transcriber-helper":
        del sys.argv[1]
        raise SystemExit(_run_transcriber_cli())

    main()