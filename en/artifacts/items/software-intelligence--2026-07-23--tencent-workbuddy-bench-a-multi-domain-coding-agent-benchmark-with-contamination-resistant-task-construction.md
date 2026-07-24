---
source: arxiv
url: https://arxiv.org/abs/2607.20911v1
published_at: '2026-07-23T04:34:06'
authors:
- Tencent WorkBuddy Bench Team
- Siqi Cai
- Shaopeng Chen
- Xiang Fei
- Yong Mao
- Zihan Xu
- Zhiheng Lyu
- Zhijian Shao
- Yuchen Shi
- Shuwen Zhang
- Chaofan Qiu
- Linjie Che
- Xiaoxi Zhao
- Feng Wu
- Kai Zhang
- Chaofan Zhu
- Yubin Qi
- Xiaoyun Liang
- Peijie Dong
- Yunhao Zhang
- Yuanjie Zhu
- Ling Jiang
- Xianjun Zhang
- Zhehang Chu
- Anyuan Sang
- Zhen Feng
- Sen Nie
- Shi Wu
- Yuanzhen Xu
- Xin Li
- Ning Yang
- Zhiqiang Dong
- Hande Dong
- Qiang Lin
- Yi Liu
- Yunsheng Wu
- Ke Li
- Xing Sun
topics:
- coding-agent-benchmark
- code-intelligence
- automated-software-production
- multi-domain-evaluation
- contamination-resistance
- multi-agent-software-engineering
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Tencent WorkBuddy Bench: A Multi-Domain Coding-Agent Benchmark with Contamination-Resistant Task Construction

## Summary
Tencent WorkBuddy Bench is an openly released benchmark for coding agents across repository engineering, web development, office workflows, and security tasks. It aims to measure realistic work while reducing searchable-prompt contamination through task rewriting, versioning, and reproducible evaluation.

## Problem
- Existing public benchmarks often reuse web-searchable issue or repository content and focus mainly on single-issue software fixes, making scores vulnerable to memorization.
- Production-derived benchmarks better reflect real usage but are commonly closed, limiting auditability and independent reproduction.
- Agents increasingly work across code, web, office, and security artifacts, so a broader evaluation suite matters; however, these domains require different verification methods.

## Approach
- Construct each task by reverse-engineering a real commit, pull request, CVE, or business scenario, then rewriting it as a colloquial, role-played request that withholds the root cause, target files, and reference solution.
- Match task categories, roles, modes, and difficulty to aggregate internal usage distributions without reusing raw user prompts or sessions.
- Package tasks in a Harbor-style directory with an agent-visible workspace separated from post-episode evaluation assets; release prompts, environments, tests, harnesses, and reference solutions openly.
- Evaluate four tracks with domain-specific verifiers: hidden tests for Code, rule and LLM/VLM/agent judges for Web, deterministic checks plus evidence-grounded LLM judging for Office, and deterministic scoring for Security.
- Use dataset versioning and optional canary strings to manage post-release exposure; the construction prevents searchable recovery of task prompts but does not guarantee contamination-free evaluation.

## Results
- The initial release contains 260 tasks: 80 Code, 70 Web, 50 Office, and 60 Security. Scores are reported separately because the tracks use different metrics, and the suite reports no overall average.
- The Code subset includes 34 tasks anchored to real upstream commits, 24 clean-room or ported tasks, and 22 synthetic workspaces; only 10 of 80 tasks are bug fixes.
- Code task admission requires baseline verifier reward <= 0.3 and oracle reward = 1.0, ensuring the untouched workspace does not already satisfy the contract and a reference patch can reach full reward.
- Code tasks span five requester roles and are concentrated at higher difficulty levels: 42 of 80 are editorially hard and 40 of 80 are L4 on the repository-complexity ladder.
- The excerpt describes a cross-model leaderboard evaluated with CodeBuddy Code and Claude Code, but it does not provide quantitative model scores, dataset-level baselines, or comparative performance results.

## Link
- [https://arxiv.org/abs/2607.20911v1](https://arxiv.org/abs/2607.20911v1)
