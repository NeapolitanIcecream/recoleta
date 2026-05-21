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

# 有针对性的 VLA 适配测试

## Summary
机器人团队现在有了针对三个采用阻碍的具体测试：混合机器人动作标签、部署时视觉条件漂移，以及昂贵的在线规划。共同检查项小而可测：在可行时固定基础模型，加入一个有针对性的控制或监督机制，然后比较成功率和推理成本。

## 面向 VLA 训练的任务特定潜在动作监督测试
使用混合机器人数据集的 VLA 训练团队，应在确定单一训练方案前，加入一轮小规模潜在动作监督扫测。实用的划分很明确：长时域场景推理用基于图像的潜在动作 token，动作格式不一致且运动控制占主要难度的任务用基于动作的潜在动作 token。

`From Pixels to Tokens` 中的受控比较让这个测试可以直接执行，因为它固定了基于 Qwen3-VL-2B 的 VLA 基线，并比较了四种集成方法。LA-Direct 在 LIBERO-Long 上达到 96.6%，基线为 85.8%；LA-Tok 在 RoboTwin 2.0 上达到 78.0% 平均成功率，基线为 60.5%。一个低成本的内部版本可以用冻结的潜在动作模型训练同一个 backbone，运行一个长时域基准和一个运动控制占主要难度的基准，然后在扩大数据采集前按任务族选择监督路径。

### Evidence
- [From Pixels to Tokens: A Systematic Study of Latent Action Supervision for Vision-Language-Action Models](../Inbox/2026-05-06--from-pixels-to-tokens-a-systematic-study-of-latent-action-supervision-for-vision-language-action-models.md): 概述了受控的潜在动作比较、异构动作标签问题、四种集成方法，以及主要的 LIBERO 和 RoboTwin 结果。
- [From Pixels to Tokens: A Systematic Study of Latent Action Supervision for Vision-Language-Action Models](../Inbox/2026-05-06--from-pixels-to-tokens-a-systematic-study-of-latent-action-supervision-for-vision-language-action-models.md): 论文摘要说明了基于图像和基于动作的表述划分，以及报告的任务对应关系。

## 用于 Visual Foresight VLA 部署的过滤式测试时视觉校正
部署 Visual Foresight VLA 策略的团队，应针对摄像头、光照、背景和布局变化测试一个范围较窄的测试时更新循环。具体做法是：存储模型预测的未来图像，将它与随后观察到的图像比较，并且只在采样动作方差较低时更新可学习的 query token。

T³VF 给出了第一次复现可用的默认值：预测间隔 `n=4`、批大小 `B=4`、`K=5` 个动作样本、大小为 10 的方差缓冲区，以及低分位更新阈值 `ρ=0.3`。在带扰动训练的 LIBERO-Plus 上，Mantis + T³VF 达到 52.1% 平均成功率，Mantis 为 49.3%；在 Camera 和 Light 扰动上的增益更大。Robot 扰动上报告的运行时成本约为基础单 episode 时间的 1.3×，低于未过滤测试时训练的约 1.7×。

### Evidence
- [Test-Time Training for Visual Foresight Vision-Language-Action Models](../Inbox/2026-05-06--test-time-training-for-visual-foresight-vision-language-action-models.md): 给出了 T³VF 机制、过滤规则、超参数、扰动结果和运行时比较。
- [Test-Time Training for Visual Foresight Vision-Language-Action Models](../Inbox/2026-05-06--test-time-training-for-visual-foresight-vision-language-action-models.md): 解释了由预测未来图像和随后观察结果组成的自监督样本对，以及测试时更新噪声带来的实际问题。
- [Test-Time Training for Visual Foresight Vision-Language-Action Models](../Inbox/2026-05-06--test-time-training-for-visual-foresight-vision-language-action-models.md): 描述了动作方差过滤，以及用于判断何时可以安全更新的自适应方差缓冲区。

## 面向学习型世界模型控制器的低调用量 MPC 基准
无法承担大规模 MPPI rollout 成本的控制团队，应在纯策略控制器和基于采样的规划器旁边加入一个低调用量 MPC 基准。候选实现采用 Dream-MPC 的方案：从策略先验中采样五条动作序列，在学到的潜在世界模型中 rollout，对预测回报执行一步梯度更新，惩罚认知不确定性，并在滚动时域步骤之间复用已优化的动作。

报告的预算足够作为工程门槛：Dream-MPC 设置中每个时间步进行 15 次世界模型评估，而引用的 MPPI 配置为 9,216 次。在 24 个连续控制任务上使用 BMPC 时，Dream-MPC 相比 BMPC 将 IQM 归一化得分提高 26.7%，将平均归一化得分提高 20.5%。使用 TD-MPC2 时，它优于纯策略基线，但没有稳定达到 TD-MPC2 with MPPI 的水平。因此，合适的内部测试是在机器人将使用的硬件预算下，比较每次世界模型调用带来的得分。

### Evidence
- [Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination](../Inbox/2026-05-06--dream-mpc-gradient-based-model-predictive-control-with-latent-imagination.md): 概述了 Dream-MPC 的问题、规划器设计、默认预算、得分增益，以及与 MPPI 和纯策略基线的比较。
- [Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination](../Inbox/2026-05-06--dream-mpc-gradient-based-model-predictive-control-with-latent-imagination.md): 说明了基于采样的 MPC 为什么在嵌入式系统和高维控制任务上成本高。
- [Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination](../Inbox/2026-05-06--dream-mpc-gradient-based-model-predictive-control-with-latent-imagination.md): 说明了 Dream-MPC 使用带学习策略和世界模型的基于梯度的 MPC，并包含不确定性和动作复用。
