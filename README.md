# LiveScribe

<p align="center">
  <img src="assets/livescribe-banner.png" alt="LiveScribe — Record · Transcribe · Summarize" width="100%">
</p>

A floating desktop app that turns your voice into organized notes. Hit record, talk, and get clean notes automatically — no typing required.

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## How It Works

1. **Record** — click the mic button to start capturing audio
2. **Stop** — click again to stop
3. **Transcribe** — converts your speech to text (runs locally, no internet needed)
4. **Summarize** — AI organizes your words into clean, structured notes
5. **Export** — copy to clipboard or save as a Markdown file

Works great for meetings, brainstorming, voice notes, troubleshooting sessions, or any time you'd rather talk than type.

---

## Install

### Windows

Download the installer from the [latest release](https://github.com/appatalks/LiveScribe/releases), run it, and you're done.

Or install from source:

```powershell
git clone https://github.com/appatalks/LiveScribe
cd LiveScribe
.\scripts\install.ps1
```

Then run:

```powershell
.\.venv\Scripts\Activate.ps1
livescribe
```

### macOS

```bash
git clone https://github.com/appatalks/LiveScribe && cd LiveScribe
./scripts/install.sh
```

Then run:

```bash
source .venv/bin/activate
livescribe
```

> **Tip:** To capture both sides of a call on macOS, install [BlackHole](https://existential.audio/blackhole/) (`brew install blackhole-2ch`) and set up a Multi-Output Device in Audio MIDI Setup.

### Linux

```bash
git clone https://github.com/appatalks/LiveScribe && cd LiveScribe
./scripts/install.sh
```

Then run:

```bash
source .venv/bin/activate
livescribe
```

System audio capture works automatically on Linux via PulseAudio/PipeWire.

---

## Features

- **Always-on-top floating window** — stays visible alongside your other apps
- **Records mic + system audio** — captures both sides of calls
- **Offline transcription** — powered by Whisper, runs locally on your machine
- **AI-powered notes** — generates summaries using a built-in local model (no account needed)
- **Multiple AI backends** — also supports Copilot CLI, Ollama, LM Studio, and OpenAI
- **Session history** — flip between past recordings with ◀ ▶
- **Import audio files** — drag in WAV, MP3, M4A, or other formats
- **Dark & light themes** — switch in Settings
- **Everything configurable** — model size, backend, prompt, opacity, and more via ⚙ Settings

---

## Settings

Click the **⚙** gear icon in the title bar to configure:

- **Whisper model** — choose transcription accuracy vs. speed
- **Summarization backend** — local (default), Copilot CLI, Ollama-like server, or OpenAI
- **System audio** — toggle capturing speaker output
- **Theme** — dark or light
- **Opacity** — make the window semi-transparent
- **Always on top** — keep window above other apps

All settings are saved automatically between sessions.

---

## Technical Documentation

For advanced configuration, backend details, CLI options, build instructions, and project structure, see [DOCS.md](DOCS.md).

---

## Support

LiveScribe is free and open source. If it's useful to you, consider supporting development:

| Method | |
|--------|---|
| **PayPal** | [Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=3KPNXNL6QTZW2) |
| **Bitcoin** | `16CowvxvLSR4BPEP9KJZiR622UU7hGEce5` |
| **Ethereum** | `0xf75278bd6e2006e6ef4847c9a9293e509ab815c5` |

---

## License

MIT
