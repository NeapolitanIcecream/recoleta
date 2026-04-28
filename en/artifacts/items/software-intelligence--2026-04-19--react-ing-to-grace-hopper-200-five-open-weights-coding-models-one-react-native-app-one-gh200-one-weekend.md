---
source: arxiv
url: http://arxiv.org/abs/2604.17187v1
published_at: '2026-04-19T01:21:02'
authors:
- Alex Potanin
topics:
- open-weight-llms
- code-generation
- react-native
- benchmark-evaluation
- self-hosting
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# React-ing to Grace Hopper 200: Five Open-Weights Coding Models, One React Native App, One GH200, One Weekend

## Summary
This paper tests five open-weight coding models on one concrete app-building task instead of a benchmark suite. It finds that SWE-Bench rankings did not predict which model produced the best working React Native app on a GH200.

## Problem
- The paper asks whether benchmark leaders on SWE-Bench actually build a usable multi-file application from a natural product prompt.
- This matters for teams choosing self-hosted coding models, because hardware cost is high and benchmark scores may miss failures that break the shipped artifact.
- The task includes practical requirements that benchmarks often miss: authentication, per-user isolation, per-day counting semantics, and web compatibility.

## Approach
- The author ran five open-weight coding models on the same prompt: Kimi-K2.5 Q3, Kimi-K2.5 Q4, GLM-5.1, Qwen3-Coder-480B, and DeepSeek-V3.2.
- All models were served on one NVIDIA GH200 576GB node with llama.cpp and Unsloth Dynamic 2.0 GGUF quantizations, then used through aider in whole-edit mode.
- The prompt asked each model to create a React Native app with account creation, login, kangaroo counts per day, and web support.
- Outputs were judged on whether the app ran out of the box and whether key features worked: credential validation, per-user data isolation, per-day bucketing, history retention, logout, and web-safe behavior.
- The paper also records deployment issues seen during use, including temperature-sensitive sampling hangs, reasoning-token leakage into file-path parsing, and universal misuse of React Native Alert.alert on the web.

## Results
- Kimi-K2.5 Q3 was the best overall model. It was the only one described as fully spec-compliant at the application level, aside from the shared web bug around `Alert.alert`. It ran out of the box, passed auth validation, per-user isolation, per-day counting, 7-day history, and logout, at **17 tok/s** with about **4.8k output tokens**.
- Kimi-K2.5 Q4 also ran out of the box and matched most features, but it regressed on per-day semantics to **"today only"** counting. It generated at **7.9 tok/s**, about **2.2x slower** than Q3, with about **4.8k output tokens**.
- GLM-5.1 had the highest cited SWE-Bench Pro score in the paper at **58.4%**, but it failed the task operationally: the app did **not** run out of the box because it required a missing `firebaseConfig.js`. It generated at about **15 tok/s** with about **5.5k tokens**.
- Qwen3-Coder-480B ran out of the box and handled auth and per-user isolation, but failed the core requirement of per-day counting: **no per-day bucket and no history**. It generated at about **20 tok/s** with about **4.2k tokens**.
- DeepSeek-V3.2 failed to run out of the box because reasoning-text leaked into a parsed file path, which misplaced `App.js`. It also failed credential validation, per-user isolation, per-day semantics, and logout. It generated at about **14 tok/s** with about **5.1k tokens**.
- Across all five models, **0/5** handled web adaptation correctly: every model relied on `Alert.alert`, which is a no-op on `react-native-web`. The paper also claims efficiency-school models with **10-15B active parameters** can match scale-school SWE-Bench results at about **1/7th the hardware cost** of **32-40B active** models.

## Link
- [http://arxiv.org/abs/2604.17187v1](http://arxiv.org/abs/2604.17187v1)
