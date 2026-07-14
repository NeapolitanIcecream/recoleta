---
source: arxiv
url: https://arxiv.org/abs/2607.11111v1
published_at: '2026-07-13T05:41:01'
authors:
- Haotian Lin
- Silin Chen
- Xiaodong Gu
- Yuling Shi
- Chengxi Pan
- Jiaqi Ge
- Mengfan Li
- Jianghong Huang
- Mengchieh Chuang
- Beijun Shen
- Haibing Guan
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- repository-knowledge
- human-ai-interaction
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Know Before Fix: QA-Driven Repository Knowledge Acquisition for Software Issue Resolution

## Summary
ACQUIRE improves automated software issue resolution by acquiring repository knowledge through targeted question-answering before patch generation. On SWE-bench Verified, it raises Pass@1 by up to 4.4 percentage points over Mini-SWE-Agent while adding modest cost and time.

## Problem
- Coding agents often lack repository-specific knowledge about cross-module dependencies, API contracts, data flow, and external protocols, which leads to incorrect patches.
- Existing pre-repair methods focus on locating suspicious code or generating broad summaries without first identifying the agent's specific knowledge gaps.
- These failed, knowledge-deficient attempts consume over four times the token cost and nearly twice the execution steps of successful resolutions.

## Approach
- ACQUIRE separates repository understanding from repair into two stages: knowledge acquisition followed by patch generation.
- A Questioner generates targeted, non-redundant questions across four categories: Mechanism & Behavior, Design & Usage, Locating & Structure, and Ecosystem & Standards.
- Independent read-only Answerer agents explore the repository in parallel and produce evidence-grounded answers that cite files, functions, and code behavior.
- A Resolver receives the issue description and the collected QA pairs before starting its normal navigation, editing, and testing loop.

## Results
- On 500 SWE-bench Verified issues, ACQUIRE reached 62.2% Pass@1 with GPT-5-mini versus 58.4% for Mini-SWE-Agent, a gain of 3.8 percentage points; with DeepSeek-V3.2, it reached 70.8% versus 66.4%, a gain of 4.4 points.
- ACQUIRE cost an average of $0.054 and 302 seconds per GPT-5-mini instance, and $0.073 and 1,042 seconds per DeepSeek-V3.2 instance. Richer baselines such as SWE-Debate cost $0.738 and $0.382, with times of 1,552 and 2,517 seconds respectively.
- Human review found 230 of 232 QA pairs supported by repository evidence, or 99.1%; only 2 pairs contained ungrounded central claims.
- QA injection reduced mean repair rounds by 7.1% across all 500 issues and by 17.1% on the 44 instances that changed from failure to success.
- In an oracle experiment on 116 previously failed SWE-bench Lite instances, a single privileged QA pair recovered 26 cases, showing that targeted repository knowledge can unlock fixes that the base agent could not produce.

## Link
- [https://arxiv.org/abs/2607.11111v1](https://arxiv.org/abs/2607.11111v1)
