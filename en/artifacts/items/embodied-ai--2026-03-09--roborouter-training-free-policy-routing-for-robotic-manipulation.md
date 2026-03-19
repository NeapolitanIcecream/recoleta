---
source: arxiv
url: http://arxiv.org/abs/2603.07892v3
published_at: '2026-03-09T02:14:32'
authors:
- Yiteng Chen
- Zhe Cao
- Hongjia Ren
- Chenjie Yang
- Wenbo Li
- Shiyi Wang
- Yemin Wang
- Li Zhang
- Yanming Shao
- Zhenjun Zhao
- Huiping Zhuang
- Qingyao Wu
topics:
- robot-manipulation
- policy-routing
- training-free
- vision-language-action
- multi-agent-systems
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# RoboRouter: Training-Free Policy Routing for Robotic Manipulation

## Summary
RoboRouter proposes a **training-free** policy routing framework for robotic manipulation. Instead of pursuing a single universal policy, it selects a more suitable policy for each manipulation task from an existing heterogeneous policy pool. Its core idea is to use historical execution experience, similar-task retrieval, and post-execution feedback to consistently outperform any individual policy in both simulation and real-robot settings.

## Problem
- The robotic manipulation field already includes multiple policy paradigms such as VLA, VA, and code-based composition, but **each is strong on specific tasks and weak in cross-task generalization**; no single method wins comprehensively.
- Running all candidate policies and relying on trial and error each time is too costly; meanwhile, training a new router model would introduce the costs of **data, training, and continuously integrating new policies**.
- This matters because robotic systems are rapidly accumulating large numbers of off-the-shelf policies; without efficient ways to combine these “experts,” system capability and scalability will be constrained.

## Approach
- Maintain a **heterogeneous policy pool** and a **historical execution database**; when facing a new task, do not retrain, but first build a multimodal task representation (instruction, image, and metadata extracted by vision models).
- Use vector retrieval to find **similar historical tasks**, then let an LLM-style Router directly predict the policy most likely to succeed for the current task based on those records and each policy’s overall performance.
- After execution, a VLM-style Evaluator reads video frames and standardized metrics (success flag, elapsed time, distance, contact/alignment, etc.) to generate structured feedback; the Recorder writes this information back into the database and routing context, forming an **online closed-loop improvement** process.
- When a new policy is added, only **lightweight evaluation** on a small number of representative tasks is needed before writing it into memory, with no additional training required; task clustering further reduces evaluation overhead.

## Results
- **Simulation (RoboTwin 2.0)**: Across 20 representative tasks with 100 trials per task, RoboRouter achieves an average success rate of **79.85%**, outperforming all single-policy baselines: ACT **55.90%**, DP **51.05%**, DP3 **76.45%**, RDT **60.35%**, \(\pi_0\) **69.90%**, and Code as Policies **54.45%**.
- According to the paper abstract, RoboRouter improves average success rate by **more than 3%** over individual policies in simulation; from Table 1, compared with the strongest single average baseline DP3 (**76.45%**), the gain is about **3.40 percentage points**.
- **Real robot**: Across 5 tasks with 20 trials per task, RoboRouter reaches an average success rate of **47%**, higher than ACT **26%**, DP **18%**, RDT **33%**, and \(\pi_0\) **34%**.
- According to the paper abstract, the average success rate improvement in the real world is **more than 13%**; from Table 2, compared with the strongest single average baseline \(\pi_0\) (**34%**), the gain is about **13 percentage points**.
- Specific real-task examples: on Click Alarmclock, RoboRouter scores **10/20**, outperforming RDT **8/20** and \(\pi_0\) **8/20**; on Open Laptop, RoboRouter scores **9/20**, better than the best single baseline at **8/20**; on Place Container Plate, RoboRouter scores **12/20**, tying the best baseline.
- The paper also claims that the additional latency introduced by routing is small and execution efficiency is largely preserved, but the timing table in the provided excerpt is truncated, so **no complete, verifiable numerical values are provided**.

## Link
- [http://arxiv.org/abs/2603.07892v3](http://arxiv.org/abs/2603.07892v3)
