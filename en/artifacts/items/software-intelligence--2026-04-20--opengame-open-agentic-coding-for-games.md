---
source: arxiv
url: http://arxiv.org/abs/2604.18394v1
published_at: '2026-04-20T15:17:03'
authors:
- Yilei Jiang
- Jinyuan Hu
- Qianyin Xiao
- Yaozhi Zheng
- Ruize Ma
- Kaituo Feng
- Jiaming Han
- Tianshuo Peng
- Kaixuan Fan
- Manyuan Zhang
- Xiangyu Yue
topics:
- agentic-coding
- game-generation
- code-intelligence
- software-engineering-agents
- benchmarking
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# OpenGame: Open Agentic Coding for Games

## Summary
OpenGame is an open-source agentic system for turning natural-language game ideas into playable 2D web games. It combines a game-specialized code model, reusable project templates, and an accumulated debugging protocol, then evaluates outputs with a benchmark built for interactive game generation.

## Problem
- Existing LLMs and code agents can write isolated code well, but they often fail to build a full playable game with consistent logic, scene wiring, assets, and multi-file state.
- Game generation is harder than standard code generation because correctness depends on runtime behavior, visual interactivity, and engine-specific structure, not only whether code compiles.
- This matters because game development is a hard case for automated software production: if agents cannot manage long-horizon, cross-file, interactive systems, they will keep failing on many real software tasks with similar integration demands.

## Approach
- OpenGame uses **Game Skill**, which has two parts: **Template Skill** and **Debug Skill**. Template Skill grows a library of reusable game skeletons, and Debug Skill stores verified failure signatures, causes, and fixes so the agent can reuse past repairs.
- The agent follows a six-phase workflow: classify the game type, scaffold the project, generate a game design document, create assets, implement code with template extension points, then run build/test/repair loops.
- Its base model, **GameCoder-27B**, is trained on top of Qwen3.5-27B with three stages: continual pre-training on Phaser and web-game code, supervised fine-tuning on synthesized game-design tasks, and execution-grounded reinforcement learning on tested gameplay modules.
- To keep generation stable, the system uses archetype-specific templates, a three-layer file-reading strategy, data-driven config updates, and repeated headless verification instead of one-shot code output.
- The paper also introduces **OpenGame-Bench**, which scores generated games on **Build Health**, **Visual Usability**, and **Intent Alignment** through headless browser execution and VLM-based judging.

## Results
- On **OpenGame-Bench** with **150 game prompts**, OpenGame with **Claude Sonnet 4.6** reaches **Build Health 72.4**, **Visual Usability 67.2**, and **Intent Alignment 65.1**.
- Against the strongest listed baseline, **Cursor with Claude Sonnet 4.6**, OpenGame improves by **+5.6 BH** (72.4 vs 66.8), **+5.8 VU** (67.2 vs 61.4), and **+6.2 IA** (65.1 vs 58.9).
- OpenGame with **GameCoder-27B** scores **63.9 BH**, **57.0 VU**, and **54.1 IA**, beating OpenGame with **Qwen-3.5-27B** at **62.8 BH**, **53.8 VU**, and **49.8 IA**. That is **+1.1 BH**, **+3.2 VU**, and **+4.3 IA** from the specialized model.
- Among direct closed-source LLM baselines, **GPT-5.1** gets **57.4 BH / 52.9 VU / 49.4 IA**, **Claude Sonnet 4.6** gets **58.5 / 50.8 / 50.3**, and **Gemini 3.1 Pro** gets **53.6 / 60.2 / 42.1**. OpenGame exceeds all of them on all three metrics except that Gemini is closer on visual quality.
- The benchmark uses **three runs per task with different random seeds** and reports mean scores, which gives a more stable view than a single pass/fail result.

## Link
- [http://arxiv.org/abs/2604.18394v1](http://arxiv.org/abs/2604.18394v1)
