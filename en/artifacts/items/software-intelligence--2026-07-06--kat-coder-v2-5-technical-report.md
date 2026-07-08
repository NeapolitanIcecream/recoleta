---
source: arxiv
url: https://arxiv.org/abs/2607.05471v1
published_at: '2026-07-06T08:14:02'
authors:
- Bo Huang
- Fengxiang Li
- Hao Xu
- Haoyang Huang
- Hongyi Fu
- Jinhua Hao
- Kun Yuan
- Minglei Zhang
- Pengcheng Xu
- Shiyang Liu
- Wenhao Zhuang
- Yuze Shi
- Zongxian Feng
- Chao Wang
- Cheng He
- Chongling Rao
- Deyu Cao
- Fan Yang
- Gang Xiong
- Haochen Liu
- Jiabao Li
- Jian Liang
- Jinghui Jia
- Jingwen Chang
- Jun Du
- Junyu Shi
- Min Li
- Mingqi Wu
- Qiang Gao
- Shangpeng Yan
- Shaotong Qi
- Shu Xu
- Shuo Zhou
- Tiankuo Xu
- Tong Zheng
- Weilun Zhao
- Xiancheng Meng
- Xianda Sun
- Xiaoyu Jiang
- Xunhao Jia
- Yao Xia
- Yimeng Xu
- Yinghan Cui
- Yingpeng Chen
- Yiwen Ning
- Yong Wang
- Yuxuan Sun
- Zhongsheng Liu
- Ming Sun
- Cheng Luo
- Chen Yang
- Han Li
- Kun Gai
topics:
- software-foundation-model
- code-intelligence
- agentic-coding
- repository-level-swe
- tool-use-agents
- reinforcement-learning
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# KAT-Coder-V2.5 Technical Report

## Summary
KAT-Coder-V2.5 is a coding agent trained for repository-level software engineering and tool use in executable environments. The paper’s main claim is that better verifiable environments, trajectory filtering, and long-horizon RL infrastructure improve agentic coding more than scale alone.

## Problem
- Coding agents must edit real repositories, run tests, recover from failures, and use tools across long tasks; single-turn code generation does not train these behaviors well.
- Real repositories are hard to rebuild at scale because dependencies, build tools, tests, and runtime assumptions vary by project.
- Final test success alone gives weak training data because some passing traces use shortcuts, while some failing traces contain useful search and repair behavior.

## Approach
- AutoBuilder rebuilds multilingual repositories in sandboxes, runs structured test verification, and accepts environments only when more than 90% of expected tests are collected and outcomes reproduce across runs.
- The system regenerates self-contained task descriptions from golden patches and test patches, then filters unclear or inconsistent samples.
- A process-aware trajectory pipeline scores exploration, localization, patch quality, verification, recovery, and honesty; it removes brittle passing traces and recovers near-miss failures through temporary hints followed by hint-free trace regeneration.
- KwaiClawEnv creates tool-use training data through Service, Task, and Eval layers, with executable services, task variants, parallel rollouts, and multi-stage filtering.
- Reinforcement learning uses harness randomization, a hardened sandbox, asymmetric actor-critic PPO, harness-oriented rewards, and Multi-Teacher On-Policy Distillation across SWE, Claw, terminal, web-coding, and general experts.

## Results
- Across 6 software-engineering and agentic benchmarks under a unified Claude Code harness, KAT-Coder-V2.5 reports the top result on PinchBench and second-place results on SWE-Bench Pro and KAT Code Bench among evaluated models; the excerpt does not provide exact benchmark scores.
- The paper says KAT-Coder-V2.5 ranks second only to Opus 4.8 on repository-level software engineering in the reported comparison.
- AutoBuilder raises executable environment construction success from 16.5% to 57.2% and produces more than 100,000 verifiable environments across 12 languages.
- Hint-assisted recovery raises the pass rate of previously zero-pass tasks to roughly 20% before the system regenerates hint-free training trajectories.
- KwaiClawEnv reports service generation success above 90%, retains more than 100,000 high-quality task instances after verification, and produces trajectories averaging 15 tool calls, with the longest exceeding 100 steps.
- The RL infrastructure reports retokenization drift in about 40% of roughly 200-turn agentic samples when using chat endpoints, so it sends requests through the generation endpoint to keep rollout and training tokens identical.

## Link
- [https://arxiv.org/abs/2607.05471v1](https://arxiv.org/abs/2607.05471v1)
