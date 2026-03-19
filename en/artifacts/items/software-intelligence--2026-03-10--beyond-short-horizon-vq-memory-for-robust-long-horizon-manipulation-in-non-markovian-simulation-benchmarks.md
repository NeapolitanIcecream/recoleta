---
source: arxiv
url: http://arxiv.org/abs/2603.09513v1
published_at: '2026-03-10T11:13:54'
authors:
- Wang Honghui
- Jing Zhi
- Ao Jicong
- Song Shiji
- Li Xuelong
- Huang Gao
- Bai Chenjia
topics:
- robot-manipulation
- long-horizon-planning
- non-markovian-tasks
- vq-vae
- temporal-memory
relevance_score: 0.16
run_id: materialize-outputs
language_code: en
---

# Beyond Short-Horizon: VQ-Memory for Robust Long-Horizon Manipulation in Non-Markovian Simulation Benchmarks

## Summary
This paper proposes RuleSafe, a new benchmark for long-horizon, non-Markovian robotic manipulation, along with a lightweight temporal memory method called VQ-Memory. The core idea is to compress past proprioceptive joint states into discrete memory tokens, helping policies distinguish between manipulation processes that look visually similar but are actually at different stages.

## Problem
- Existing robotic simulation benchmarks are mostly short-horizon, simple pick-and-place tasks, making them inadequate for covering complex real-world manipulation involving locks and multi-joint dependencies.
- Such tasks exhibit **non-Markovianity**: from only the current image, it is often impossible to tell which step of the task has been reached, so policies tend to fail in long sequential manipulation chains.
- Directly using visual history is computationally expensive, while directly using raw joint-state history is sensitive to noise and prone to trajectory overfitting.

## Approach
- Proposes **RuleSafe**: a benchmark for safe manipulation generated with LLM assistance, containing 20 lock rules such as key, password, and logic, emphasizing multi-stage reasoning and manipulation dependencies.
- Constructs tasks using two types of hidden states: **part-phase**, representing discrete part states, and **task-phase**, representing multi-stage task progress, thereby systematically generating long-horizon, non-Markovian tasks.
- Proposes **VQ-Memory**: first encodes a past sequence of joint states into discrete tokens using a VQ-VAE, then further compresses the redundant codebook through post-processing clustering into coarser-grained, more stable semantic memory.
- This memory representation is model-agnostic: for VLA models it can be injected as special language tokens, while for diffusion policies it is mapped to additional latent-variable inputs.
- To improve efficiency, the authors use a larger temporal window and stride (**window=50, stride=20**), claiming an approximately **20× compression ratio**, reducing computational burden while preserving phase information.

## Results
- The RuleSafe benchmark contains **20** lock rules and **10** safe categories; the average success rate of generated demonstrations is **71.7%**, with an average trajectory length of **638 frames**, indicating substantial task complexity.
- Evaluation covers multiple policies including DP3, RDT, CogACT, and π0; the paper explicitly claims that VQ-Memory consistently improves **long-horizon planning**, **unseen configuration generalization**, and reduces computational cost across single-task, multi-task, and different architectures.
- VQ-Memory’s discrete memory is clustered from an original codebook size of **256** to a final vocabulary size of **4**, with a memory token length of **40**; compared with directly retaining continuous history, the method emphasizes stronger robustness and lower redundancy.
- The paper excerpt does not provide a complete quantitative comparison table for each model on specific datasets/rules (such as exact SR/PS improvement margins or relative baseline values), so it is not possible to list precise per-setting performance gains.
- In the experimental setup, single-task training uses **100 demonstrations/task**; multi-task training uses a total of **1000 trajectories** (**50** per task), to validate cross-task generalization and adaptability.

## Link
- [http://arxiv.org/abs/2603.09513v1](http://arxiv.org/abs/2603.09513v1)
