---
kind: ideas
granularity: day
period_start: '2026-05-06T00:00:00'
period_end: '2026-05-07T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robot learning
- Vision-Language-Action
- latent actions
- visual foresight
- model predictive control
- world models
tags:
- recoleta/ideas
- topic/robot-learning
- topic/vision-language-action
- topic/latent-actions
- topic/visual-foresight
- topic/model-predictive-control
- topic/world-models
language_code: zh-CN
---

# Targeted VLA Adaptation Tests

## Summary
机器人团队现在有了针对三个落地阻力的具体测试：混合机器人的动作标签、部署时的视觉条件漂移，以及昂贵的在线规划。共同的检查很简单，也能量化：在可能的情况下固定基座模型，加一个针对性的控制或监督机制，然后比较成功率和推理成本。

## Task-specific latent action supervision tests for VLA training
使用混合机器人数据集的 VLA 训练团队，应在确定训练方案前先做一轮小规模的 latent action 监督对比。实用的划分很直接：面向长时程场景推理的基于图像的 latent action token，和面向动作格式不一致、且偏重运动控制任务的基于动作的 latent action token。

`From Pixels to Tokens` 里的受控比较让这个测试可以直接执行，因为它固定了基于 Qwen3-VL-2B 的 VLA 基线，只比较四种集成方法。LA-Direct 在 LIBERO-Long 上达到 96.6%，基线是 85.8%；LA-Tok 在 RoboTwin 2.0 上的平均成功率是 78.0%，基线是 60.5%。一个成本较低的内部版本可以用冻结的 latent-action 模型训练同一个 backbone，跑一个长时程基准和一个偏运动控制的基准，然后在扩数据前按任务类型选监督路径。

### Evidence
- [From Pixels to Tokens: A Systematic Study of Latent Action Supervision for Vision-Language-Action Models](../Inbox/2026-05-06--from-pixels-to-tokens-a-systematic-study-of-latent-action-supervision-for-vision-language-action-models.md): Summarizes the controlled latent-action comparison, the heterogeneous action-label problem, the four integration methods, and the main LIBERO and RoboTwin results.
- [From Pixels to Tokens: A Systematic Study of Latent Action Supervision for Vision-Language-Action Models](../Inbox/2026-05-06--from-pixels-to-tokens-a-systematic-study-of-latent-action-supervision-for-vision-language-action-models.md): The paper abstract states the image-based versus action-based formulation split and the reported task correspondence.

## Filtered test-time visual correction for Visual Foresight VLA deployments
部署 Visual Foresight VLA 策略的团队，应为相机、光照、背景和布局变化测试一条窄范围的 test-time 更新流程。做法很具体：保存模型预测的未来图像，把它和之后观测到的图像对比，并且只在采样动作方差较低时更新可学习的 query token。

T³VF 给出了第一次复现可直接用的默认值：预测间隔 `n=4`、批大小 `B=4`、`K=5` 个动作样本、10 个样本的方差缓冲区，以及 `ρ=0.3` 的低分位更新阈值。在带扰动训练的 LIBERO-Plus 上，Mantis + T³VF 的平均成功率是 52.1%，Mantis 是 49.3%，在 Camera 和 Light 扰动上的提升更大。Robot 扰动下报告的运行时开销大约是基础每回合时间的 1.3×，低于不加筛选的 test-time training，后者大约是 1.7×。

### Evidence
- [Test-Time Training for Visual Foresight Vision-Language-Action Models](../Inbox/2026-05-06--test-time-training-for-visual-foresight-vision-language-action-models.md): Gives the T³VF mechanism, filtering rule, hyperparameters, perturbation results, and runtime comparison.
- [Test-Time Training for Visual Foresight Vision-Language-Action Models](../Inbox/2026-05-06--test-time-training-for-visual-foresight-vision-language-action-models.md): Explains the self-supervised pair formed by the predicted future image and later observation, plus the practical problem of noisy test-time updates.
- [Test-Time Training for Visual Foresight Vision-Language-Action Models](../Inbox/2026-05-06--test-time-training-for-visual-foresight-vision-language-action-models.md): Describes action-variance filtering and the adaptive variance buffer used to decide when updates are safe.

## Low-call MPC benchmark for learned world-model controllers
付不起大规模 MPPI rollout 成本的控制团队，应在只用策略的控制器和基于采样的规划器旁边，再加一个低调用次数的 MPC 基准。可采用 Dream-MPC 的做法：从策略先验里采样五组动作序列，把它们送入学到的 latent world model，在预测回报上做一步梯度更新，惩罚 epistemic uncertainty，并在 receding-horizon 步骤之间复用已经优化过的动作。

报告中的预算已经足够做工程门槛：Dream-MPC 设置下每个时间步要 15 次 world-model 评估，而引用的 MPPI 配置是 9,216 次。在 BMPC 的 24 个连续控制任务上，Dream-MPC 的 IQM normalized score 比 BMPC 高 26.7%，mean normalized score 高 20.5%。在 TD-MPC2 上，它比只用策略的基线更好，但不能稳定达到带 MPPI 的 TD-MPC2，所以内部测试应当看在机器人实际硬件预算下，每次 world-model 调用能拿到多少分。

### Evidence
- [Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination](../Inbox/2026-05-06--dream-mpc-gradient-based-model-predictive-control-with-latent-imagination.md): Summarizes the Dream-MPC problem, planner design, default budget, score gains, and comparison with MPPI and policy-only baselines.
- [Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination](../Inbox/2026-05-06--dream-mpc-gradient-based-model-predictive-control-with-latent-imagination.md): Describes why sampling-based MPC is costly on embedded systems and high-dimensional control tasks.
- [Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination](../Inbox/2026-05-06--dream-mpc-gradient-based-model-predictive-control-with-latent-imagination.md): States Dream-MPC’s use of gradient-based MPC with a learned policy and world model, including uncertainty and action reuse.
