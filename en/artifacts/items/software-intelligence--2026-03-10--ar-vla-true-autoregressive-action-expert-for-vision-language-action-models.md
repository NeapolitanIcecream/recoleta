---
source: arxiv
url: http://arxiv.org/abs/2603.10126v1
published_at: '2026-03-10T18:03:29'
authors:
- Yutong Hu
- Jan-Nico Zaech
- Nikolay Nikolov
- Yuanqi Yao
- Sombit Dey
- Giuliano Albanese
- Renaud Detry
- Luc Van Gool
- Danda Paudel
topics:
- vision-language-action
- autoregressive-policy
- robot-manipulation
- temporal-memory
- transformer-decoder
relevance_score: 0.73
run_id: materialize-outputs
language_code: en
---

# AR-VLA: True Autoregressive Action Expert for Vision-Language-Action Models

## Summary
AR-VLA proposes a truly cross-temporal autoregressive action expert that drives robot control using persistent action memory instead of resetting context at every step. It aims to solve the structural problem in existing VLA/diffusion policies that are “autoregressive only within a single step but reactive across steps,” thereby improving long-horizon consistency, smoothness, and history awareness.

## Problem
- Existing Vision-Language-Action models and diffusion policies usually predict in “action chunks” or in a single-step reactive manner, resetting temporal context whenever a new observation arrives and lacking a persistent internal state.
- This “Markovian amnesia” makes it difficult for robots to use past action and velocity information, leading to jittery trajectories, temporal inconsistency, and failures on long-horizon or partially observable tasks.
- Robot control also faces a frequency mismatch between “slow perception/slow reasoning” and “fast control,” so it needs a structure that can still output stable actions when visual updates are sparse or delayed.

## Approach
- Model action generation as **true cross-temporal autoregressive sequence prediction**: the current action depends on the history of past actions and proprioceptive states, while conditioning on the most recently available vision-language prefix, rather than only the current snapshot.
- Design a **Hybrid Key-Value Cache (HKV)**: one is a high-frequency, rolling FIFO cache for action/proprioceptive history; the other is a low-frequency, refreshable vision-language cache. This allows the action expert to run independently and continuously, with vision only providing asynchronous “guidance.”
- Propose **Dynamic Temporal Re-anchoring (DTR)**: assign visual tokens a temporal anchor corresponding to their sampling time, and use RoPE so the model can explicitly understand “how stale” the visual information is, thereby reducing the distribution gap between short-context training and long-horizon inference.
- Training proceeds in two stages: first, **action-only pretraining** to learn kinematic “syntax” (dynamics, constraints, common motion patterns), then **vision-action alignment**; history dropout is also added to prevent the model from over-relying on perfect history and to improve robustness to delay and noise.

## Results
- In the generalist VLA setting with **BridgeV2 training and SimplerEnv evaluation**, AR-VLA achieves an average success rate of **61.5%**, higher than the runner-up **CogACT 52.1%**, an improvement of **+9.4 percentage points**.
- Compared with models using the same Paligemma-3B backbone, AR-VLA outperforms **Pi-0-Fast 49.0%** and **Pi-0.5 51.0%**, indicating that the improvement mainly comes from the action expert architecture rather than a stronger perception backbone.
- On single tasks, AR-VLA reaches **75.0%** on the **spoon** task, outperforming **Pi-0-Fast 62.5%** and **Pi-0.5 58.3%**; on the more fine-grained **carrot** task, it reaches **54.2%**, outperforming **29.2%** and **33.3%**.
- The paper also claims that in **simulated and real robot manipulation**, it can replace traditional chunk-based action heads, and that it significantly outperforms reactive baselines in **trajectory smoothness, kinematic consistency, history awareness, and long-horizon task completion ability**.
- Qualitative figures and examples show that AR-VLA generates smoother joint trajectories and succeeds on long-horizon tasks requiring persistent historical awareness, while baselines lacking temporal context such as **DP** and **FM** fail.
- This excerpt does not provide more complete table values for detailed quantitative results (such as real robots, specialist tasks, ablations, or inference frequency), so these parts can only be summarized based on the authors’ qualitative and abstract-level descriptions.

## Link
- [http://arxiv.org/abs/2603.10126v1](http://arxiv.org/abs/2603.10126v1)
