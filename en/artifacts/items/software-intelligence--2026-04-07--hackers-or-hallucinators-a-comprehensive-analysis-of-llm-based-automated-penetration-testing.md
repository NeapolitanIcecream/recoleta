---
source: arxiv
url: http://arxiv.org/abs/2604.05719v1
published_at: '2026-04-07T11:19:16'
authors:
- Jiaren Peng
- Zeqin Li
- Chang You
- Yan Wang
- Hanlin Sun
- Xuan Tian
- Shuqiao Zhang
- Junyi Liu
- Jianguo Zhao
- Renyang Liu
- Haoran Ou
- Yuqiang Sun
- Jiancheng Zhang
- Yutong Jiao
- Kunshu Song
- Chao Zhang
- Fan Shi
- Hongda Sun
- Rui Yan
- Cheng Huang
topics:
- automated-penetration-testing
- llm-agents
- cybersecurity-evaluation
- multi-agent-systems
- hallucination-analysis
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Hackers or Hallucinators? A Comprehensive Analysis of LLM-Based Automated Penetration Testing

## Summary
This paper is a systematization and benchmark study of LLM-based automated penetration testing frameworks. It reviews how these systems are built and compares 13 open-source frameworks plus 2 baselines under one evaluation setup.

## Problem
- The field has many new AutoPT systems, but there was no broad architectural review and no fair large-scale comparison under one benchmark.
- This matters because penetration testing is expensive, expert-limited, and in growing demand; weak evidence about what design choices help can mislead both research and deployment.
- The paper focuses on black-box automated penetration testing, where the agent must discover and exploit issues with limited prior knowledge and high uncertainty.

## Approach
- The authors build a taxonomy of AutoPT systems across six design dimensions: agent architecture, agent planning, memory, execution, external knowledge, and benchmarks.
- They run a unified empirical study on 13 representative open-source AutoPT frameworks and 2 baselines, using the XBOW challenge set to reduce data contamination risk.
- Main experiments use DeepSeek-Chat-v3.2 as the backbone model under identical conditions, with added comparisons using Claude-Opus-4.6, GPT-5.2, Gemini-Pro-3.1, and DeepSeek-Reasoner-v3.2.
- The evaluation is large: over 10 billion tokens, more than 1,500 execution logs, over 15 security-trained reviewers, and four months of manual log analysis.
- The core mechanism is simple: hold many AutoPT agents to the same tasks and settings, then compare which design choices actually improve attack success, cost, and failure modes.

## Results
- Single-agent systems were stronger than expected: among 13 frameworks, 3 single-agent designs ranked in the top 6 on Easy and Medium tasks, matching or beating several multi-agent systems.
- External knowledge often hurt performance. In ablations on 6 frameworks with knowledge bases, 3 improved after removal; Cruiser rose from 42 to 57, and LuaN1aoAgent from 83 to 90.
- Simple coding-agent baselines beat most specialized frameworks: Kimi CLI scored 72 and Claude Code scored 69 with minimal prompts.
- Hallucinations were common. 8 of the 13 open-source frameworks produced hallucinated flags on at least one challenge, and switching to Claude-Opus-4.6 or GPT-5.2 did not remove the issue.
- On chained-vulnerability tasks, 83.3% of samples stalled before completing the full exploit chain, and only 16.67% completed a full multi-vulnerability chain.
- On CVE exploitation tasks, about 56.67% of samples linked the target to the right CVE but still failed to build an effective payload. The excerpt does not provide a full benchmark table with aggregate success rates for all 15 systems.

## Link
- [http://arxiv.org/abs/2604.05719v1](http://arxiv.org/abs/2604.05719v1)
