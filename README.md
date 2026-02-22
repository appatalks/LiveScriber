# LiveScribe

A small, floating desktop app that **records**, **transcribes**, and **summarizes** your spoken audio into organized notes — think out loud, troubleshoot problems, capture meetings, or brainstorm ideas and get clean notes automatically.

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey)
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
- **AI-powered notes** — generates structured summaries via Copilot CLI, Ollama, or OpenAI
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

```bash
git clone https://github.com/appatalks/LiveScribe && cd LiveScribe
./scripts/install.sh
```

### 2. Run

```bash
source .venv/bin/activate
livescribe
```

### CLI Options

```
livescribe                          # default (Copilot CLI + local Whisper)
livescribe --backend ollama         # use local LLM server for notes
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

### Ollama / LM Studio (local, private)

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
│   ├── recorder.py          # Mic + system audio capture (sounddevice + parec)
│   ├── transcriber.py       # Chunked local Whisper transcription
│   ├── summarizer.py        # Copilot CLI / Ollama / OpenAI summarization
│   ├── config.py            # Dataclass config with JSON persistence
│   └── styles.py            # QSS dark/light themes
├── scripts/
│   └── install.sh           # One-command Linux/macOS setup
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
- **Copilot CLI** (for default summarization backend — free with Copilot subscription)
- **Ollama or LM Studio** (optional, for fully local/private operation)
- **OpenAI API key** (optional, for direct OpenAI backend)

---

## License

MIT
