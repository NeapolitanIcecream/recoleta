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
- robot-control
- generalist-robot-policy
- long-horizon-manipulation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# AR-VLA: True Autoregressive Action Expert for Vision-Language-Action Models

## Summary
AR-VLA proposes a truly temporally autoregressive action expert that treats robot control as continuous action-sequence generation, rather than re-predicting a chunk of actions every time it sees a new frame. Its goal is to significantly improve history awareness, trajectory smoothness, and long-horizon control stability while preserving or improving task success rates.

## Problem
- Existing VLA, diffusion-policy, and action-chunking methods are mostly **reactive**: they reset context whenever a new observation arrives and lack persistent action/state memory.
- This kind of “Markovian amnesia” makes it difficult for robots to leverage long-term motion history, leading to control jitter, temporal inconsistency, and failures on long-horizon or partially observable tasks.
- Robotics also faces a **slow-perception / fast-control** frequency mismatch: heavy vision-language backbones update slowly, but motor control requires high-frequency continuous outputs, so a mechanism is needed that can generate actions stably even under visual latency.

## Approach
- Proposes an independent **autoregressive action expert**: like a language model generating text token by token, the model generates continuous actions step by step, explicitly conditioning on past actions and proprioceptive-state history, as well as the most recently available vision-language prefix.
- Designs a **Hybrid Key-Value Cache (HKV)**: memory is split into two streams, with the action/proprioception stream using a long-lived rolling FIFO cache, and the vision-language stream using a low-frequency refreshed semantic-prefix cache with single-slot replacement, thereby decoupling fast control from slow perception.
- Introduces **Dynamic Temporal Re-anchoring (DTR)**: vision-language tokens are tagged with “sampling time” anchors, and the relative-position property of RoPE is used so the model can explicitly understand how “stale” an image is, enabling it to handle asynchronous, multi-latency inputs during both training and inference.
- Uses two-stage training: first **action-only pretraining** to learn kinematic “syntax”; then vision-action alignment, with history dropout to force the model to still use visual prefixes when history is incomplete.

## Results
- In the generalist VLA setting with **BridgeV2 training and SimplerEnv evaluation**, AR-VLA achieves an average success rate of **61.5%**, higher than the runner-up **CogACT 52.1%**, a lead of **+9.4%**.
- Compared with baselines of the same **Paligemma-3B + 300M** scale that share the same VLM backbone, AR-VLA outperforms **Pi-0-Fast 49.0%** and **Pi-0.5 51.0%**.
- In per-task results, AR-VLA reaches **75.0%** on the **spoon** task, above **Pi-0-Fast 62.5%** and **Pi-0.5 58.3%**.
- On the more fine-grained manipulation **carrot** task, AR-VLA reaches **54.2%**, clearly outperforming **Pi-0-Fast 29.2%** and **Pi-0.5 33.3%**.
- The paper also claims that it is better than or no worse than SOTA reactive VLA/diffusion baselines on **real-robot manipulation, expert-policy replacement, trajectory smoothness, and long-horizon tasks**, but the provided excerpt does not include the full quantitative tables for those sections.
- Qualitatively, the authors claim that AR-VLA produces smoother joint trajectories with better kinematic consistency, and succeeds on history-dependent long-horizon tasks such as **PushT2** and **Stack3**, whereas baselines such as **DP** and **FM** fail due to lack of temporal context.

## Link
- [http://arxiv.org/abs/2603.10126v1](http://arxiv.org/abs/2603.10126v1)
