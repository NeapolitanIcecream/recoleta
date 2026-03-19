---
source: arxiv
url: http://arxiv.org/abs/2603.14523v1
published_at: '2026-03-15T17:59:51'
authors:
- Chaoyang Wang
- Wenrui Bao
- Sicheng Gao
- Bingxin Xu
- Yu Tian
- Yogesh S. Rawat
- Yunhao Ge
- Yuzhang Shang
topics:
- vision-language-action
- embodied-reasoning
- chain-of-thought
- tool-use
- robot-manipulation
- long-horizon
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# VLA-Thinker: Boosting Vision-Language-Action Models through Thinking-with-Image Reasoning

## Summary
VLA-Thinker proposes a "thinking-with-image" paradigm that lets robots actively look at images again during reasoning, rather than treating vision only as one-shot context. The method targets vision-language-action models, with a focus on improving robustness and success rates in long-horizon manipulation.

## Problem
- Existing CoT-enhanced VLAs are still largely based on **text-style reasoning**: images are encoded only once, and subsequent thinking happens mainly in the language space, making it hard to continuously leverage visual information.
- This static visual context weakens the model's ability to **disambiguate, track subgoals, and correct intermediate errors**, especially in long-horizon manipulation tasks.
- Directly learning the full mapping from perception to action typically **requires large amounts of data and lacks robustness**, so a stronger "think-before-acting" mechanism is needed.

## Approach
- The core idea is to treat **visual perception as a callable reasoning action**: during thinking, the model can invoke visual tools to obtain task-relevant local images, then continue reasoning and output actions.
- The paper formalizes the process as an interleaved trajectory of **text reasoning steps + tool invocation + returned visual evidence + action**, rather than producing actions directly after a single image pass.
- The current implementation uses a representative visual tool, **ZOOM-IN**, to inspect details in specified regions, thereby testing whether the "interleaved perception-reasoning-action" paradigm itself is effective.
- Training uses two stages: first, **SFT cold start** on synthetic embodied CoT data so the model learns structured reasoning and tool-use formats; then **GRPO** for trajectory-level reinforcement learning, aligning complete reasoning-action trajectories with task success.
- To construct supervision data, the authors use **Qwen3-VL-30B-A3B-Instruct** to generate CoT annotations with tool calls, and clean the data through schema checks and temporal consistency constraints.

## Results
- On **LIBERO**, VLA-Thinker achieves an average success rate of **97.5%**, a **+6.5 percentage point** improvement over its backbone **OpenVLA-OFT 91.0%**.
- LIBERO subset results: **Spatial 98.7 vs 91.6 (+7.1)**, **Object 99.0 vs 95.3 (+3.7)**, **Goal 95.2 vs 90.6 (+4.6)**, **Long 96.9 vs 86.5 (+10.4)**; the improvement is most pronounced on the long-horizon subset.
- On the 4 short-horizon tasks in **RoboTwin 2.0**, the average success rate is **62.3%**, versus **OpenVLA-OFT 21.3%**, an improvement of **+41.0**; examples include **Lift Pot 64.8 vs 10.1** and **Beat Hammer Block 82.5 vs 28.1**.
- On the 4 medium-horizon tasks in RoboTwin 2.0, the average is **70.7%**, compared with **47.1%**, an improvement of **+23.6**; examples include **Move Can Pot 61.0 vs 28.1**, **Place Empty Cup 92.7 vs 77.3**, and **Handover Mic 89.9 vs 45.3**.
- On the 4 long/extra-long-horizon tasks in RoboTwin 2.0, the average is **64.6%**, compared with **46.5%**, an improvement of **+18.1**; examples include **Handover Block 52.8 vs 33.1**, **Stack Bowls Two 71.1 vs 40.6**, **Blocks Rank RGB 79.3 vs 70.2**, and **Put Bottles Dustbin 55.4 vs 42.2**.
- The authors also claim this is the **first VLA model to support thinking-with-image reasoning**, and that it still achieves better performance using only single-view image input (compared with the official OpenVLA-OFT, which also uses a wrist camera).

## Link
- [http://arxiv.org/abs/2603.14523v1](http://arxiv.org/abs/2603.14523v1)
