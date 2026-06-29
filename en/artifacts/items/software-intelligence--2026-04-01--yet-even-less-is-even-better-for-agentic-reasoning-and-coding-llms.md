---
source: arxiv
url: http://arxiv.org/abs/2604.00824v3
published_at: '2026-04-01T12:33:25'
authors:
- CodeArts Model Team
- Yang Ye
- Jingyuan Tan
- Tianyue Jiang
- Ruizhe Ye
- Qiankun He
- Jiarui Yang
- Jian Dong
- Sicong Liang
- Chongjian Yue
- Peibai Xu
- Lufan Lu
- Shiguan Pang
- Taotao Qian
- Junbao Hu
- Yuechan Hao
- Ensheng Shi
- Qi Zhang
- Yi Hao
- Na Fan
- Xin Tan
- Shuai Yao
- Zhiwei Shen
- Zongchen Li
- Yanlin Wang
- Chong Chen
- Yuchi Ma
topics:
- agentic-llms
- code-intelligence
- software-engineering-agents
- trajectory-curation
- swe-bench
- supervised-fine-tuning
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Yet Even Less Is Even Better For Agentic, Reasoning, and Coding LLMs

## Summary
This paper argues that software-engineering agents can improve more from a small set of filtered, high-value trajectories than from a large pool of raw trajectories. It introduces STITCH, a trajectory curation method, plus SandForge, a task construction and evaluation pipeline, and reports gains on SWE-bench-style coding tasks across Python, Java, and ArkTS.

## Problem
- Training coding and agentic LLMs often needs many full trajectories, which are expensive to collect and clean.
- Raw agent traces contain a lot of low-value tokens, repeated actions, and broken context segments, which weakens supervised fine-tuning.
- Prior work focused more on scaling data volume than on finding which parts of trajectories actually carry the training signal, especially for larger models and multilingual software tasks.

## Approach
- The paper builds an end-to-end pipeline called **SandForge** that turns real software repair records from GitHub into executable tasks, runs agents on them, and stores trajectories, patches, verifier outputs, rewards, and metadata.
- It proposes **STITCH** (`Sliding-memory Trajectory Inference and Task Chunking Heuristic`), a two-stage filter for trajectory data.
- In the first stage, STITCH uses automatically discovered trajectory features plus logistic regression to screen out weak trajectories based on signals such as code edits, tool usage, efficiency, and recovery behavior.
- In the second stage, it uses an LLM judge to split long trajectories into semantically safe chunks, carries forward a compressed memory summary between chunks, scores local segments, and keeps decision-critical sub-trajectories even when the full run is mediocre.
- The core idea is simple: keep the steps where the agent makes useful decisions or code changes, drop noisy parts, and fine-tune on that smaller but cleaner dataset.

## Results
- On **SWE-bench Verified**, models trained with STITCH show **up to 63.16% relative improvement** over their base models.
- On **Multi-SWE-bench (Java)**, **MiniMax-M2.5-STITCH** reaches **43.75%** with the **CodeArts Agent** scaffold, a gain of **+16.67%** over the comparison stated in the paper.
- On **HarmonyOS (ArkTS)**, **GLM-4.7-STITCH** raises the **compilation pass rate to 61.31%**, with an improvement of **+43.34%**.
- The paper states that these gains hold across agent frameworks such as **mini-SWE-agent** and **MSWE-agent**, model sizes from **30B to 355B**, and multilingual settings.
- For the ArkTS setting, the paper says the model used **less than 1K training trajectories**.
- The excerpt does not provide full benchmark tables, variance, or detailed baseline names for every experiment, so the strongest concrete claims are the percentages above.

## Link
- [http://arxiv.org/abs/2604.00824v3](http://arxiv.org/abs/2604.00824v3)
