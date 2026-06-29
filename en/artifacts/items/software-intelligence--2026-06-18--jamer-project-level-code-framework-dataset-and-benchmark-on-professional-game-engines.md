---
source: arxiv
url: https://arxiv.org/abs/2606.19830v1
published_at: '2026-06-18T06:17:46'
authors:
- Jianwen Sun
- Chuanhao Li
- Zizhen Li
- Yukang Feng
- Fanrui Zhang
- Yifei Huang
- Yu Dai
- Kaipeng Zhang
topics:
- project-level-code-generation
- code-benchmark
- godot
- game-development
- code-agents
- dataset-curation
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# JAMER: Project-Level Code Framework Dataset and Benchmark on Professional Game Engines

## Summary
JAMER introduces JamSet and JamBench, a Godot project-level game code dataset and benchmark built from verified Game Jam projects. It matters for code intelligence because it tests whether models can produce multi-file, runnable game projects, not just short scripts or local edits.

## Problem
- Current game-code benchmarks mostly cover single-file games, web games, local edits, or small task sets, so they miss project-level engineering on a professional engine.
- Game behavior is hard to test with unit tests because interactive runtime behavior has no simple expected output.
- Open-source game repositories are noisy; the authors report that about 96% of candidates failed filtering due to missing files, compile errors, version mismatch, or runtime crashes.

## Approach
- The authors collect about 240,000 candidate repositories, filter for Godot 4.x 2D projects with at least 1,200 game code lines and fewer than 1,000 addon lines, then verify them in Godot headless mode.
- The verification pipeline checks file integrity, compilation, 30-second startup stability, and 60-second runtime behavior collection with deterministic input injection.
- JamBench contains 300 manually verified projects split into Small, Medium, and Large tiers; JamSet contains 7,833 remaining verified projects converted into multi-turn training data.
- The benchmark has two task types: theme-driven full project generation and code completion at function, script, and full-script granularity.
- Evaluation uses pass rates for L1/L2/L3a, Structural Completeness Score for static project shape, and Behavioral Alignment Score for runtime similarity.

## Results
- The pipeline distills 8,133 behavior-valid projects from over 240,000 candidates; 300 form JamBench and 7,833 form JamSet.
- The benchmark is larger than listed prior game-code benchmarks: GameDevBench has 132 tasks, OpenGame has 150 prompts, AutoUE has 20 tasks, and V-GameGym has 2,219 single-file samples.
- On Task 1a theme-only generation, the best plain-model L3a runtime pass rates are 78.7% for Gemini 3.1 Pro, 77.3% for Claude Opus 4.6, and 77.3% for GPT-5.4; BAS remains low, with GPT-5.4 at 0.17 and Gemini 3.1 Pro at 0.14.
- On Task 1b with a gameplay description, Gemini 3.1 Pro reaches 58.7% L3a, 0.57 SCS, and 0.31 BAS; GPT-5.4 reaches 60.7% L3a, 0.63 SCS, and 0.31 BAS.
- On Task 2a, runtime pass rates drop from 80.4% on small projects to 5.7% on large projects, showing a sharp scale failure.
- Code-agent runs raise compilation and runtime pass rates in Task 1, such as Claude Opus 4.6 agent improving Task 1b L3a from 50.0% to 80.0%, but the paper reports no gain in runtime behavioral quality; JamSet fine-tuning improves Qwen3.5-27B Task 1a BAS from 0.09 to 0.21 and L3a from 58.7% to 62.0%.

## Link
- [https://arxiv.org/abs/2606.19830v1](https://arxiv.org/abs/2606.19830v1)
