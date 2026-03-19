---
source: arxiv
url: http://arxiv.org/abs/2603.03823v1
published_at: '2026-03-04T08:20:25'
authors:
- Jialong Chen
- Xander Xu
- Hu Wei
- Chuan Chen
- Bing Zhao
topics:
- software-engineering-benchmark
- code-maintenance
- continuous-integration
- llm-agents
- repository-level-eval
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# SWE-CI: Evaluating Agent Capabilities in Maintaining Codebases via Continuous Integration

## Summary
SWE-CI proposes a new benchmark for **long-term code maintenance**, using CI-style multi-round evolution to evaluate agents rather than only checking whether a one-shot fix passes tests. It emphasizes that what truly matters is not just “fixing the current problem,” but ensuring the code remains easy to extend and suffers fewer regressions across dozens of future modifications.

## Problem
- Most existing code benchmarks are **static, one-shot** evaluations that measure only current functional correctness, making it hard to distinguish between a “fragile patch that barely passes tests” and a “highly maintainable implementation that supports future evolution.”
- Real-world software development is mainly about **long-term maintenance and iterative requirements changes**; the paper notes that software maintenance accounts for about **60%–80%** of lifecycle cost, so evaluating only single fixes deviates from real value.
- There is a lack of repository-level benchmarks that can observe technical debt, regression control, and long-term maintainability over **continuous multi-round modifications**.

## Approach
- Build **SWE-CI**: the first repository-level benchmark based on the **Continuous Integration loop**, with tasks drawn from long-term evolution segments of real GitHub Python repositories.
- Each task consists of a **base commit** and a **target/oracle commit**; the agent must start from the base version and, through multiple rounds of analysis, coding, and testing, gradually approach the test behavior corresponding to the target version.
- Propose **evolution-based evaluation**: the requirements for each round are not fixed in advance, but are dynamically generated based on the testing gap between the “current code vs. target code,” so early design decisions affect the difficulty of later rounds.
- Design an **Architect–Programmer dual-agent protocol**: the Architect first summarizes failures, identifies causes, and generates no more than 5 high-level requirements; the Programmer then interprets the requirements, plans, and implements modifications, simulating a real CI team workflow.
- Introduce two core metrics: **normalized change**, which normalizes the change in the number of tests passed to [-1,1]; and **EvoScore**, which computes a future-weighted average of multi-round normalized change (giving higher weight to later rounds) to approximate long-term maintainability.

## Results
- Dataset scale: **100 tasks** in the final benchmark, drawn from **68 repositories**; each base/target pair spans on average **233 days** and **71 consecutive commits**, and includes at least **500 lines** of non-test source code changes.
- Dataset construction pipeline: starting from **4,923** candidate repositories, the authors obtained **8,311** candidate commit pairs; after environment building, **1,458** remained; after automatic filtering, **137** remained; the final **100** were selected from these.
- Experimental setup: **18 models from 8 providers** were evaluated, with total consumption exceeding **10 billion tokens**; each task allowed up to **20 rounds**, and a single test timeout was **3600 seconds**.
- Main finding 1: within the same provider family, **newer models consistently outperform older ones**; the authors say models **released after 2026** show more pronounced gains over prior generations. Qualitatively, the **Claude Opus series** leads overall, and **GLM-5** also performs strongly.
- Main finding 2: different providers show different preferences for short-term gains vs. long-term maintainability; when increasing the future weight in EvoScore, **MiniMax, DeepSeek, and GPT** lean more toward long-term gains, **Kimi and GLM** lean more toward short-term gains, and **Qwen, Doubao, and Claude** are relatively stable. This section **does not provide a specific score table**.
- Main finding 3: current models are still **weak at regression control** in long-term maintenance. For most models, the **zero-regression rate < 0.25**; only **two Claude-opus series models > 0.5**. This suggests that even as static bug-fixing ability improves, automated long-term maintenance remains far from solved.

## Link
- [http://arxiv.org/abs/2603.03823v1](http://arxiv.org/abs/2603.03823v1)
