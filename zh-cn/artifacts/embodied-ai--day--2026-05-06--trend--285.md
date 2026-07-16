---
kind: trend
trend_doc_id: 285
granularity: day
period_start: '2026-05-06T00:00:00'
period_end: '2026-05-07T00:00:00'
topics:
- robot learning
- Vision-Language-Action
- latent actions
- visual foresight
- model predictive control
- world models
run_id: materialize-outputs
aliases:
- recoleta-trend-285
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action
- topic/latent-actions
- topic/visual-foresight
- topic/model-predictive-control
- topic/world-models
language_code: zh-CN
---

# 机器人策略正被紧凑前瞻和可部署控制所衡量

## 概览
当前的重点是让机器人策略在部署约束下保留有用的内部状态。Vision-Language-Action（VLA）工作关注紧凑的空间 token、潜在动作监督和测试时视觉校正。Dream-MPC 把同样的压力带到连续控制中：在线规划，但把模型调用次数压低。

## 研究发现

### Compact spatial foresight for VLA manipulation
ConsisVLA-4D 将空间一致性当作推理预算问题来处理。它保留 32 个与指令相关的视觉 token，在多个摄像头视角之间对齐这些 token，并把几何信息存到紧凑的潜变量 token 中。报告中的提升同时来自准确率和速度：在 LIBERO 上比 OpenVLA 提升 21.6%，推理速度快 2.3 倍；在真实机器人平台上提升 41.5%，推理速度快 2.4 倍。

T³VF 处理的是视觉前瞻 VLA 模型中的另一个失效点。它把预测的未来图像和之后观测到的图像做比较，然后在动作方差较低时只更新可学习的查询 token。在带扰动训练的 LIBERO-Plus 上，它把 Mantis 的平均成功率从 49.3% 提高到 52.1%，在摄像头和光照扰动上的提升更大。

#### 资料来源
- [ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation](../Inbox/2026-05-06--consisvla-4d-advancing-spatiotemporal-consistency-in-efficient-3d-perception-and-4d-reasoning-for-robotic-manipulation.md): Summary of ConsisVLA-4D token compression, multi-view 3D perception, future-scene reasoning, and reported LIBERO and real-world gains.
- [Test-Time Training for Visual Foresight Vision-Language-Action Models](../Inbox/2026-05-06--test-time-training-for-visual-foresight-vision-language-action-models.md): Summary of T³VF test-time training mechanism, filtered updates, and LIBERO-Plus perturbation results.

### Latent action tokens as VLA supervision
这项潜在动作研究给出了许多 VLA 论文缺少的受控比较。它使用一个基于 Qwen3-VL-2B 的统一基线，在四种集成方法下测试基于图像的潜在动作和基于动作的潜在动作。最好的结果取决于任务类型。LA-Direct 在 LIBERO-Long 上达到 96.6%，比基线高 10.8 个百分点。LA-Tok 在 RoboTwin 2.0 上达到 78.0% 的平均成功率，高出 17.5 个百分点，并把 Move Can Pot 这类偏重运动控制的任务从 46% 提升到 70%。

实际含义很清楚：潜在动作在与监督问题匹配时才有用。由图像导出的 token 有助于长时程场景推理。由动作导出的 token 有助于在异构机器人数据上统一运动控制。

#### 资料来源
- [From Pixels to Tokens: A Systematic Study of Latent Action Supervision for Vision-Language-Action Models](../Inbox/2026-05-06--from-pixels-to-tokens-a-systematic-study-of-latent-action-supervision-for-vision-language-action-models.md): Summary of the unified VLA baseline, four latent-action supervision strategies, and LIBERO, LIBERO-Long, and RoboTwin 2.0 results.

### Cheap online planning in latent world models
Dream-MPC 把部署约束这个主题带到了连续控制上。它只从策略先验中采样 5 个候选动作序列，把它们放进一个学习到的潜在世界模型里展开，然后用预测回报和终值只做一步梯度更新。一个不确定性惩罚会压低进入模型误差区域的计划，动作复用则把优化工作带到后续的模型预测控制步骤中。

效率上的说法很具体。在报告的设置里，Dream-MPC 每个时间步只做 15 次世界模型评估，而引用的 MPPI 配置要做 9,216 次。用 BMPC 跑 24 个连续控制任务时，它把 IQM 归一化分数提高 26.7%，把平均归一化分数提高 20.5%。用 TD-MPC2 时，它比只用策略的基线更好，但没有稳定达到带 MPPI 的 TD-MPC2。

#### 资料来源
- [Dream-MPC: Gradient-Based Model Predictive Control with Latent Imagination](../Inbox/2026-05-06--dream-mpc-gradient-based-model-predictive-control-with-latent-imagination.md): Summary of Dream-MPC method, planner settings, evaluation counts, and benchmark results.
