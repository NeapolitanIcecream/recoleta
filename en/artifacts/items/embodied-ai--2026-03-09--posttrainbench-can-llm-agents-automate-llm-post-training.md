---
source: arxiv
url: http://arxiv.org/abs/2603.08640v2
published_at: '2026-03-09T17:18:00'
authors:
- Ben Rank
- Hardik Bhatnagar
- Ameya Prabhu
- Shira Eisenberg
- Karina Nguyen
- Matthias Bethge
- Maksym Andriushchenko
topics:
- llm-agents
- post-training
- benchmarking
- ai-rd-automation
- instruction-tuning
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# PostTrainBench: Can LLM Agents Automate LLM Post-Training?

## Summary
This paper introduces **PostTrainBench**, designed to measure whether frontier LLM agents can autonomously complete LLM post-training under constrained compute. The results show that agents can already substantially improve base models and, on a few targeted tasks, surpass official instruction-tuned models, but overall they still lag far behind general-purpose instruction-tuned models.

## Problem
- The paper addresses the question: **how to systematically evaluate whether LLM agents can autonomously complete LLM post-training**, rather than just isolated research subtasks.
- This matters because post-training directly determines instruction following, reasoning, tool use, and safety; if agents can automate this step, it would mean AI R&D automation could truly accelerate.
- Existing benchmarks mostly do not cover the end-to-end process of “given a base model → autonomously find data / write code / run experiments → submit a post-trained model,” making it difficult to assess real capabilities and risks.

## Approach
- The authors build **PostTrainBench**: agents are given a base LLM, a target evaluation task, **10 hours + 1 H100**, internet access, and developer tools, but **no predefined strategy, training code, or training data**.
- Agents can autonomously execute the full post-training pipeline: search the web for information, download/filter data, write scripts, tune hyperparameters, train, and submit checkpoints; the final evaluation only considers the submitted model’s score on a held-out test set.
- The benchmark covers **4 base models × 7 tasks**, including math, code, function calling, scientific QA, creative writing, and medical dialogue; it also compares multiple CLI agent scaffolds and underlying models.
- To ensure evaluation validity, the authors use an **LLM judge** to check for cheating/violations, such as contaminating the training set with test data, swapping in a different model, or directly downloading a ready-made instruction-tuned model; violations are reverted to the base model score.
- In addition to the overall leaderboard, the paper analyzes scaffold effects, reasoning intensity, time budget, and failure modes to assess the capability boundaries and safety issues of agentic post-training.

## Results
- The **best overall agent** is Claude Opus 4.6 (Claude Code), with a weighted average score of **23.2% ± 1.8**; this is clearly above the **base zero-shot 7.5%**, but still far behind the **official instruction-tuned baseline 51.1%**.
- By task, agents are strongest on **BFCL function calling**: the best agent reaches **75.9% ± 17.8**, while the base model is only **1.5%**; this suggests that on tasks with clear objectives and clear feedback, agents can effectively “climb” through iterative optimization.
- The paper claims that in a few targeted scenarios agents **surpass official instruction-tuned models**: for example, **GPT-5.1 Codex Max** gets **Gemma-3-4B** to **89%** on **BFCL**, compared with **67%** for the official model; for **SmolLM3-3B** on **BFCL**, the agent reaches **91% vs. 84%** official; for **Gemma-3-4B** on **GPQA**, it achieves **33% vs. 31%** official.
- But performance remains weak on harder, broader tasks: for example, on **AIME 2025** the best average is only **5.0% ± 3.5**, on **ArenaHard Writing** the top level is about **10.1%**, and many configurations on **GPQA** still remain below random guessing at **25%**.
- In an example run, Claude Opus 4.5 improves **Gemma-3-4B** on **HumanEval** from **0% to 37.3%**, using **104 interaction rounds, 9 hours 20 minutes, and $4.62 in API cost**, showing that agents already have the ability to conduct relatively long-horizon experimentation and debugging.
- Ablation results show that more time helps but with diminishing returns: at **1 hour**, agents average about **10–12%** (above the 7.5% baseline); for GPT-5.1 Codex Max, **medium reasoning** is best, with a score of **19.7 ± 0.3**, outperforming **low 15.5 ± 0.4** and **high 17.2 ± 0.04**, while high mode consumes about **1.89M vs. 0.96M** tokens.

## Link
- [http://arxiv.org/abs/2603.08640v2](http://arxiv.org/abs/2603.08640v2)
