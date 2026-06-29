---
kind: ideas
granularity: day
period_start: '2026-06-04T00:00:00'
period_end: '2026-06-05T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- world models
- test-time compute
- affordance grounding
- policy evaluation
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/test-time-compute
- topic/affordance-grounding
- topic/policy-evaluation
language_code: zh-CN
---

# VLA Robot Policy Preflight

## Summary
机器人团队现在有了在更大规模上硬件运行前测试 VLA 策略的具体办法：用闭环想象 rollout 筛选 checkpoint，用延迟-成功扫参评估 action decoding，用合成 recovery 数据处理失败率高的操作任务。

## Policy-in-the-loop rollout gate for VLA checkpoint promotion
训练 VLA 策略的机器人团队可以在上硬件前加一道门，把每个候选 checkpoint 先跑一遍闭环想象 rollout。策略先预测一个 action chunk，世界模型再预测下一段多视角观测，生成的终端观测再作为策略的下一次输入。这和机器人上的 observe-act 循环一致，也能让团队在花时间做复位、安全检查和重复实机试验之前先做一次更便宜的筛选。

PiL-World 是最清楚的模板。在三个真实双臂任务上，它把真实成功率和想象成功率的平均差距从 Ctrl-World 的 63.2% 降到 12.0%，并报告了跨任务和 checkpoint 设置的 0.94 Pearson 相关系数。一个可行的起点是先在团队已经有真实 rollout 结果的两到三个任务上校准这道门，再看想象 rollout 能否把新 checkpoint 的排序和一小批真实机器人评测保持一致。

### Evidence
- [PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation](../Inbox/2026-06-04--pil-world-a-chunk-wise-world-model-for-vla-policy-in-the-loop-evaluation.md): PiL-World alternates VLA action chunks with generated multi-view observations and reports the real-imagined success-rate gap and correlation.
- [PiL-World: A Chunk-Wise World Model for VLA Policy-in-the-Loop Evaluation](../Inbox/2026-06-04--pil-world-a-chunk-wise-world-model-for-vla-policy-in-the-loop-evaluation.md): The source describes why closed-loop testing is needed for policies that repeatedly observe, act, and re-plan.

## Latency and success sweeps for VLA action generation settings
VLA 部署团队应把 action generation 设置当作控制参数来测，把成功率和每次查询延迟放在同一张表里。值得做的扫参范围很小：扩散式 action head 的单步解码和多步解码，以及支持测试时细化的策略的 latent refinement 宽度和深度。输出应该是机器人控制环里的任务特定工作点，而不是单一基准分数。

两篇论文把这一点说得很清楚。MPCoT 的最佳固定设置 K=5、M=4，把 LIBERO Long 成功率从 95.3% 提高到 98.9%，同时测得延迟从 24 ms 增加到 38 ms，而且没有生成 reasoning token。单步 VLA 论文报告，高噪声偏置的 flow matching 调度让单步 action generation 在 LIBERO 系列测试里能和 10 步解码竞争；在 LIBERO-Plus 上，18 个可比配方都把单步放在了不低于 10 步解码的位置，平均高出 5.4 个成功点。团队可以在自己的任务集上做同样的扫参，并在离线成功率更高但错过控制环截止时间的设置上直接淘汰。

### Evidence
- [MPCoT: Reward-Guided Multi-Path Latent Reasoning for Test-Time Scalable Vision-Language-Action](../Inbox/2026-06-04--mpcot-reward-guided-multi-path-latent-reasoning-for-test-time-scalable-vision-language-action.md): MPCoT reports success gains together with measured latency for latent multi-path refinement.
- [Let It Be Simple: One-Step Action Generation for Vision-Language-Action Models](../Inbox/2026-06-04--let-it-be-simple-one-step-action-generation-for-vision-language-action-models.md): The one-step VLA paper reports one-step versus 10-step decoding results across LIBERO-family benchmarks and a small real-robot check.

## Synthetic recovery trajectory queue for warehouse manipulation failures
仓储机器人团队可以把常见的失败操作案例变成一条 recovery data 队列。流程很具体：收集少量示范和短时 play data，训练 action-conditioned world model，生成候选视频-动作恢复轨迹，过滤那些终点帧和真实示范结果不一致的 rollout，再把过滤后的 recovery 加进 imitation training。

WM-DAgger 给出了这个流程的一个可测起点。在 Soft Bag Pushing 上，5 个真实示范加 1,500 条生成轨迹达到了 93.3% 成功率，而 behavioral cloning 只有 26.7%。同一篇论文还报告了在 seen 和 unseen 的 pick-and-place、ballot insertion 和 towel folding 上的提升。落地时可以先选一个高频失败类，比如可变形袋子推动或一个未见过的包裹抓取，再比较行为克隆策略和在过滤后的合成 recovery 上重新训练后的同一策略。

### Evidence
- [Towards a Data Flywheel for Embodied Intelligence in Logistics](../Inbox/2026-06-04--towards-a-data-flywheel-for-embodied-intelligence-in-logistics.md): WM-DAgger generates and filters synthetic recovery trajectories with an action-conditioned world model and reports task success gains.
- [Towards a Data Flywheel for Embodied Intelligence in Logistics](../Inbox/2026-06-04--towards-a-data-flywheel-for-embodied-intelligence-in-logistics.md): The source frames logistics manipulation as a setting with long-tail operational complexity and limited coverage from curated demonstrations.
