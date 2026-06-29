---
kind: ideas
granularity: week
period_start: '2026-05-04T00:00:00'
period_end: '2026-05-11T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- vision-language-action
- world models
- failure recovery
- long-horizon manipulation
- model release safety
tags:
- recoleta/ideas
- topic/robotics
- topic/vision-language-action
- topic/world-models
- topic/failure-recovery
- topic/long-horizon-manipulation
- topic/model-release-safety
language_code: zh-CN
---

# VLA 策略就绪准入检查

## Summary
机器人 VLA 团队应把不利状态恢复试验、低带宽未来状态测试和发布后所有权检查，放入与名义任务成功率相同的准入检查中。实际变化是：收集失败和恢复 episode，测量紧凑状态在真实推理预算下是否有帮助，并在下游调优后验证已发布策略。

## 面向长时程 VLA 评估的不利状态恢复试验
评估 VLA 策略的机器人团队应在普通任务 rollout 之外，加入受控的接触漂移试验。一个小型测试集可以注入夹爪过早闭合、抓取滑移、抓取位置偏移和抓取姿态不匹配，然后记录策略是否在没有手写重试规则的情况下修复状态。RePO-VLA 使用带有不同标签的成功、失败和恢复 rollout，报告平均对抗成功率从 20% 升至 75%；其 FRBench 协议描述了 46 个任务中的 23,453 个仿真双臂 episode，并定义了错误类型。

这也会改变数据处理方式。失败 rollout 如果包含有用前缀，就应保留；恢复片段应切分出来，让模型从不利状态学习纠正。对于更长的任务序列，ECHO 提供了一个相关测试：存储成功的子目标片段，并在 LIBERO-Long 风格任务上测量检索效果。它报告在 LIBERO-Long 上达到 93.5% 成功率，而原版 π0 为 80.7%；消融实验显示，结构化记忆相对于只用短期缓冲区或扁平记忆有收益。

### Evidence
- [RePO-VLA: Recovery-Driven Policy Optimization for Vision-Language-Action Models](../Inbox/2026-05-10--repo-vla-recovery-driven-policy-optimization-for-vision-language-action-models.md): RePO-VLA 定义了带恢复标签的训练、FRBench 错误注入，以及可恢复操作漂移下的对抗成功率提升。
- [ECHO: Continuous Hierarchical Memory for Vision-Language-Action Models](../Inbox/2026-05-09--echo-continuous-hierarchical-memory-for-vision-language-action-models.md): ECHO 报告了用于长时程 VLA 任务的层级记忆，以及相对原版 π0 的 LIBERO-Long 增益。

## 面向机器人控制环路的令牌预算内未来状态模块
为 VLA 添加世界模型的开发者，应在机器人实际使用的令牌和延迟限制下评测未来状态预测。OneWM-VLA 是一个具体起点：把每个摄像头视角和每一帧压缩成一个语义令牌，同时生成未来潜在令牌和动作块，并在推理时只执行动作流。该论文报告 LIBERO 平均成功率为 98.1%，LIBERO-Long 成功率为 95.6%，同时只在基本冻结的 π0 上训练 14.71M 个 LoRA 参数。

一个实用评估是固定训练预算和固定控制环路延迟下的带宽扫描。ConsisVLA-4D 为多视角设置提供了另一个实现目标：保留与指令相关的物体令牌，将它们与跨视角 3D 特征对齐，并在推理时使用学习到的动态令牌和深度令牌。它报告相对 OpenVLA 在 LIBERO 上有 2.3x 推理加速，并称其未来场景令牌在推理时占观察-指令序列的比例低于 10%。

### Evidence
- [One Token Per Frame: Reconsidering Visual Bandwidth in World Models for VLA Policy](../Inbox/2026-05-08--one-token-per-frame-reconsidering-visual-bandwidth-in-world-models-for-vla-policy.md): OneWM-VLA 展示了每帧一个语义令牌、联合潜在-动作生成、LoRA 规模适配，以及 LIBERO 和真实机器人结果。
- [ConsisVLA-4D: Advancing Spatiotemporal Consistency in Efficient 3D-Perception and 4D-Reasoning for Robotic Manipulation](../Inbox/2026-05-06--consisvla-4d-advancing-spatiotemporal-consistency-in-efficient-3d-perception-and-4d-reasoning-for-robotic-manipulation.md): ConsisVLA-4D 报告了紧凑的多视角物体和几何令牌、未来场景推理，以及相对 OpenVLA 的推理加速。

## 面向微调后 VLA 策略的发布后水印审计
发布 VLA checkpoint 的组织应在下游微调前后加入所有权和行为审计。GuardVLA 在带有固定 6-bit 隐写消息的具身图像上训练受保护模型，然后通过换入触发投影器和分类头来检查水印识别置信度。审计从良性任务成功率开始，因此验证路径不依赖于迫使机器人执行不安全的触发动作。

报告中的数字足以用于发布清单。在采用 OpenVLA-OFT 的 LIBERO 上，带水印模型在各套件上的水印识别置信度约为 99.7% 到 100%，而干净模型接近 0。良性成功率接近干净基线；从 LIBERO-10 下游适配到 LIBERO-Spatial 后，成功率稳定在约 99%，水印识别仍接近 100%。

### Evidence
- [Towards Backdoor-Based Ownership Verification for Vision-Language-Action Models](../Inbox/2026-05-09--towards-backdoor-based-ownership-verification-for-vision-language-action-models.md): GuardVLA 描述了一种面向 VLA 的水印和审计方法，并给出了 LIBERO WIC、良性成功率和下游适配结果。
