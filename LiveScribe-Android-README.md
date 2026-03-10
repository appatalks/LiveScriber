<h1 align="center">LiveScribe Android</h1>

<p align="center">
  <strong>Record &nbsp;→&nbsp; Transcribe &nbsp;→&nbsp; Summarize — entirely on your phone.</strong><br/>
  <sub>The Android companion to <a href="https://github.com/appatalks/LiveScribe">LiveScribe</a>.</sub>
</p>

<p align="center">
  <img alt="Platform" src="https://img.shields.io/badge/Platform-Android-3DDC84?logo=android&logoColor=white"/>
  <img alt="Min SDK" src="https://img.shields.io/badge/Android-8.0%2B%20(API%2026)-brightgreen"/>
  <img alt="Kotlin" src="https://img.shields.io/badge/Kotlin-2.1-7F52FF?logo=kotlin&logoColor=white"/>
  <img alt="Compose" src="https://img.shields.io/badge/Jetpack%20Compose-Material%203-4285F4"/>
</p>

<!-- <p align="center">
  <a href="https://play.google.com/store/apps/details?id=com.livescribe.android">
    <img alt="Get it on Google Play" src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" width="200"/>
  </a>
</p> -->

---

## About

LiveScribe Android brings the full **LiveScribe** experience to your phone — record audio, transcribe it locally on-device with [whisper.cpp](https://github.com/ggerganov/whisper.cpp), and summarize the transcript using your choice of AI backend, including fully offline on-device summarization with [llama.cpp](https://github.com/ggerganov/llama.cpp).

No cloud account required for basic usage. Record, transcribe, and summarize without ever leaving your device.

---

## Features

| | Feature | Description |
|---|---------|-------------|
| 🎙️ | **Microphone recording** | High-quality 16 kHz mono audio capture with background recording support via foreground service |
| 📝 | **On-device transcription** | Local speech-to-text powered by whisper.cpp — no internet needed |
| 🤖 | **AI summarization** | Generate structured meeting notes from transcripts using multiple backend options |
| 📥 | **Audio import** | Import existing WAV, MP3, or M4A files for transcription (auto-converts to the required format) |
| 🌐 | **Multi-language UI** | English, Korean, Japanese, Ukrainian, Spanish, and French — switchable at runtime |
| 🗣️ | **Bilingual summaries** | Generate summaries in two languages simultaneously |
| 🎨 | **Catppuccin theme** | Beautiful Mocha (dark) and Latte (light) color schemes, matching the desktop app |
| 💾 | **Session history** | All recordings, transcripts, and summaries are saved locally and browsable |
| 📤 | **Markdown export** | Export summaries as `.md` files to your device storage |
| 🔒 | **Privacy-first** | Transcription and (optionally) summarization run entirely on-device |

---

## Summarization backends

LiveScribe Android supports the same backends as the desktop app, plus on-device inference:

| Backend | Network required | Description |
|---------|:---:|-------------|
| **Local (on-device)** | ❌ | Runs GGUF language models directly on your phone via llama.cpp. Fully offline. |
| **Ollama-like** | ✅ | Connect to any OpenAI-compatible server — Ollama, LM Studio, vLLM, text-generation-webui, etc. |
| **OpenAI** | ✅ | Use OpenAI's API directly (GPT-4o, etc.) |
| **GitHub Models** | ✅ | Use models hosted on `models.github.ai` |

### On-device models

For fully offline summarization, download a model directly within the app:

| Model | Download size | Best for |
|-------|:---:|----------|
| SmolLM2 360M | ~360 MB | Fastest responses, lower quality |
| Qwen2.5 1.5B | ~1.0 GB | Good balance of speed and quality |
| Gemma 2 2B | ~1.5 GB | Higher quality summaries |
| Phi 3.5 Mini 3.8B | ~2.4 GB | Best quality (needs 4+ GB RAM) |

---

## Transcription options

| Backend | Network required | Description |
|---------|:---:|-------------|
| **Local whisper.cpp** | ❌ | On-device transcription with downloadable model sizes from tiny (39 MB) to medium (769 MB) |
| **OpenAI Transcription** | ✅ | Cloud-based transcription via OpenAI's API |

---

## Requirements

- **Android 8.0** (Oreo, API 26) or higher
- ~100 MB storage for the app + space for downloaded models
- Microphone permission (for recording)

**Recommended for on-device LLM:**
- 4+ GB RAM for larger models
- ARM64 device (arm64-v8a) — covers virtually all modern Android phones

---

## Desktop parity

LiveScribe Android maintains feature parity with the desktop app where it makes sense:

- Same system prompt and summarization output format
- Same Catppuccin color theme
- Same ollama-like, OpenAI, and GitHub Models backend support
- Same markdown export format (summary only)
- **Android extras:** on-device llama.cpp inference, audio import with auto-transcoding, foreground service for background recording

---

## Download

<!-- Uncomment when Play Store listing is live:
<p align="center">
  <a href="https://play.google.com/store/apps/details?id=com.livescribe.android">
    <img alt="Get it on Google Play" src="https://play.google.com/intl/en_us/badges/static/images/badges/en_badge_web_generic.png" width="250"/>
  </a>
</p>
-->

**Play Store release coming soon.** Development builds are available for testing — see below.

---

## Feedback & bug reports

The Android source is currently in a **private repository**. Please submit all feedback through the main LiveScribe project:

- **🐛 Bug reports:** [Open an issue](https://github.com/appatalks/LiveScribe/issues/new?labels=android,bug&template=bug_report.md&title=%5BAndroid%5D+) with the `android` label
- **💡 Feature requests:** [Open an issue](https://github.com/appatalks/LiveScribe/issues/new?labels=android,enhancement&title=%5BAndroid%5D+) with the `android` label

When reporting bugs, please include:
- Device model and Android version
- App version (shown in Settings)
- Steps to reproduce
- Logcat output if available (`adb logcat | grep -i livescribe`)

---

## LiveScribe family

| Platform | Status | Link |
|----------|--------|------|
| 🐧🍎🪟 **Desktop** (Linux, macOS, Windows) | ✅ Released | [LiveScribe](https://github.com/appatalks/LiveScribe) |
| 📱 **Android** | 🔧 In development | Play Store (coming soon) |

---

<p align="center">
  <sub>Built with ❤️ using Kotlin, Jetpack Compose, whisper.cpp, and llama.cpp</sub>
</p>
