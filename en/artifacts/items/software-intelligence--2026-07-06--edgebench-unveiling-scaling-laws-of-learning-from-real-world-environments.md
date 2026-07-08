---
source: arxiv
url: https://arxiv.org/abs/2607.05155v1
published_at: '2026-07-06T14:39:22'
authors:
- Deyao Zhu
- Xin Zhou
- Shengling Qin
- Xuekai Zhu
- Hangliang Ding
- Shu Zhong
- Zixin Wen
- Zhonglin Xie
- Chenhui Gou
- Linxuan Ren
- Yueyang Wang
- Junfeng Zhong
- Rui Liu
- Tian Gao
- Yangguang Lin
- Jingyuan Zhang
- Maojia Song
- Xuan Qi
- Jinhong Wu
- Chenyang Zhang
- Yinzhu Piao
- Ziru Niu
- Hongbin Lin
- Lingxiang Meng
- Peng Tang
- Chengyao Tang
- Shanyu Wu
- Huanyu Zheng
- Yu Liu
- Liya Zhu
- He Wang
- Ming Ding
- Ziyu Wan
- Hao Liu
- Sibo Wang
- Haotian Zhu
- Xintian Zhang
- Nan Chai
- Yipeng Liu
- Panhao Lai
- Sihang Yuan
- Zixin Su
- Ge Zhang
- Wangchunshu Zhou
- Yantao Du
- Wenhao Huang
- Guang Shi
topics:
- agent-learning
- scaling-laws
- real-world-benchmarks
- software-engineering-agents
- long-horizon-evaluation
relevance_score: 0.73
run_id: materialize-outputs
language_code: en
---

# EdgeBench: Unveiling Scaling Laws of Learning from Real-World Environments

## Summary
EdgeBench is a 134-task benchmark for measuring how agents improve during long runs in executable environments. The paper claims aggregate agent performance follows a log-sigmoid curve with mean R² = 0.998 over about 38,000 hours of interaction.

## Problem
- Deployed agents need to learn private data, tool behavior, hidden tests, and task feedback that cannot be fully covered by pretraining.
- Many existing benchmarks use short tasks or weak feedback, so they mainly measure starting capability instead of within-run learning.
- This matters for software engineering, research, optimization, and professional work where users need agents to turn failures and judge feedback into better artifacts over many hours.

## Approach
- EdgeBench contains 134 tasks across six families: 39 scientific/ML tasks, 36 systems/software engineering tasks, 19 combinatorial optimization tasks, 19 professional knowledge work tasks, 13 formal math tasks, and 8 games/simulators.
- Each task supports at least 12 hours of agent work. The setup uses separate work and judge containers, so agents can test locally, submit artifacts for hidden judging, and continue working while results return.
- The study evaluates five agents: Claude Opus 4.8, GPT-5.5, GPT-5.4, GLM-5.1, and DeepSeek-V4-Pro preview. Each task-model pair gets three independent 12-hour trials.
- The core curve is S(t) = S_max / (1 + (t_mid / t)^β). In plain terms, score rises slowly at first, speeds up after useful feedback accumulates, then tapers as reachable gains run out.
- The proposed mechanism models a task as hidden score units connected in a graph. Solved parts help unlock nearby unsolved parts, and progress becomes smooth after averaging many different tasks.

## Results
- Across all 134 tasks, the 12-hour average learning curves fit the log-sigmoid form with R² ≥ 0.997 for all five agents and mean R² = 0.998.
- Longer runs keep the same fit: 28-hour curves over 80 tasks and four models, plus 72-hour curves over 18 tasks and two models, all reach R² ≥ 0.993.
- Forecasts trained only on the first 6.5 hours predict performance from 6.5 to 12 hours with R² ≥ 0.997 and RMSE below 1.0 point.
- In full-window curve comparison on a 0–100 score scale, log-sigmoid has RMSE 0.390, versus 0.398 for log-probit, 0.402 for log-Gompertz, 0.404 for Weibull CDF, and 0.717 for log-linear.
- The paper reports that frontier agent learning speed roughly doubles every three months across models released since September 2025.
- The benchmark reports mean human expert effort of 57.2 hours per task, with a maximum of 320 hours, and releases 51 tasks plus the evaluation code.

## Link
- [https://arxiv.org/abs/2607.05155v1](https://arxiv.org/abs/2607.05155v1)
