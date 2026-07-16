---
kind: ideas
granularity: day
period_start: '2026-05-25T00:00:00'
period_end: '2026-05-26T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- vision-language-action models
- world models
- reinforcement learning
- robot deployment
- adversarial reliability
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action-models
- topic/world-models
- topic/reinforcement-learning
- topic/robot-deployment
- topic/adversarial-reliability
language_code: zh-CN
---

# Factory VLA Execution Checks

## 摘要
制造机器人团队可以用任务级失败日志、小规模在线微调试验和对抗图像检查，让 VLA 试点更具体。共同的做法是把真实执行、action chunk 和视觉失败案例都放进通过/失败门槛里。

## Failure-coded rollout logs for factory VLA packaging pilots
工厂 VLA 试点需要按每个 episode 记录失败标签，并和生产质量检查对齐。西门子包装研究给出了一套适合透明配件袋装入任务的起始分类：产品上方残留内容物、抓到多个袋子、插入不完整、抓取差或抓取失败。报告中最常见的问题是内容物留在产品上方，占无约束失败 episode 的 65%。

制造自动化团队可以把这些标签加到每次 rollout 复核里，并在每轮评估后围绕占比最高的类别收集恢复 episode。同一轮复核也可以把受限和无约束试验分开记录，因为西门子团队先简化任务，再在后续轮次里逐步取消约束。一个低成本试点就是一个包装工位、一套 VLA policy、30 次清空料箱式评估，以及一条规则：下一轮数据收集优先覆盖前两个失败类别。

### 资料来源
- [A Factory-Floor Deployment Case Study of VLA Pipelines for Industrial Packaging Task: Workflow, Failures, and Lessons](../Inbox/2026-05-25--a-factory-floor-deployment-case-study-of-vla-pipelines-for-industrial-packaging-task-workflow-failures-and-lessons.md): Reports the Siemens factory packaging task, 2,535 episodes, iterative fine-tuning workflow, constrained-to-unconstrained rollout plan, and failure breakdown.
- [A Factory-Floor Deployment Case Study of VLA Pipelines for Industrial Packaging Task: Workflow, Failures, and Lessons](../Inbox/2026-05-25--a-factory-floor-deployment-case-study-of-vla-pipelines-for-industrial-packaging-task-workflow-failures-and-lessons.md): Confirms the factory task setup and the repeated loop of data collection, curation, fine-tuning, evaluation, and targeted recovery data collection.

## Operator-corrected replay buffers for action-chunk VLA fine-tuning
把预训练 VLA 适配到新操作任务的机器人团队，可以试一个小型在线 RL 回路，在保留基础 policy 的同时编辑 action chunk。EXPO-FT 在预训练 π0.5 policy 上训练一个轻量编辑 policy，让 Q-function 在基础动作和编辑后的动作之间选择，并把人工对 action chunk 内单个时间步的修正存进回放缓冲区。

这个试验范围很窄：运行零样本 policy，加入稀疏二元奖励和基于规则的成功检测器，收集带操作员修正的在线 rollout，然后做 30 次人工判定的评估试验。EXPO-FT 报告在 8 个真实操作任务上都达到 30/30 的最终成功率，平均只用了 19.1 分钟的在线机器人数据。这个结果说明，可以在精密操作任务上测试 edit-policy 回路，因为完整任务数据采集通常要花几天。

### 资料来源
- [EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models](../Inbox/2026-05-25--expo-ft-sample-efficient-reinforcement-learning-finetuning-for-vision-language-action-models.md): Describes EXPO-FT’s pretrained VLA edit policy, action-chunk RL, operator corrections, sparse rewards, and reported 30/30 success after 19.1 minutes of online data.
- [EXPO-FT: Sample-Efficient Reinforcement Learning Finetuning for Vision-Language-Action Models](../Inbox/2026-05-25--expo-ft-sample-efficient-reinforcement-learning-finetuning-for-vision-language-action-models.md): Confirms the paper’s claim of perfect task performance across evaluated manipulation tasks within an average of 19.1 minutes of online robot data.

## Pre-flight adversarial image tests for VLA robot policies
VLA 部署清单里应加入图像扰动测试，用来测动作变化，而不只是看干净任务成功率。对抗可靠性论文引用了 OpenVLA-7B 在 16/255 的 PGD 图像攻击下，LIBERO 成功率从 95% 以上跌到 5% 以下，并把问题归结为物理动作安全，因为模型输出会直接驱动机器人。

一个实用审计可以在留出的数据集上运行 PGD 和 Square 攻击，对比短时域内干净动作和受攻击动作，并计算论文中的 encoder-specific ceiling 或 head-agnostic robustness ratio。论文说这些诊断最多用 200 个样本就能算出，并报告在覆盖 OpenVLA、LIBERO 套件、攻击类型、最长到 10 的时域，以及两种 action-head 设计的 320 个验证单元里没有出现边界违例。这给机器人集成人员一个小型的上机前测试，可在有人附近的现场试验前检查面向相机的 policy。

### 资料来源
- [Capability and Robustness Cannot Both Be Free: An Information-Theoretic Bound for Vision-Language-Action Models](../Inbox/2026-05-25--capability-and-robustness-cannot-both-be-free-an-information-theoretic-bound-for-vision-language-action-models.md): Summarizes the capability and adversarial reliability bound, the OpenVLA PGD drop, the 320-cell validation, and diagnostics computable from at most 200 samples.
- [Capability and Robustness Cannot Both Be Free: An Information-Theoretic Bound for Vision-Language-Action Models](../Inbox/2026-05-25--capability-and-robustness-cannot-both-be-free-an-information-theoretic-bound-for-vision-language-action-models.md): Confirms the paper’s reported zero violations and the proposed pre-flight encoder ceiling, defense-forensics probe, and head-agnostic robustness ratio.
