---
source: arxiv
url: https://arxiv.org/abs/2606.18023v1
published_at: '2026-06-16T15:03:05'
authors:
- Jian Yang
- Shawn Guo
- Wei Zhang
- Tianyu Zheng
- Yaxin Du
- Haau-Sing Li
- Jiajun Wu
- Yue Song
- Yan Xing
- Qingsong Cai
- Zelong Huang
- Chuan Hao
- Ran Tao
- Xianglong Liu
- Wayne Xin Zhao
- Mingjie Tang
- Weifeng Lv
- Ming Zhou
- Bryan Dai
topics:
- code-intelligence
- software-foundation-models
- test-time-compute
- looped-transformers
- agentic-software-engineering
- kv-cache-efficiency
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# LoopCoder-v2: Only Loop Once for Efficient Test-Time Computation Scaling

## Summary
LoopCoder-v2 finds that a 7B Parallel Loop Transformer for coding works best with two loops, not more. The two-loop model gains strongly on code and software-agent benchmarks while three and four loops regress.

## Problem
- Looped Transformers can add latent computation without adding parameters, but standard sequential loops increase latency and KV-cache memory with the loop count.
- Parallel Loop Transformers reduce that cost, but they need a way to choose the loop count because extra loops can add positional mismatch through cross-loop offsets.
- This matters for code models because SWE-style tasks need stronger internal computation, while deployment still has latency and memory limits.

## Approach
- The model reuses the same Transformer block across loops, so the effective depth grows while the parameter count stays fixed.
- PLT makes loops cheaper with cross-loop position offsets, where each later loop receives the previous loop shifted by one token, and with shared-KV gated sliding-window attention, where later loops reuse the first-loop KV cache and mix it with local attention.
- The authors train 7B LoopCoder-v2 variants from scratch on 18T mixed text/code tokens with loop counts R=1, R=2, R=3, and R=4, then apply the same supervised instruction tuning on 6M examples.
- They diagnose loop behavior with hidden-state movement, effective rank, fixed-point gap, attention KL, attention-head diversity, output-distribution shift, and an intrinsic offset cost Ω that measures adjacent-token hidden-state mismatch.

## Results
- The two-loop model improves the benchmark average from 38.0 for the R=1 baseline to 46.5, a gain of 8.5 points across the reported suite.
- On SWE-bench Verified, R=2 rises from 43.0 to 64.4, a gain of 21.4 points over the non-looped baseline; R=3 falls to 27.6 and R=4 falls to 22.4.
- On Multi-SWE, R=2 improves from 14.0 to 31.0, a gain of 17.0 points; R=3 scores 11.0 and R=4 scores 9.3.
- Code benchmark gains for R=2 include HumanEval+ 81.1 to 84.1, MultiPL-E 69.5 to 73.9, BigCodeBench 40.1 to 46.1, and LiveCodeBench 27.4 to 35.4.
- Tool and agent benchmarks also improve for R=2: Terminal-Bench v1 26.3 to 34.2, Terminal-Bench v2 11.2 to 21.0, and BFCL 32.2 to 40.1; M2W drops slightly from 35.3 to 34.5.
- The paper claims a non-monotonic loop-count effect: loop 2 gives the main useful refinement, while later loops show smaller, more oscillatory updates and lower representational diversity as the offset cost stays roughly fixed.

## Link
- [https://arxiv.org/abs/2606.18023v1](https://arxiv.org/abs/2606.18023v1)
