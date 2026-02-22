# Security Policy

## Supported Versions

We release patches for security vulnerabilities. Currently supported:

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability, please **do not** open a public issue.

Instead, please report it by emailing the maintainers or opening a private security advisory through GitHub's [Security Advisories](https://github.com/appatalks/LiveScribe/security/advisories).

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

We will respond within 48 hours and work with you to understand and address the issue.

## Security Considerations

### API Keys
- **Never commit API keys** to the repository
- LiveScribe stores OpenAI API keys in `~/.livescribe/config.json` (user's home directory)
- API keys can be set via `OPENAI_API_KEY` environment variable
- The config file is excluded from version control

### Local Data
- Audio recordings are kept in memory by default
- Transcripts are only saved when explicitly exported by the user
- Configuration is stored locally in `~/.livescribe/`

### Dependencies
- We use Dependabot to monitor and update dependencies
- Security updates are applied promptly
- Review the dependency list in `requirements.txt` and `pyproject.toml`

### Privacy
- **Local-first**: By default, LiveScribe uses local Whisper models for transcription
- **Optional cloud**: AI summarization can use Copilot CLI, Ollama (local), or OpenAI (cloud)
- **No telemetry**: LiveScribe does not collect or send any usage data

## Best Practices for Users

1. **Protect your API keys**: If using OpenAI backend, keep your API key secure
2. **Use local models**: For maximum privacy, use Ollama backend for fully offline operation
3. **Review recordings**: Be mindful of sensitive content in recordings before sharing exports
4. **Keep updated**: Regularly update to the latest version for security patches
