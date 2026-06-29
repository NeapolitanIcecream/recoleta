---
source: arxiv
url: https://arxiv.org/abs/2606.07131v1
published_at: '2026-06-05T10:43:19'
authors:
- Wenbo Guo
- Wei Zeng
- Chengwei Liu
- Xiaojun Jia
- Yijia Xu
- Lei Tang
- Yong Fang
- Yang Liu
topics:
- malicious-agent-skills
- coding-agents
- benchmark
- code-injection
- prompt-injection
- supply-chain-security
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills

## Summary
MalSkillBench is a runtime-verified benchmark for malicious third-party skills used by AI coding agents. It tests whether detectors can catch attacks that combine executable code, markdown instructions, and agent tool use.

## Problem
- AI coding agents such as Claude Code, OpenCode, Cursor, and Gemini CLI load third-party skills that can contain both instructions and executable scripts, creating a supply-chain risk for agent workflows.
- Existing malicious-skill datasets are small or skewed: one public dataset has 157 samples, and the authors' 703 wild samples are dominated by dependency impersonation.
- Detector results are unreliable without shared ground truth, because wild-only evaluation can change a tool's recall by up to 66.3 points.

## Approach
- The paper defines a 3D taxonomy with 108 cells: attack vector, malicious behavior, and insertion strategy.
- Attack vectors include code injection, prompt injection, and mixed attacks where markdown instructions and scripts work together.
- The Generate-Verify-Feedback pipeline creates malicious skills from real attack sources, then runs each candidate in a Docker sandbox with OpenCode, system-call monitoring, file monitoring, and an LLM judge.
- Generated samples enter the benchmark only when the expected malicious behavior appears at runtime.
- The dataset also includes wild malicious skills and matched benign skills for detector evaluation.

## Results
- MalSkillBench contains 3,944 malicious skills and 4,000 matched benign skills.
- Of the malicious skills, 3,214 are generated and runtime-verified, 703 are in-the-wild samples, and 27 are curated for tool-compatibility validation.
- Code injection has a 94.5% verification yield, while prompt injection has a 75.8% yield.
- The wild sample is narrow: 86.3% to 86.6% of samples are dominated by one dependency-impersonation or cryptocurrency-theft pattern, and 81% come from two accounts.
- The strongest skill-specific detector reaches 98.4% recall on code injection, but drops on prompt-injection and agent-control attacks.
- Across 12 evaluated tools, the best skill-specific detector reaches 88.6% F1; high-recall transfer tools can produce up to 3,979 false positives on 4,000 benign skills.

## Link
- [https://arxiv.org/abs/2606.07131v1](https://arxiv.org/abs/2606.07131v1)
