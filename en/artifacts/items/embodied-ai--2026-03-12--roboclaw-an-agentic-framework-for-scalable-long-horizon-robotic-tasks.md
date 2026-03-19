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
- vision-language-action
- long-horizon-robotics
- agentic-framework
- autonomous-data-collection
- skill-orchestration
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# RoboClaw: An Agentic Framework for Scalable Long-Horizon Robotic Tasks

## Summary
RoboClaw is a unified agent framework for long-horizon robotic manipulation that places data collection, policy learning, and deployment execution into the same VLM-driven closed loop. Its key idea is to let the robot self-reset using paired "execute-reset" actions, while during deployment the same agent dynamically schedules skills and recovery policies.

## Problem
- Existing VLA robotic systems tend to fail on long-horizon tasks because data collection, training, and deployment are usually fragmented from one another, leading to inconsistent task semantics and state distributions.
- Real-robot data collection depends heavily on human labor: demonstrations, environment resets, failure monitoring, trajectory filtering, and deployment supervision are all time-consuming and difficult to scale.
- In long-chain multi-skill execution, small early errors can cascade and amplify; lacking runtime supervision and recovery mechanisms makes multi-policy systems very brittle.

## Approach
- Use an off-the-shelf vision-language model as a meta-controller, combining visual observations with structured memory to perform high-level reasoning, subtask selection, tool calling, and skill orchestration.
- Design a three-layer structure: Policies handle low-level action generation, Tools provide interfaces for launching/switching policies and querying the environment, and Skills organize tools into reusable procedures.
- Propose **Entangled Action Pairs (EAP)**: pair a forward manipulation policy with an inverse recovery/reset policy to form a self-resetting loop of "do, then undo," enabling continuous online data collection.
- During deployment, continue using the same agentic closed loop to continuously check whether subtasks are completed; if they fail, retry, switch policies, call recovery skills, and request human intervention only when necessary.
- Trajectories generated during execution are also fed back into the training set, forming a lifecycle closed-loop learning process under unified semantics.

## Results
- The paper claims that on real-world long-horizon tasks, RoboClaw improves task success rate by **25%** compared with baseline methods.
- The paper claims that across the robot lifecycle, human time investment is reduced by **53.7%**.
- With the same amount of data, the purely human data-collection baseline requires about **2.16×** as much human time; during rollout it requires about **8.04×** as much human intervention, while RoboClaw can complete most of the process autonomously.
- The inverse reset policy achieved success rates of **36/50, 38/50, 43/50, 39/50** on four single-skill tasks, respectively (Body Lotion, Primer, Lipstick, Tissue Wipe).
- After 5 rounds of iteration, the forward manipulation policy improved across the four tasks from **21/50, 23/50, 2/50, 11/50** in round 1 to **43/50, 40/50, 23/50, 26/50** in round 5, showing that online collection and iterative optimization are effective.
- The figure also claims that on the vanity table organization long-horizon task, RoboClaw significantly outperforms the end-to-end VLA baseline as well as the expected success rate obtained from the "product of independent subtask success rates"; the result is based on **20 trials**, but the excerpt does not provide the full baseline values.

## Link
- [http://arxiv.org/abs/2603.11558v1](http://arxiv.org/abs/2603.11558v1)
