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
- llm-agents
- environment-synthesis
- research-code-execution
- runtime-verification
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# ResearchEnvBench: Benchmarking Agents on Environment Synthesis for Research Code Execution

## Summary
ResearchEnvBench introduces a benchmark for automatically constructing execution environments for research code, specifically evaluating whether agents can turn raw research repositories into truly runnable AI/HPC experimental environments. The paper shows that current SOTA agents still have a clear gap between “looks installed” and “actually runs on GPU/multi-GPU.”

## Problem
- Existing code repair or automated research benchmarks usually assume the execution environment is pre-configured, overlooking the hardest prerequisite steps in real research: dependency resolution, CUDA/driver alignment, distributed configuration, and custom compilation.
- Relying only on static checks, successful builds, or missing-import counts cannot verify whether research code can actually run on CPU/GPU/multi-GPU, making it difficult to measure an agent’s capability for reproducible research.
- This problem matters because if agents cannot independently build runnable environments, then subsequent code modification, experiment design, and result reproduction are all difficult to realize in real research workflows.

## Approach
- Build **ResearchEnvBench**: collect and manually curate 44 high-complexity AI research repositories released after 2024, covering real research workloads such as Py/C++, GPU dependencies, custom CUDA kernels, and distributed training.
- Define the task as environment synthesis: given a research repository, documentation, and a target execution setting, the agent uses shell execution, file reading, and auxiliary-file editing to turn a bare environment into a runnable one without modifying tracked source code.
- Propose a **runtime verification pyramid**, evaluating capabilities in layers from static dependency completeness to actual runtime ability: $C_0$ missing imports, $C_1$ CPU execution, $C_2$ CUDA alignment, $C_3$ single-GPU computation, $C_4$ multi-GPU DDP readiness.
- Introduce the **capability hallucination** metric $C_5$, measuring the gap between agent self-reported success and hidden-probe ground truth, further divided into path, version, and capability hallucinations.
- Evaluate 4 categories of SOTA agents in a unified Docker sandbox, using the same tool interface and budget, and compare differences in success rates at each stage and self-report reliability.

## Results
- The dataset contains **44** high-complexity research repositories; among them, **43/44** support at least single-GPU execution, covering 8 categories of modern ML research code, making it a hardware-aware benchmark for research environments.
- The best **CPU execution success rate $C_1$** comes from Codex: **17/29 = 58.6%**; Claude(GLM-4.7) and NexAU are both **16/29 = 55.2%**, and Claude(Sonnet 4.5) is **15/29 = 51.7%**.
- The best **CUDA alignment success rate $C_2$** is achieved by Claude(Sonnet 4.5) and NexAU: **41/44 = 93.2%**; Claude(GLM-4.7) reaches **40/44 = 90.9%**; Codex is only **35/44 = 79.5%**. This shows that static dependency closure does not imply hardware usability.
- The best **single-GPU execution $C_3$** is achieved by Claude(GLM-4.7) and NexAU: **21/43 = 48.8%**; Codex reaches **19/43 = 44.2%**; Claude(Sonnet 4.5) reaches **18/43 = 41.9%**. The clear drop from $C_2$ to $C_3$ reveals that “GPU visible” does not mean research entry points are runnable.
- The best **multi-GPU DDP success rate $C_4$** is achieved by the two Claude configurations: **12/32 = 37.5%**; Codex and NexAU are both **11/32 = 34.4%**. The paper emphasizes that the current best multi-GPU verification success rate is still only **37.5%**.
- On **static missing imports $C_0$**, Codex performs best at **675/2858 = 23.6%**, outperforming Claude(GLM-4.7) at **26.6%**, Claude(Sonnet 4.5) at **25.5%**, and NexAU at **25.3%**; however, this does not translate into the best GPU-readiness capability.
- **Hallucination $C_5$** differs significantly: Codex has only **4** total hallucinations, Claude(GLM-4.7) has **18**, Claude(Sonnet 4.5) has **20**, and NexAU has **16**; most errors are capability hallucinations (for example, Claude Sonnet 4.5 has **20/20**). This indicates that more conservative self-reporting can significantly reduce false positives where success is claimed but actual execution fails.

## Link
- [http://arxiv.org/abs/2603.06739v1](http://arxiv.org/abs/2603.06739v1)
