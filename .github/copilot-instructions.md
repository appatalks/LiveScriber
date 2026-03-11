# LiveScriber Workspace Instructions

## Project Overview

LiveScriber is a Python desktop app built with PyQt6.
It records audio, transcribes locally with faster-whisper, and summarizes with one of four backends:

- `copilot`
- `local`
- `ollama-like`
- `openai`

Keep changes small, focused, and consistent with the current UI and config model.

## Codebase Priorities

- Preserve Windows support. This repo originally worked on Linux/macOS and now has explicit Windows paths for recording, transcription, and packaging.
- Preserve the current summary export behavior: Markdown export saves the summary only, not the transcript.
- Do not regress backend-specific settings visibility in the Settings dialog. Copilot, embedded local, ollama-like, and OpenAI controls should only appear when relevant.
- Prefer fixing the root cause instead of layering UI-only workarounds.

## Transcription Rules

- `livescriber/transcriber.py` contains important Windows-specific behavior.
- On Windows, transcription must remain isolated from the Qt GUI process.
- Source runs may use `python -m livescriber.transcriber` as the helper path.
- Packaged Windows builds must prefer the sibling helper executable `LiveScriberTranscriber.exe`.
- Do not change packaged helper invocation back to `LiveScriber.exe -m livescriber.transcriber ...`; that breaks in frozen builds.
- CPU fallback for missing CUDA runtime DLLs is intentional and should remain in place.

## Recording Rules

- `livescriber/recorder.py` includes Windows-specific system audio detection.
- On Windows, system audio may come from `Stereo Mix`, `Wave Out Mix`, `What U Hear`, or another loopback-style input.
- Do not assume WASAPI loopback devices always exist.

## Summarization Rules

- Canonical backend name is `ollama-like`. Older `ollama` values are compatibility aliases and should continue to normalize to `ollama-like`.
- Embedded local summarization uses `llama.cpp` through `llama-cpp-python`.
- Keep the local model catalog valid against public GGUF repos and current runtime compatibility.
- Avoid adding `Qwen3` local embedded models unless runtime compatibility is explicitly verified first.
- Current embedded presets are:
  - `Gemma 2 2B Instruct`
  - `Gemma 2 9B Instruct`
  - `Llama 3.1 ELM Turbo 4B Instruct`
  - `Mistral Nemo 12B Instruct`
- Local model downloads should keep Hugging Face progress bars disabled in app-managed flows. This avoids packaged GUI crashes caused by missing stderr/progress streams.

## Settings Dialog Rules

- `livescriber/app.py` `SettingsDialog` is backend-sensitive.
- Hide irrelevant groups instead of only disabling them.
- Current intent:
  - Copilot group visible only for `copilot`
  - Embedded local group visible only for `local`
  - Ollama-like server group visible only for `ollama-like`
  - OpenAI API key group visible only for `openai`
- The embedded local section should expose both model selection and local context window.

## Packaging Rules

- Windows packaging is handled by `scripts/build_windows_installer.ps1`.
- The build should produce:
  - `dist/LiveScriber/LiveScriber.exe`
  - `dist/LiveScriber/LiveScriberTranscriber.exe`
  - `dist/installer/LiveScriber-Setup-<version>.exe`
- `installer/LiveScriber.iss` is the Inno Setup definition.
- Keep the dedicated transcription helper executable in the packaged output.
- Be careful with PyInstaller collection scope. Broad `--collect-all` usage makes the build much larger and noisier.

## Installer and Setup Rules

- `scripts/install.ps1` is the Windows source-setup path.
- `scripts/install.sh` is the Linux/macOS source-setup path.
- The embedded local runtime is optional in packaging metadata and installed during setup when possible.
- Do not move `llama-cpp-python` back into mandatory base dependencies.

## Validation Shortcuts

When making risky changes, prefer quick targeted validation:

- Syntax/editor check with workspace diagnostics.
- GUI smoke tests using a small `QApplication` script.
- Synthetic audio transcription tests with `numpy.zeros(...)`.
- Local summarization smoke tests through the actual `Summarizer` path.
- For packaged Windows transcription issues, test the frozen subprocess path explicitly, not just the source path.

## Known Good Expectations

- Packaged Windows transcription should route through `LiveScriberTranscriber.exe`.
- Local downloads should succeed without progress-bar errors in packaged builds.
- The Settings dialog should resize cleanly when backend-specific groups are shown or hidden.
- The current local config may be migrated on load to keep old keys working.

## Editing Style

- Preserve existing naming and structure unless there is a clear reason to refactor.
- Avoid unrelated reformatting.
- Keep comments sparse and only where they explain non-obvious platform-specific behavior.