---
source: hn
url: https://github.com/ayushh0110/ScreenMind
published_at: '2026-06-13T23:12:54'
authors:
- skye0110
topics:
- screen-memory
- local-ai
- multimodal-llm
- privacy
- search
- agent-automation
relevance_score: 0.71
run_id: materialize-outputs
language_code: en
---

# Show HN: I run a vision model on every screenshot, locally, on a 4GB GPU

## Summary
ScreenMind is a local screen-memory app that captures screenshots, analyzes them with Gemma 4, and lets you search, chat with, and build automations on top of your activity history. It matters because it targets the same use case as screen-aware assistants like Recall, but keeps data on-device and adds redaction, encryption, and local search.

## Problem
- Screen-aware assistants need to record and understand what happens on your computer across apps, meetings, and voice notes.
- Existing approaches raise privacy and trust issues when they store data plainly or send it to cloud services.
- Users also need a way to search old screen activity by meaning, not just by file name or exact text.

## Approach
- Capture screenshots only when screen content changes, then skip duplicates with perceptual hashing and app-aware caching.
- Send each screenshot, plus OCR text, to Gemma 4 E2B for structured vision analysis such as app name, activity category, summary, mood, scene description, and layout regions.
- Combine EasyOCR, MiniLM embeddings, and SQLite FTS5 so search can use both semantic similarity and keyword matching.
- Add voice memo and meeting transcription with Gemma 4's audio encoder, then store summaries and metadata locally.
- Expose the stored history through chat, REST API, MCP, and plugin agents for custom automation.

## Results
- The project claims 100% local processing with zero cloud dependencies after the initial model download.
- It reports three analysis modes: Accurate at about 76s per screenshot, Balanced at about 40s, and Fast at about 12s.
- It says the system runs on a 4GB+ GPU and needs about 5GB of disk space for the model.
- It claims fewer inference calls through a 3-tier per-app pHash cache and faster GPU release, with chat canceling in-flight analysis in under 1 second.
- No benchmark table or external evaluation numbers are provided in the excerpt, so the strongest claims are the local-private workflow, multimodal screen understanding, and automation support.

## Link
- [https://github.com/ayushh0110/ScreenMind](https://github.com/ayushh0110/ScreenMind)
