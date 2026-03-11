# Privacy Policy

**LiveScriber**
*Effective Date: March 9, 2026*
*Last Updated: March 9, 2026*

LiveScriber ("the App") is an open-source desktop and mobile application for audio recording, transcription, and AI-powered summarization. This Privacy Policy explains how the App handles your data.

**Developer:** appatalks
**Contact:** https://github.com/appatalks/LiveScriber/issues
**Source Code:** https://github.com/appatalks/LiveScriber

---

## 1. Information We Collect

### 1.1 Audio Data

The App records audio from your device's microphone (and optionally system audio) when you initiate a recording session. Audio is captured in memory and is **not** automatically saved to permanent storage. Recordings are only saved to your device when you explicitly choose to do so.

### 1.2 Transcripts and Summaries

The App generates text transcripts from your audio recordings and AI-generated summaries from those transcripts. This content exists in memory during your session and is only saved to your device when you explicitly export it.

### 1.3 User Preferences

The App stores your settings (theme, language, selected models, summarization backend) in a local configuration file on your device.

### 1.4 API Keys

If you choose to use the OpenAI summarization backend, your API key is stored locally on your device in the App's configuration file. The App does not transmit your API key to anyone other than the OpenAI API for authentication.

---

## 2. How Your Data Is Processed

### 2.1 Transcription (Always Local)

All speech-to-text transcription is performed **entirely on your device** using the Whisper model. Your audio is **never** sent to any external server for transcription.

### 2.2 Summarization

The App offers multiple summarization backends. The data handling depends on which backend you select:

| Backend | Data Handling |
|---|---|
| **Local (Embedded)** | Runs entirely on your device. No data leaves your device. |
| **Ollama-like** | Sends transcript text to a server URL you configure (typically a local server on your own machine). |
| **GitHub Copilot** | Sends transcript text to GitHub/Microsoft servers via the Copilot CLI. Subject to [GitHub's Privacy Statement](https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement). |
| **OpenAI** | Sends transcript text to OpenAI's API. Subject to [OpenAI's Privacy Policy](https://openai.com/policies/privacy-policy). |

**You choose which backend to use.** The default is the fully offline local backend—no data is shared with any third party unless you explicitly configure a cloud-based backend.

### 2.3 Model Downloads

If you use the embedded local summarization backend, language model files are downloaded from Hugging Face. These downloads are standard file transfers; no personal data is sent. Hugging Face telemetry is explicitly disabled by the App.

### 2.4 Update Checks

When you manually check for updates (via the About tab), the App queries the public GitHub Releases API for version information. No personal data is sent in this request.

---

## 3. Data Storage

All data generated and stored by the App resides **locally on your device**:

| Data | Location |
|---|---|
| Configuration and preferences | `~/.livescriber/config.json` |
| Saved audio recordings | `~/.livescriber/recordings/` |
| Saved summary notes | `~/.livescriber/notes/` |
| Downloaded AI models | `~/.livescriber/models/` |

Session data (in-memory audio, transcripts, and summaries) is **automatically discarded** when you close the App unless you explicitly save it.

---

## 4. Data Sharing

**We do not collect, store, or have access to any of your data.** The App runs on your device and the developer has no server infrastructure that receives your data.

Data is only shared with third-party services when **you** configure and use a cloud-based summarization backend:

- **OpenAI** — if you select the OpenAI backend and provide your own API key
- **GitHub Copilot** — if you select the Copilot backend and authenticate with your own GitHub account
- **Ollama-like server** — if you configure a remote (non-localhost) server URL

In each case, transcript text is sent to the service you selected. Refer to that service's own privacy policy for how they handle the data.

---

## 5. Data Retention

- **On-device data** is retained until you delete it.
- **In-memory session data** is discarded when the App is closed.
- **Data sent to third-party services** (if any) is governed by the respective service's data retention policies. The App does not control data once transmitted.

---

## 6. Data Deletion

You have full control over your data:

- **Delete all App data:** Remove the `~/.livescriber/` directory from your device.
- **Delete saved recordings:** Remove files from `~/.livescriber/recordings/`.
- **Delete saved notes:** Remove files from `~/.livescriber/notes/`.
- **Delete downloaded models:** Remove `~/.livescriber/models/`.
- **Reset configuration:** Delete `~/.livescriber/config.json` — the App will regenerate default settings on next launch.
- **Uninstall the App** to remove the application itself. Note that the data directory (`~/.livescriber/`) is not automatically removed on uninstall; delete it manually for complete removal.

---

## 7. Permissions

The App requests the following permissions:

| Permission | Purpose |
|---|---|
| **Microphone** | Record audio for transcription — core App functionality |
| **Storage** | Save recordings, notes, configuration, and downloaded models to your device |
| **Internet** | Required only for cloud-based summarization backends, model downloads, and manual update checks |

---

## 8. Analytics, Advertising, and Tracking

- **No analytics or telemetry.** The App does not collect usage data, crash reports, or any behavioral information.
- **No advertisements.** The App contains no ads and no ad-related SDKs.
- **No tracking.** The App does not use cookies, device fingerprinting, or any tracking technology.

---

## 9. Children's Privacy

The App does not knowingly collect personal information from children under the age of 13. The App does not require account creation and does not collect any personal information from any user.

---

## 10. Account Information

**No account is required** to use the App. There is no sign-up, login, or user account system within the App itself. If you choose to use a cloud summarization backend, authentication is handled by that external service (e.g., your GitHub account for Copilot, your OpenAI API key for OpenAI).

---

## 11. Security

- API keys are stored locally on your device and are only transmitted to the respective API service for authentication.
- All transcription processing occurs on-device.
- The App is open source — the complete source code is available for review at [github.com/appatalks/LiveScriber](https://github.com/appatalks/LiveScriber).

For security concerns, please see our [Security Policy](SECURITY.md) or report issues via [GitHub Security Advisories](https://github.com/appatalks/LiveScriber/security/advisories).

---

## 12. Changes to This Policy

We may update this Privacy Policy from time to time. Changes will be posted to the [LiveScriber GitHub repository](https://github.com/appatalks/LiveScriber) and the effective date will be updated accordingly. Continued use of the App after changes constitutes acceptance of the updated policy.

---

## 13. Contact Us

If you have questions or concerns about this Privacy Policy, please reach out:

- **GitHub Issues:** https://github.com/appatalks/LiveScriber/issues
- **Repository:** https://github.com/appatalks/LiveScriber

---

*This privacy policy applies to the LiveScriber application distributed via the Google Play Store and all other platforms.*
