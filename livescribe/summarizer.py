"""LLM-powered summarization — supports GitHub Models, Ollama, and OpenAI backends."""

from __future__ import annotations

import json
import threading
from typing import Callable

import requests

from livescribe.config import SummarizerConfig


class Summarizer:
    """Generate meeting summaries from transcript text."""

    def __init__(self, config: SummarizerConfig):
        self.cfg = config

    # ── Public API ─────────────────────────────────────────────────────────

    def summarize(self, transcript: str) -> str:
        """Summarize transcript text. Returns the summary string."""
        if not transcript.strip():
            return ""

        if self.cfg.backend == "copilot":
            return self._summarize_copilot(transcript)
        elif self.cfg.backend == "openai":
            return self._summarize_openai(transcript)
        else:
            return self._summarize_ollama(transcript)

    def summarize_async(
        self,
        transcript: str,
        on_complete: Callable[[str], None] | None = None,
        on_error: Callable[[Exception], None] | None = None,
    ) -> threading.Thread:
        """Run summarization in a background thread."""

        def _worker():
            try:
                result = self.summarize(transcript)
                if on_complete:
                    on_complete(result)
            except Exception as exc:
                if on_error:
                    on_error(exc)

        t = threading.Thread(target=_worker, daemon=True)
        t.start()
        return t

    # ── Copilot CLI backend ────────────────────────────────────────────────

    def _summarize_copilot(self, transcript: str) -> str:
        """Summarize via Copilot CLI (copilot --prompt)."""
        import shutil
        import subprocess

        copilot_bin = shutil.which("copilot")
        if not copilot_bin:
            return "[Copilot CLI not found] Install it from https://github.com/github/copilot-cli"

        prompt = (
            f"{self.cfg.system_prompt}\n\n"
            f"Here is the meeting transcript:\n\n{transcript}"
        )

        try:
            result = subprocess.run(
                [
                    copilot_bin,
                    "--model", self.cfg.copilot_model,
                    "--prompt", prompt,
                    "--allow-all-tools",
                    "--no-color",
                ],
                capture_output=True,
                text=True,
                timeout=180,
            )

            if result.returncode != 0:
                stderr = result.stderr.strip()
                return f"[Copilot CLI error] {stderr or 'Unknown error'}"

            # Parse output — strip the usage stats footer
            output = result.stdout.strip()
            lines = output.split("\n")

            # Find where the stats footer begins (starts with empty line then "Total usage")
            summary_lines = []
            for line in lines:
                if line.strip().startswith("Total usage") or line.strip().startswith("Usage by model"):
                    break
                summary_lines.append(line)

            # Remove trailing empty lines
            while summary_lines and not summary_lines[-1].strip():
                summary_lines.pop()

            return "\n".join(summary_lines).strip()

        except subprocess.TimeoutExpired:
            return "[Copilot CLI timeout] The request took too long"
        except Exception as exc:
            return f"[Copilot CLI error] {exc}"

    # ── Ollama / Local server backend ─────────────────────────────────────

    def _summarize_ollama(self, transcript: str) -> str:
        """Summarize via local server — tries OpenAI-compatible API first, then Ollama native."""
        # Try OpenAI-compatible endpoint first (LM Studio, vLLM, etc.)
        try:
            from openai import OpenAI

            base_url = self.cfg.ollama_url.rstrip("/")
            if not base_url.endswith("/v1"):
                base_url = f"{base_url}/v1"

            client = OpenAI(
                base_url=base_url,
                api_key="local",  # most local servers don't need a real key
            )
            response = client.chat.completions.create(
                model=self.cfg.ollama_model,
                messages=[
                    {"role": "system", "content": self.cfg.system_prompt},
                    {
                        "role": "user",
                        "content": f"Here is the meeting transcript:\n\n{transcript}",
                    },
                ],
                temperature=0.3,
            )
            return response.choices[0].message.content.strip()
        except Exception:
            pass

        # Fall back to native Ollama API
        url = f"{self.cfg.ollama_url}/api/generate"
        prompt = f"{self.cfg.system_prompt}\n\nTranscript:\n{transcript}\n\nSummary:"

        payload = {
            "model": self.cfg.ollama_model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.3},
        }

        try:
            resp = requests.post(url, json=payload, timeout=120)
            resp.raise_for_status()
            return resp.json().get("response", "").strip()
        except requests.ConnectionError:
            return (
                f"[Server not reachable at {self.cfg.ollama_url}]\n"
                "Make sure the server is running."
            )
        except Exception as exc:
            return f"[Summarization error] {exc}"

    # ── OpenAI backend ─────────────────────────────────────────────────────

    def _summarize_openai(self, transcript: str) -> str:
        try:
            from openai import OpenAI

            client = OpenAI(api_key=self.cfg.openai_api_key)
            response = client.chat.completions.create(
                model=self.cfg.openai_model,
                messages=[
                    {"role": "system", "content": self.cfg.system_prompt},
                    {
                        "role": "user",
                        "content": f"Here is the meeting transcript:\n\n{transcript}",
                    },
                ],
                temperature=0.3,
                max_tokens=2048,
            )
            return response.choices[0].message.content.strip()
        except Exception as exc:
            return f"[OpenAI error] {exc}"

    # ── Utility ────────────────────────────────────────────────────────────

    @staticmethod
    def check_ollama(url: str = "http://localhost:11434") -> bool:
        """Return True if Ollama is reachable."""
        try:
            resp = requests.get(url, timeout=3)
            return resp.status_code == 200
        except Exception:
            return False
