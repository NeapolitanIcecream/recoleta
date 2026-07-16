---
kind: trend
trend_doc_id: 717
granularity: day
period_start: '2026-06-24T00:00:00'
period_end: '2026-06-25T00:00:00'
topics:
- robotics
- vision-language-action models
- online adaptation
- reinforcement learning
- world action models
- humanoid locomotion
run_id: materialize-outputs
aliases:
- recoleta-trend-717
tags:
- recoleta/trend
- topic/robotics
- topic/vision-language-action-models
- topic/online-adaptation
- topic/reinforcement-learning
- topic/world-action-models
- topic/humanoid-locomotion
language_code: zh-CN
---

# 机器人 VLA 研究聚焦部署时适应和控制

## 概览
这一天的机器人研究把视觉-语言-动作（VLA）模型视为已部署的控制系统，需要在硬件约束下完成校准、微调和执行。ICWM、FORCE 和 ACNet 给出了最清晰的证据：设置探测、在线奖励和延迟条件化都能在不重建完整策略的情况下改进控制。

## 研究发现

### 部署时系统识别
ICWM 针对一个具体失效模式：训练后，相机视角、安装偏移和机器人几何形态可能发生变化。机器人先运行一个短暂的安全探测阶段，记录起始图像、动作和结束图像片段，再把这些片段作为策略的上下文前置输入。在 LIBERO 跨视角测试中，它的平均分布外成功率比 Multi-View BC 高 13.0 个百分点，比显式相机角度基线高 9.5 个百分点。消融结果有力支持了这一机制：移除图像会使平均成功率下降 56.4 个百分点，错误上下文的表现比没有上下文更差。

#### 资料来源
- [In-Context World Modeling for Robotic Control](../Inbox/2026-06-24--in-context-world-modeling-for-robotic-control.md): 摘要报告了 ICWM 的探测设置、LIBERO 跨视角增益、真实机器人设置和消融结果。

### 在线奖励作为密集动作监督
两篇 VLA 论文把在线交互转化为更安全的策略改进。FORCE 在更新 actor 之前校准 critic，保留专家缓冲区和 rollout 缓冲区，并向 critic 偏好的动作蒸馏。它报告称，使用 Octo 骨干网络时，在六个 ManiSkill 任务上的平均成功率为 82.3%；在线微调后，在六个真实 Franka 任务上的平均成功率为 98.3%，高于行为克隆的 45.0%。ROAD-VLA 采用 token 级路线：它用校准后的 advantage 估计移动采样动作 token 的 logits，并训练学生模型拟合附近的教师分布。该摘录给出了任务覆盖范围和方法细节，但没有成功率表。

#### 资料来源
- [FORCE: Efficient VLA Reinforcement Fine-Tuning via Value-Calibrated Warm-up and Self-Distillation](../Inbox/2026-06-24--force-efficient-vla-reinforcement-fine-tuning-via-value-calibrated-warm-up-and-self-distillation.md): 摘要给出了 FORCE 的三阶段方法，以及 ManiSkill 和真实 Franka 结果。
- [ROAD-VLA: Robust Online Adaptation via Self-Distillation for Vision-Language-Action Models](../Inbox/2026-06-24--road-vla-robust-online-adaptation-via-self-distillation-for-vision-language-action-models.md): 摘要解释了 ROAD-VLA 的 advantage 引导动作 token 蒸馏和评估范围。

### 动作模块获得专属先验和时序修正
多篇论文把 VLA 模型的动作侧视为瓶颈，并为它单独处理数据和运行时需求。Learning Action Priors 在 VLA 训练前用状态-动作轨迹预训练动作模块，再把解码器复用为动作头。报告中的评估覆盖 LIBERO、RoboCasa 和一个真实 Franka 平台上的 13 个跨具身任务，但摘录没有给出精确成功率。ACNet 处理分块控制中的推理延迟。它根据延迟期间已经执行的运动来条件化下一个动作块，并且在 Kinetix 上只训练约 20% 的参数。在 Meta-World MT50 上，它以 0.74 的平均成功率匹配完整延迟条件重训练，同时报告 91 ms 延迟和 11.0 Hz 控制频率。

#### 资料来源
- [Learning Action Priors for Cross-embodiment Robot Manipulation](../Inbox/2026-06-24--learning-action-priors-for-cross-embodiment-robot-manipulation.md): 摘要描述了仅动作预训练、解码器复用、历史压缩和评估范围。
- [Action ControlNet: A Lightweight Delay-Aware Adapter for Smooth Asynchronous Control in Vision-Language-Action Models](../Inbox/2026-06-24--action-controlnet-a-lightweight-delay-aware-adapter-for-smooth-asynchronous-control-in-vision-language-action-models.md): 摘要报告了 ACNet 的延迟感知适配器设计、参数占比、Meta-World 结果和延迟。

### 世界动作建模和人形机器人数据扩大控制目标
更大的研究表述也更偏向动作中心。World Action Models 按预测是否有助于控制来定义预测动作模型，并按渲染未来、潜在未来或不生成视频的动作推理来组织方法。WOLF-VLA 将 VLA 训练用于全身人形机器人运动，示范由最优控制生成。其数据集包含 MuJoCo 中 RH5 人形机器人上的 277 小时数据，覆盖六类运动任务，共 15,276 个 episode。论文提供了数据集规模和训练细节，但摘录没有给出数值成功率表。

#### 资料来源
- [World Action Models: A Survey](../Inbox/2026-06-24--world-action-models-a-survey.md): 摘要给出了 World Action Models 的定义、输出形态和设计轴。
- [WOLF-VLA: Whole-Body Humanoid Optimal Locomotion Framework for Vision-Language-Action Learning](../Inbox/2026-06-24--wolf-vla-whole-body-humanoid-optimal-locomotion-framework-for-vision-language-action-learning.md): 摘要报告了 WOLF-VLA 的最优控制示范流程和数据集规模。
