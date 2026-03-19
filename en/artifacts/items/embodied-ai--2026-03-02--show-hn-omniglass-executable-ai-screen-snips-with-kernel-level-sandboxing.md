---
source: hn
url: https://github.com/goshtasb/OmniGlass
published_at: '2026-03-02T23:51:00'
authors:
- goshtasb
topics:
- desktop-ai
- screen-understanding
- mcp-plugins
- sandboxing
- local-first
relevance_score: 0.06
run_id: materialize-outputs
language_code: en
---

# Show HN: OmniGlass – Executable AI screen snips with kernel-level sandboxing

## Summary
OmniGlass is a local-first platform that directly connects “understanding screenshots” to “executable actions,” rather than merely returning text responses. It emphasizes zero-trust execution and plugin-based extensibility, allowing users to trigger automated actions directly from screenshots or text input.

## Problem
- Existing desktop AI tools can usually only “look at an image and chat,” but cannot safely turn recognized context into executable actions.
- Letting plugins or desktop agents run with user-level permissions creates serious security risks, such as reading SSH keys, environment variables, or browser cookies.
- Building this kind of automation typically requires handling screenshots, OCR, prompt engineering, and tool-calling pipelines yourself, making development difficult and unreliable.

## Approach
- The core mechanism is simple: after the user takes a screenshot or enters text, the system first performs OCR locally, then sends the extracted text to an LLM for classification and action generation, and finally presents candidate operations as buttons that execute when clicked.
- The execution layer is based on an MCP (Model Context Protocol) plugin system; plugin developers do not need to write complex prompts, but instead receive structured JSON and then call the target API.
- On security, it centers on a “zero-trust execution engine”: plugins run through built-in handlers or sandboxed MCP plugins, and it claims to use kernel-level sandbox-exec profiles to isolate permissions.
- On privacy, it emphasizes a local-first design: OCR is completed on-device; there are no OmniGlass servers; the API key communicates directly with the model provider; it also supports running Qwen-2.5-3B locally with llama.cpp for a fully offline workflow.

## Results
- It claims the latency from sending OCR text into the LLM to receiving the action menu is **under 1 second**, but provides no standard benchmarks, test conditions, or comparison systems.
- It claims that in a **no API key** scenario, a full offline pipeline can run locally with **Qwen-2.5-3B** via llama.cpp in about **6 seconds**.
- It claims plugins can be extremely lightweight, with community examples positioned as implementable in **under 100 lines** for various workflow automations; the provided Slack example is essentially a minimal MCP tool plus a manifest file.
- The strongest concrete security claim is that if a plugin process can read `~/.ssh/id_rsa`, that would indicate a severe vulnerability; however, the text **does not provide a formal security evaluation, attack success rates, or quantitative comparisons against baselines such as Claude Desktop**.

## Link
- [https://github.com/goshtasb/OmniGlass](https://github.com/goshtasb/OmniGlass)
