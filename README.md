# LiveScribe

A small, floating desktop app for **recording**, **transcribing**, and **summarizing** meetings and audio — like Copilot in Teams, but cross-platform.

Uses your **GitHub Copilot subscription** for high-accuracy Whisper transcription and GPT-4o summarization via [GitHub Models](https://github.com/marketplace/models) — no extra API keys needed.

![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20macOS-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

---

## Features

- **Floating window** — always-on-top, draggable, minimal UI you can invoke quickly
- **One-click recording** — press the red button to capture audio from your mic
- **GitHub Models transcription** (default) — cloud Whisper via your Copilot subscription for high accuracy
- **GitHub Models summarization** (default) — GPT-4o generates structured meeting summaries with key points, decisions, and action items
- **Local fallback** — optional offline transcription via [faster-whisper](https://github.com/SYSTRAN/faster-whisper) + [Ollama](https://ollama.com) summarization
- **Multiple backends** — GitHub Models (default), OpenAI direct, or fully local (Ollama + faster-whisper)
- **Import audio** — drag in existing WAV/MP3/M4A/OGG/FLAC files
- **Copy all** — one click to copy transcript + summary to clipboard
- **Save as Markdown** — export notes with transcript, summary, and metadata to `.md` files
- **Dark & light themes** — Catppuccin-inspired color scheme
- **Configurable** — backend, language, always-on-top, opacity, and more via `~/.livescribe/config.json`

---

## Quick Start

### 1. Install

```bash
# Clone the repo
git clone <your-repo-url> LiveScribe && cd LiveScribe

# Run the install script (creates venv, installs deps)
./scripts/install.sh
```

### 2. Run

```bash
source .venv/bin/activate
livescribe
```

### CLI Options

```
livescribe                          # default (GitHub Models backend)
livescribe --token ghp_xxxx         # pass GitHub token directly
livescribe --backend local          # fully offline (faster-whisper + Ollama)
livescribe --backend ollama         # local transcription + Ollama summaries
livescribe --backend openai         # Whisper API + OpenAI summaries
livescribe --theme light            # light theme
livescribe --no-on-top              # disable always-on-top
```

---

## How It Works

```
┌─────────────────────────────────────┐
│         LiveScribe Window           │
│                                     │
│         ┌──────────────┐            │
│         │   ● Record   │            │
│         └──────────────┘            │
│            00:00                    │
│  ────────────────────────────────   │
│  ▶ Transcription                    │
│    (collapsible live transcript)    │
│                                     │
│  ▶ Summary & Notes                  │
│    (collapsible AI summary)         │
│                                     │
│  [Transcribe]  [Summarize]          │
│  [Import Audio]  [Copy All]         │
│                                     │
│  Ready                              │
└─────────────────────────────────────┘
```

**Workflow:**
1. Click the **record** button to capture audio from your microphone
2. Click **stop** when done — audio saves to `~/.livescribe/recordings/`
3. Click **Transcribe** — Whisper processes the audio (via GitHub Models or locally)
4. Click **Summarize** — GPT-4o generates a structured summary
5. Click **Copy All** to grab everything for your notes

---

## Backends

### GitHub Models (default — uses your Copilot subscription)

```bash
# Set your GitHub personal access token
export GITHUB_TOKEN="ghp_..."
livescribe

# Or pass it directly
livescribe --token ghp_...
```

Create a token at [github.com/settings/tokens](https://github.com/settings/tokens) with no special scopes — just needs basic access to GitHub Models.

### Ollama (fully local, free)

```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama3

# Run fully offline
livescribe --backend local
```

### OpenAI (direct)

```bash
export OPENAI_API_KEY="sk-..."
livescribe --backend openai
```

---

## Configuration

Config is stored at `~/.livescribe/config.json` and is created on first run. You can edit it directly or use CLI flags.

```json
{
  "audio": {
    "sample_rate": 16000,
    "channels": 1
  },
  "transcription": {
    "backend": "github",
    "github_model": "openai/whisper-large-v3-turbo",
    "github_base_url": "https://models.inference.ai.azure.com",
    "model_size": "base",
    "language": null
  },
  "summarizer": {
    "backend": "github",
    "github_model": "openai/gpt-4o-mini",
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

### Whisper Model Sizes (local backend only)

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
│   ├── app.py               # PyQt6 floating window UI
│   ├── recorder.py          # Audio capture via sounddevice
│   ├── transcriber.py       # GitHub Models Whisper / local faster-whisper
│   ├── summarizer.py        # GitHub Models / Ollama / OpenAI summarization
│   ├── config.py            # Dataclass config with persistence
│   └── styles.py            # QSS dark/light themes
├── scripts/
│   └── install.sh           # One-command setup
├── pyproject.toml            # Package metadata & deps
├── requirements.txt
└── README.md
```

---

## Requirements

- **Python 3.10+**
- **PortAudio** (for microphone access)
  - Linux: `sudo apt install portaudio19-dev`
  - macOS: `brew install portaudio`
- **GitHub personal access token** (for default GitHub Models backend — free with Copilot)
- **Ollama** (optional, for fully local operation)
- **OpenAI API key** (optional, for direct OpenAI backend)
- **faster-whisper** (optional, for local transcription: `pip install faster-whisper`)

---

## License

MIT
