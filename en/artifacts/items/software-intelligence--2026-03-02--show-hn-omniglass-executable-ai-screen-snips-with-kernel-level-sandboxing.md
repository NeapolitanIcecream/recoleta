---
source: hn
url: https://github.com/goshtasb/OmniGlass
published_at: '2026-03-02T23:51:00'
authors:
- goshtasb
topics:
- desktop-ai
- mcp-plugins
- screen-understanding
- sandboxed-execution
- local-llm
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Show HN: OmniGlass – Executable AI screen snips with kernel-level sandboxing

## Summary
OmniGlass is a local open-source platform that turns screen snips directly into executable actions, rather than only providing chat-style responses. It emphasizes zero-trust plugin execution, kernel-level sandboxing, and local OCR / optional local models to reduce the security risks of handing screen content to AI.

## Problem
- Existing desktop AI tools usually can only “look at an image and talk about it,” and cannot turn recognized context directly into executable workflows, which means users still have to manually switch contexts and copy-paste between understanding and action.
- Letting AI plugins or desktop agents run with user privileges creates clear security risks: malicious plugins or prompt injection could read sensitive data such as SSH keys, `.env` files, and browser cookies.
- Building this kind of automation typically requires handling screenshots, OCR, prompt engineering, and tool invocation chains yourself, which raises the barrier to entry and makes it harder to expand the ecosystem quickly.

## Approach
- The core mechanism is simple: the user snips the screen or enters text, the system performs OCR locally, then sends the extracted text to an LLM, which determines the content type and generates a menu of executable actions; execution only happens after the user clicks.
- The overall pipeline is `Screen/Input -> OCR -> LLM classification -> action menu -> execution`; execution can go through either built-in handlers or MCP plugins.
- Plugin development is simplified to “receive structured JSON and then call an API”: OmniGlass handles the earlier screen understanding and prompting flow, so developers mainly need to write the tool interface and permission declarations.
- On security, it centers on zero-trust execution: plugins run inside a kernel-level `sandbox-exec` sandbox and declare permissions such as network access through a manifest, reducing the risk that plugins obtain full user privileges.
- On deployment, it emphasizes local execution and privacy: there are no OmniGlass relay servers, OCR is completed on-device; it can call Claude/Gemini directly, or run local Qwen-2.5-3B offline (via llama.cpp).

## Results
- The article claims the action menu can be returned in **under 1 second** (with the LLM completing classification and generating the executable menu), which is its main interaction performance metric.
- In offline mode without an API key, using **Qwen-2.5-3B + llama.cpp** can complete the “full pipeline” in about **6 seconds**, with the **entire process offline**.
- The core claim about plugin development efficiency is that community example plugins can be kept to **under about 100 lines total**; the Slack plugin shown is basically a single `index.js` plus a manifest.
- The project claims plugin development can go from zero to usable in **5 minutes**, but this is a documentation-level developer experience promise, not a strict experimental result.
- It does not provide standard academic datasets, accuracy, success rates, or quantitative comparisons with baseline systems; the strongest concrete results are mainly the engineering metrics and security claims of **<1 second menu return, ~6 seconds for the fully local offline flow, and kernel-level sandbox isolation**.

## Link
- [https://github.com/goshtasb/OmniGlass](https://github.com/goshtasb/OmniGlass)
