---
source: hn
url: https://github.com/JitseLambrichts/WTF-CLI
published_at: '2026-03-06T23:46:53'
authors:
- JitseLambrichts
topics:
- cli-tool
- terminal-error-debugging
- developer-tools
- llm-applications
- rust
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Show HN: WTF-CLI – An AI-powered terminal error solver written in Rust

## Summary
This is a command-line wrapper written in Rust: when a terminal command fails, it automatically reads the error output and invokes AI to provide diagnosis and repair suggestions. Its core selling points are seamless integration into existing command workflows and prioritizing local models to protect privacy and reduce costs.

## Problem
- Terminal errors are often fragmented and hard to pinpoint quickly, especially for users unfamiliar with the command line or environment configuration, making troubleshooting costly.
- Existing workflows often require manually copying error messages into a search engine or chat model, interrupting workflow and reducing efficiency.
- For many developers, sending sensitive error logs to the cloud also raises privacy and cost concerns, so a local-first solution is needed.

## Approach
- It works as a minimal CLI wrapper layer: simply prepend `wtf` to the original command. If the command succeeds, output is passed through normally; if it fails, the error output is intercepted and AI analysis is triggered.
- It sends the failed command’s error information to the configured model provider, which returns a structured explanation and executable fix suggestions to help users take the next step directly.
- It supports multiple backends: Ollama is preferred locally, while OpenAI, Gemini, and OpenRouter are also supported as cloud or fallback options.
- It supports interactive configuration via `wtf --setup`, or manual specification of the provider, model, and API key through `.env` / environment variables, lowering the deployment barrier.
- It is implemented in Rust and installed via Cargo, emphasizing lightweight distribution and minimal intrusion into existing shell usage habits.

## Results
- The documentation shows clear usage examples, such as `wtf npm run build` and `wtf ls /fake/directory`, where errors are automatically captured and AI diagnosis and fix suggestions are output when commands fail.
- It claims to provide “seamless wrapping”: successful commands exit normally, while only failed commands trigger AI analysis, without changing the normal command execution path.
- It claims to be “privacy first”: it supports running models locally through Ollama, thereby avoiding API costs and reducing external transmission of error logs.
- It supports 4 types of model providers/backends: Ollama, OpenAI, Gemini, and OpenRouter, and allows switching specific models through environment variables, such as `qwen3.5:9b`, `gpt-4o-mini`, and `gemini-2.0-flash`.
- The provided text **does not give any quantitative experimental results**. It does not report success rate, fix rate, latency, user studies, or baseline comparisons with other terminal assistants/search workflows. It only contains functional and product-level claims.

## Link
- [https://github.com/JitseLambrichts/WTF-CLI](https://github.com/JitseLambrichts/WTF-CLI)
