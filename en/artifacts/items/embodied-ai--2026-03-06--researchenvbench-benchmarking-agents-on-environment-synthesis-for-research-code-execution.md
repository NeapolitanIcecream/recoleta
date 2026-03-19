---
source: arxiv
url: http://arxiv.org/abs/2603.06739v1
published_at: '2026-03-06T08:29:08'
authors:
- Yubang Wang
- Chenxi Zhang
- Bowen Chen
- Zezheng Huai
- Zihao Dai
- Xinchi Chen
- Yuxin Wang
- Yining Zheng
- Jingjing Gong
- Xipeng Qiu
topics:
- benchmarking
- research-code-execution
- environment-synthesis
- runtime-verification
- llm-agents
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# ResearchEnvBench: Benchmarking Agents on Environment Synthesis for Research Code Execution

## Summary
ResearchEnvBench is a benchmark for the automatic setup of research code execution environments, specifically evaluating whether an agent can truly configure an original research repository into a **runnable** state rather than one that merely **looks installed correctly**. The paper shows that even the strongest current agents still fall noticeably short of reproducible experimentation on complex AI/HPC repositories.

## Problem
- Existing code/scientific agent evaluations usually assume the execution environment has already been configured, overlooking the hardest prerequisite steps in practice: dependency installation, CUDA/driver alignment, and distributed training setup.
- Static checks, missing-import detection, or even a successful Docker build alone cannot prove that a research repository can actually run on CPU/GPU, and therefore may overestimate agent capability.
- This matters because if an agent cannot autonomously set up the research environment, then its subsequent code edits, experiments, and scientific conclusions are difficult to truly verify and reproduce.

## Approach
- Proposes **ResearchEnvBench**: a collection of **44** high-complexity research repositories released after 2024, focusing on real challenges such as AI/HPC, GPU dependencies, custom CUDA kernels, and distributed training.
- The task is straightforward: given an original repository, documentation, and a target execution setting, the agent uses shell commands, file reading, and helper-script editing to build the environment, but **may not modify tracked source code**.
- Designs a layered **Pyramid of Runtime Verification**: from static dependency completeness **C0**, to CPU execution **C1**, CUDA alignment **C2**, single-GPU computation **C3**, and multi-GPU DDP **C4**, with difficulty increasing at each level.
- Adds a **C5 hallucination metric**: compares the agent's self-reported "success/usability" against the actual results of hidden probes, measuring false claims about paths, versions, and capabilities.
- Evaluates 4 classes of SOTA agents in a unified sandbox environment: Ubuntu 22.04, **2× RTX 4090**, CUDA **12.4** driver, with no deep learning framework preinstalled.

## Results
- Benchmark scale and coverage: **44** repositories total, in **Python/C++**; **43/44** support at least single-GPU execution, some support multi-GPU DDP, covering 8 categories of modern ML research code.
- The **best CPU execution rate C1** comes from Codex: **17/29 = 58.6%**; Claude(GLM-4.7) and NexAU achieve **16/29 = 55.2%**; Claude(Sonnet 4.5) achieves **15/29 = 51.7%**.
- The **best CUDA alignment C2** is achieved by Claude(Sonnet 4.5) and NexAU: **41/44 = 93.2%**; Claude(GLM-4.7) reaches **40/44 = 90.9%**; Codex reaches **35/44 = 79.5%**.
- The **best real single-GPU computation C3** is achieved by Claude(GLM-4.7) and NexAU: **21/43 = 48.8%**; Codex reaches **19/43 = 44.2%**; Sonnet 4.5 reaches **18/43 = 41.9%**. This shows that “GPU visible” does not mean “repository runnable.”
- The **best multi-GPU DDP C4** is only **12/32 = 37.5%**, achieved by two Claude configurations; Codex and NexAU both reach **11/32 = 34.4%**. This is a key breakthrough finding emphasized by the paper: current SOTA still has a low success rate on real research-environment reproduction.
- Static checks are disconnected from real execution: Codex has the lowest missing-import ratio, **675/2858 = 23.6%**, but its **C2 is only 79.5%**, behind Claude/NexAU at **90.9%–93.2%**, indicating that “dependencies appear complete” does not mean CUDA/ABI is actually correct.
- On hallucination, Codex has the lowest total number, at just **4**; Claude(GLM-4.7) has **18**, Claude(Sonnet 4.5) has **20**, and NexAU has **16**. Most are **capability hallucinations** (for example, 17/18, 20/20, 14/16), showing that many agents misjudge “installation succeeded” as “already runnable.”

## Link
- [http://arxiv.org/abs/2603.06739v1](http://arxiv.org/abs/2603.06739v1)
