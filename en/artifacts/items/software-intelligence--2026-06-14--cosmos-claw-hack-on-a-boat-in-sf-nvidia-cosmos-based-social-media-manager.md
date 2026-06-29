---
source: hn
url: https://github.com/manas15/cosmos-claw
published_at: '2026-06-14T23:57:59'
authors:
- manas95
topics:
- agentic-video-generation
- social-media-automation
- multimodal-ai
- self-hosted-inference
- venue-marketing
relevance_score: 0.83
run_id: materialize-outputs
language_code: en
---

# Cosmos Claw: Hack on a Boat in SF (Nvidia Cosmos Based Social Media Manager)

## Summary
Cosmos Claw is an agentic social-video generator for venues. It turns existing photos and venue facts into branded short-form posts, voiceover, captions, and video cuts with no human film crew.

## Problem
- Venues need a steady flow of short videos to keep attention on Reels, TikTok, Shorts, and similar feeds.
- Manual production is slow, expensive, and hard to keep consistent across formats and posts.

## Approach
- It starts from uploaded venue photos and facts, then uses GPT-4o vision to label the assets and build a brand dossier with stable assumptions.
- A manager agent researches the venue and nearby area, then writes a fresh campaign plan for each post: angle, hook, asset order, format, music, voice, and caption.
- NVIDIA Cosmos 3 Nano generates short first-person motion clips from the selected photos, self-hosted on Nebius H200 NVLink GPUs through vLLM-Omni.
- The pipeline adds GPT-written voiceover, mood-matched music, cross-fades, and aspect-ratio handling, then outputs ready-to-post packages.
- The system runs as a loop, with one worker per venue, persistent memory in a brand dossier, and resume-on-reconnect behavior for network blips.

## Results
- The paper does not report benchmark numbers, accuracy scores, or user-study results.
- It claims the system can generate ready-to-post social videos for multiple venues in parallel.
- It says two workers were running at once for two San Francisco venues, each producing its own ready-to-post Reels and TikToks.
- It says the system can continue after a Wi-Fi or tunnel interruption by pausing and resuming automatically.
- It claims one uploaded photo set is enough to drive repeated branded video generation across formats such as 9:16, 1:1, 4:5, and 16:9.

## Link
- [https://github.com/manas15/cosmos-claw](https://github.com/manas15/cosmos-claw)
