---
source: hn
url: https://github.com/aarifmms/keyblind
published_at: '2026-05-26T22:47:33'
authors:
- aarifshaikhs
topics:
- ai-agent-security
- secrets-management
- mcp
- developer-tools
- code-intelligence
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Keyblind – encrypted secrets vault that hides API keys from AI agents

## Summary
Keyblind is a local encrypted secrets vault for AI coding agents. It keeps real API keys out of model context by giving agents fake `.env` values and resolving secrets only when commands run.

## Problem
- AI coding tools can read `.env` files and send API keys, tokens, and passwords into LLM conversations or commits.
- The excerpt cites 100,000+ LLM conversations with exposed secrets indexed by search engines in 2025.
- Leaked secrets can lead to account takeover, cloud spend, data exposure, and compromised software delivery.

## Approach
- Keyblind stores secrets in a local SQLite vault encrypted with AES-256-GCM.
- It derives encryption keys with PBKDF2 using 600K iterations, then wraps the key with a machine fingerprint.
- An MCP server exposes 6 tools so agents can list or resolve secret names without seeing plaintext in the transcript.
- `keyblind sandbox` replaces `.env` values with deterministic HMAC-SHA256 fakes per project and key name.
- `keyblind run -- <command>` injects real secrets as environment variables at runtime.

## Results
- The excerpt reports no benchmark, user study, attack evaluation, or comparison against tools such as 1Password CLI, Bitwarden CLI, or dotenv vaults.
- It claims support for any MCP-compatible editor, including Claude Code, Cursor, Windsurf, Copilot, Cline, and Zed.
- It claims zero network access, zero telemetry, no cloud account, and a local vault stored under `~/.keyblind/` with `0700` permissions.
- It claims multiple secret backends, including the built-in encrypted vault, 1Password, and Bitwarden.
- Security-relevant numbers given are AES-256-GCM encryption, PBKDF2 with 600K iterations, 6 MCP tools, and 100,000+ exposed LLM conversations as the motivating incident scale.

## Link
- [https://github.com/aarifmms/keyblind](https://github.com/aarifmms/keyblind)
