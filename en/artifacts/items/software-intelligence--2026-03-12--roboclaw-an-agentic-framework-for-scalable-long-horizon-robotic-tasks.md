---
source: arxiv
url: http://arxiv.org/abs/2603.11558v1
published_at: '2026-03-12T05:22:59'
authors:
- Ruiying Li
- Yunlang Zhou
- YuYao Zhu
- Kylin Chen
- Jingyuan Wang
- Sukai Wang
- Kongtao Hu
- Minhui Yu
- Bowen Jiang
- Zhan Su
- Jiayao Ma
- Xin He
- Yongjian Shen
- Yangyang
- Guanghui Ren
- Maoqing Yao
- Wenhao Wang
- Yao Mu
topics:
- agentic-robotics
- long-horizon-planning
- vision-language-action
- autonomous-data-collection
- process-supervision
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# RoboClaw: An Agentic Framework for Scalable Long-Horizon Robotic Tasks

## Summary
RoboClaw is a unified agentic framework for long-horizon robotic manipulation that places data collection, policy learning, and deployment execution into the same VLM-driven closed loop. Its core selling point is improving robustness on long-chain tasks and reducing human involvement through a self-resetting data collection mechanism and process supervision during deployment.

## Problem
- Existing VLA robotic pipelines usually separate **data collection, training, and deployment**, leading to semantic inconsistency and train-execution distribution mismatch, with errors easily accumulating in long-horizon tasks.
- Real-world robot data collection depends heavily on humans: demonstrations, environment resets, failure monitoring, trajectory filtering, and deployment supervision are all time-consuming and hard to scale.
- Multi-policy sequential execution is typically open-loop or brittle, lacking runtime supervision and recovery mechanisms, which leads to low success rates on complex long-chain operations.

## Approach
- Use a **VLM meta-controller** to unify the entire lifecycle: perform high-level reasoning, select subtasks, and invoke tools and policies based on visual observations and structured memory.
- Propose **Entangled Action Pairs (EAP)**: pair a “forward manipulation policy” with an “inverse reset policy” to form a **self-resetting loop**, allowing the robot to continuously collect online data without requiring frequent manual environment resets.
- The system adopts a **Skills–Tools–Policies** hierarchy: high-level skill orchestration, mid-level MCP tool invocation, and low-level VLA policy execution, thereby connecting reasoning with control.
- During deployment, the same agent continuously queries environment summaries and robot state, and dynamically decides whether to **continue, retry, switch policies, recover, or request human intervention**, effectively adding process supervision to multi-step tasks.
- Execution trajectories flow back into the training dataset, forming a closed loop of continuous improvement, so deployment itself also becomes a source of learning.

## Results
- The paper claims that on real-world long-horizon tasks, RoboClaw achieves a **25% improvement in success rate** over baseline methods while **reducing human time investment by 53.7%**.
- In terms of data collection efficiency, if RoboClaw’s human effort is normalized to 1, the purely manual baseline requires about **2.16×** more human time, and about **8.04×** more human intervention during rollout.
- The success rates of the inverse reset policies on 4 tasks are: **Body Lotion 36/50, Primer 38/50, Lipstick 43/50, Tissue Wipe 39/50**.
- The forward manipulation policies improve substantially after 5 iterations: Body Lotion **21/50 → 43/50**, Primer **23/50 → 40/50**, Lipstick **2/50 → 23/50**, Tissue Wipe **11/50 → 26/50**.
- Figure 4 shows that on the vanity table organization long-chain task, RoboClaw significantly outperforms the end-to-end VLA baseline as well as the expected success rate obtained from the “product of 4 independent subtask success rates”; the results are based on the **average over 20 trials**, but the full numerical values for that figure are not provided in the excerpt.

## Link
- [http://arxiv.org/abs/2603.11558v1](http://arxiv.org/abs/2603.11558v1)
