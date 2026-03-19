---
source: hn
url: https://github.com/JitseLambrichts/WTF-CLI
published_at: '2026-03-06T23:46:53'
authors:
- JitseLambrichts
topics:
- cli-tooling
- terminal-error-diagnosis
- rust
- local-llm
- developer-tools
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# Show HN: WTF-CLI – An AI-powered terminal error solver written in Rust

## Summary
WTF-CLI is a command-line wrapper written in Rust: when a terminal command fails, it automatically intercepts the error output and invokes a local or cloud-based large model to generate fix suggestions. It targets common CLI error-diagnosis scenarios for developers, emphasizing a low-friction user experience and a local-first privacy approach.

## Problem
- When terminal commands fail, developers usually need to manually read the error, search for the cause, and then try a fix, which is time-consuming and interrupts workflow.
- Many AI-assisted tools are not directly embedded into the shell command execution path, so there is still significant operational overhead between “an error occurs” and “getting an executable fix suggestion.”
- For sensitive code or local environment issues, sending error logs to the cloud can also raise privacy and cost concerns, so a local-first error analysis solution is needed.

## Approach
- The core mechanism is very simple: write ordinary commands as `wtf <your-command>`; if the command succeeds, it exits just like normal execution; if it fails, it captures the error context from stderr/stdout.
- The tool sends the failed output to the configured AI provider, allowing the model to generate a structured diagnosis and executable fix commands, which are returned directly to the user in the terminal.
- It defaults to a local-model workflow, prioritizing support for running local models through Ollama to achieve “no API cost + stronger privacy protection.”
- It also provides cloud fallback options, supporting OpenAI, Gemini, and OpenRouter, which can be switched quickly via `wtf --setup` or environment variables.
- In implementation terms, it is packaged as a standalone CLI using Rust/Cargo, with the goal of embedding into developers’ existing command-line habits with minimal changes.

## Results
- The text does not provide standard paper-style quantitative experimental results, so there are no benchmark data, accuracy metrics, speed figures, or user-study numbers to report.
- The strongest concrete product claim given is: simply prepend `wtf` to the original command to achieve a seamless wrapper experience of “analyze on failure, pass through transparently on success.”
- It supports **4 model provider categories**: Ollama, OpenAI, Gemini, and OpenRouter; among them, the default local example model is `qwen3.5:9b`, and cloud examples include `gpt-4o-mini`, `gemini-2.0-flash`, and `arcee-ai/trinity-mini:free`.
- The example failure scenarios given include **2 cases**: `wtf npm run build` and `wtf ls /fake/directory`, indicating that its target coverage includes build errors and file-system command error diagnosis.
- The project claims that its output has a “clear structure” and “executable fix commands,” and emphasizes practical value such as **privacy first**, local execution, and no API cost (when using Ollama).

## Link
- [https://github.com/JitseLambrichts/WTF-CLI](https://github.com/JitseLambrichts/WTF-CLI)
