# LiveScribe

<p align="center">
  <img src="assets/livescribe-banner.png" alt="LiveScribe — Record · Transcribe · Summarize" width="100%">
</p>

A small, floating desktop app that **records**, **transcribes**, and **summarizes** your spoken audio into organized notes — think out loud, troubleshoot problems, capture meetings, or brainstorm ideas and get clean notes automatically.

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS%20%7C%20Windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What It Does

Hit record, talk, stop. LiveScribe transcribes your audio locally with Whisper and generates structured notes using AI. Whether you're:

- **Troubleshooting** — talk through a problem, get organized notes of your thought process
- **Brainstorming** — capture ideas as you speak, get a clean summary
- **In a meeting** — record both sides of the call, get key points and action items
- **Taking voice notes** — quick thoughts while coding, walking, or commuting

The AI adapts its note format to match whatever you're recording.

---

## Features

- **Floating window** — always-on-top, resizable, draggable — invoke it quickly alongside your work
- **One-click recording** — press the red button to capture audio from mic + system audio
- **Dual audio capture** — records your mic and system output (hear both sides of a call)
- **Local transcription** — powered by [faster-whisper](https://github.com/SYSTRAN/faster-whisper) `distil-large-v3` (runs offline, no API key needed)
- **AI-powered notes** — generates structured summaries via Copilot CLI, ollama-like local servers, or OpenAI
- **Embedded local notes** — optional in-app GGUF summarizer with no external server required
- **Copilot CLI backend** (default) — use Claude, GPT-5, or Gemini through your GitHub Copilot subscription
- **Editable notes** — click into the Summary section to add your own annotations
- **Session history** — navigate between past sessions with ◀ ▶ while they're in memory
- **Chunked transcription** — handles recordings up to 5+ hours by splitting into segments
- **Import audio** — bring in existing WAV/MP3/M4A/OGG/FLAC files
- **Save as Markdown** — export transcript + notes to `.md` files
- **Copy All** — one click to clipboard
- **Settings dialog** — configure backend, model, prompt, theme, opacity, and more
- **Dark & light themes** — Catppuccin-inspired color scheme
- **In-memory audio** — recordings stay in RAM, nothing written to disk unless you export

---

## Quick Start

### 1. Install

Linux / macOS:

```bash
git clone https://github.com/appatalks/LiveScribe && cd LiveScribe
./scripts/install.sh
```

Windows PowerShell:

```powershell
git clone https://github.com/appatalks/LiveScribe
cd LiveScribe
.\scripts\install.ps1
```

### Windows Installer Build

If you want a distributable Windows installer instead of a source checkout:

```powershell
.\.venv\Scripts\Activate.ps1
.\scripts\build_windows_installer.ps1
```

This builds:
- a packaged app bundle in `dist\LiveScribe`
- an installer `.exe` in `dist\installer` when [Inno Setup 6](https://jrsoftware.org/isinfo.php) is installed

If Inno Setup is not installed, the script still builds the app bundle and tells you what is missing.

### 2. Run

Linux / macOS:

```bash
source .venv/bin/activate
livescribe
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
livescribe
```

### CLI Options

```
livescribe                          # default (Copilot CLI + local Whisper)
livescribe --backend local          # use embedded GGUF summarizer
livescribe --backend ollama-like    # use a local LLM server for notes
livescribe --backend openai         # use OpenAI directly (needs API key)
livescribe --theme light            # light theme
livescribe --no-on-top              # disable always-on-top
```

---

## How It Works

```
┌─────────────────────────────────────┐
│  LiveScribe              ⚙  ─  ✕   │
│                                     │
│         ┌──────────────┐            │
│         │   ● Record   │            │
│         └──────────────┘            │
│            00:00                    │
│  ────────────────────────────────   │
│       ◀   1/3 • 14:32   ▶          │
│                                     │
│  ▶ Transcription                    │
│    (collapsible transcript)         │
│                                     │
│  ▶ Summary & Notes                  │
│    (collapsible, editable notes)    │
│                                     │
│  [Transcribe]  [Summarize]          │
│  [Import Audio] [Copy All] [Save MD]│
│                                     │
│  Ready — Copilot summarizer         │
└─────────────────────────────────────┘
```

**Workflow:**
1. Click **record** — captures your mic + system audio
2. Click **stop** — audio stays in memory
3. Click **Transcribe** — Whisper processes the audio locally (chunked for long recordings)
4. Click **Summarize** — AI generates organized notes
5. Edit the notes if needed, then **Copy All** or **Save MD**

Use ▶ to start a new session, ◀ to revisit previous ones.

---

## Summarization Backends

### Copilot CLI (default — uses your Copilot subscription)

Requires [Copilot CLI](https://github.com/github/copilot-cli) installed and authenticated.

Available models:
- `claude-sonnet-4.5` (default), `claude-sonnet-4`, `claude-haiku-4.5`
- `gpt-5`, `gpt-5.1`, `gpt-5.1-codex`
- `gemini-3-pro-preview`

### Local (embedded — no server required)

Runs directly inside LiveScribe with `llama.cpp` and downloadable GGUF models.

Included presets:
- `Gemma 2 2B Instruct`
- `Gemma 2 9B Instruct`
- `Llama 3.1 ELM Turbo 4B Instruct`
- `Mistral Nemo 12B Instruct`

Download the selected model from **Settings** when using the `local` backend.
You can also choose the embedded model and local context window there.
On Windows, setup now also attempts to install the embedded llama.cpp runtime automatically.

### Ollama-Like / LM Studio (local, private)

```bash
# Works with any OpenAI-compatible local server
# Configure URL + model in ⚙ Settings
```

### OpenAI (direct)

```bash
export OPENAI_API_KEY="sk-..."
livescribe --backend openai
```

---

## Configuration

Settings are accessible via the **⚙** button in the title bar, or edit `~/.livescribe/config.json` directly.

```json
{
  "audio": {
    "sample_rate": 16000,
    "channels": 1,
    "capture_system_audio": true
  },
  "transcription": {
    "model_size": "distil-large-v3",
    "language": null,
    "chunk_minutes": 10
  },
  "summarizer": {
    "backend": "copilot",
    "copilot_model": "claude-sonnet-4.5",
    "local_model_key": "gemma-2-2b-it",
    "local_context_window": 8192,
    "ollama_url": "http://localhost:11434",
    "ollama_model": "llama3"
  },
  "ui": {
    "window_width": 420,
    "window_height": 620,
    "opacity": 0.95,
    "always_on_top": true,
    "theme": "dark"
  }
}
```

### Whisper Model Sizes

| Model | Size | RAM | Speed | Accuracy |
|-------|------|-----|-------|----------|
| `tiny` | 75 MB | ~1 GB | Fastest | Basic |
| `base` | 142 MB | ~1 GB | Fast | Good |
| `small` | 466 MB | ~2 GB | Medium | Better |
| `distil-large-v3` | 1.5 GB | ~3 GB | Fast | Great (default) |
| `medium` | 1.5 GB | ~5 GB | Slow | Great |
| `large-v3` | 3.1 GB | ~10 GB | Slowest | Best |

---

## Project Structure

```
LiveScribe/
├── livescribe/
│   ├── __init__.py          # Package version
│   ├── main.py              # CLI entry point & arg parsing
│   ├── app.py               # PyQt6 floating window UI + settings dialog
│   ├── recorder.py          # Mic + system audio capture (sounddevice + platform backends)
│   ├── transcriber.py       # Chunked local Whisper transcription
│   ├── summarizer.py        # Copilot CLI / local / ollama-like / OpenAI summarization
│   ├── config.py            # Dataclass config with JSON persistence
│   └── styles.py            # QSS dark/light themes
├── scripts/
│   ├── install.sh           # One-command Linux/macOS setup
│   ├── install.ps1          # One-command Windows setup
│   ├── build_windows_installer.ps1  # Build Windows app bundle + installer
│   └── windows_launcher.py  # PyInstaller launcher entry point
├── installer/
│   └── LiveScribe.iss       # Inno Setup installer definition
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Requirements

- **Python 3.10+**
- **PortAudio** (for microphone access)
  - Linux: `sudo apt install portaudio19-dev`
  - macOS: `brew install portaudio`
  - Windows: included with the `sounddevice` wheel used by this project
- **Copilot CLI** (for default summarization backend — free with Copilot subscription)
- **llama-cpp-python** (installed during setup for the embedded local summarization backend when available)
- **Inno Setup 6** (optional, only if you want to build a Windows installer `.exe`)
- **Ollama-like server or LM Studio** (optional, for fully local/private operation)
- **OpenAI API key** (optional, for direct OpenAI backend)

### System Audio Capture

LiveScribe can capture both your mic and system audio output (e.g., the other side of a call).

**Linux** — works automatically via PulseAudio/PipeWire monitor sources (`parec`).

**macOS** — requires a virtual audio loopback device:

```bash
brew install blackhole-2ch
```

Then open **Audio MIDI Setup** → click **+** → **Create Multi-Output Device** → check both your speakers/headphones and "BlackHole 2ch". Set this as your system output. LiveScribe will automatically detect BlackHole and capture system audio through it.

**Windows** — uses a driver-exposed system-audio input such as `Stereo Mix`, `Wave Out Mix`, or another loopback-style device when available. If your audio driver does not expose one of those inputs, LiveScribe will still record your microphone and continue without system audio.

---

## Support

LiveScribe is free and open source. If it's useful to you, consider supporting development:

| Method | Address |
|--------|---------|
| **PayPal** | [Donate via PayPal](https://www.paypal.com/donate/?hosted_button_id=3KPNXNL6QTZW2) |
| **Bitcoin** | `16CowvxvLSR4BPEP9KJZiR622UU7hGEce5` |
| **Ethereum** | `0xf75278bd6e2006e6ef4847c9a9293e509ab815c5` |

---

## License

MIT
