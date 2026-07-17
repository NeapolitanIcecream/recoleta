---
source: arxiv
url: https://arxiv.org/abs/2607.14698v1
published_at: '2026-07-16T08:01:49'
authors:
- Marino Watanabe
- Takami Sato
- Kentaro Yoshioka
topics:
- vision-language-action
- robot-foundation-model
- adversarial-robustness
- sim2real
- robot-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Lights, Camera, Malfunction: When Illumination Robustness Leaves VLA Models Blind to Color

## Summary
## 总结
FLARE 表明，固定式物理聚光灯会严重干扰 VLA 机器人策略；而朴素的颜色增强可能通过让模型忽略颜色来掩盖这一脆弱性。ChromaGuard 在对抗训练过程中保留色相线索，改善了照明鲁棒性与依赖颜色的操作任务之间的平衡。

## 问题
- VLA 模型在幅度较小且符合物理规律的照明变化下可能失效；这一点很重要，因为在实际部署中，错误的轨迹可能导致操作失败和碰撞风险。
- 朴素的颜色与照明增强可能通过丢弃颜色信息，而不是学习对照明变化不敏感的视觉特征，来提高模型在攻击下的成功率。

## 方法
- FLARE 将攻击者视为黑盒：使用贝叶斯优化调整固定聚光灯的色相、饱和度、强度、高度和截止角，并评估任务失败情况与轨迹偏差。
- 研究在 LIBERO-Spatial、LIBERO-Object 和 LIBERO-10 上训练 SmolVLA 模型，然后在正常、随机和优化照明条件下测试基线策略与采用朴素增强的策略。
- 研究通过灰度诊断测试朴素增强是否导致模型不再依赖颜色线索。
- ChromaGuard 执行对抗性照明增强，同时将色相扰动固定为零，在改变饱和度、亮度、对比度和锐度的同时保留色度。
- 实验在配备 6-DoF SO-101 机械臂的真实环境中使用 SmolVLA 和 pi_0.5，测试颜色不变任务与依赖颜色的任务。

## 结果
- 在仿真中，经过优化的 FLARE 攻击将三个 LIBERO 套件上的基线成功率全部降至 0.0%，并造成最高 115.5 cm 的轨迹误差；基线在正常照明下的成功率分别为 LIBERO-Spatial 83.0%、LIBERO-Object 89.4% 和 LIBERO-10 58.4%。
- 朴素增强在仿真中表现出较高的鲁棒性：三个套件在优化攻击下的成功率分别为 78.8%、93.2% 和 47.2%。但其灰度成功率仍然很高，例如在 LIBERO-Object 上灰度输入为 90.5%，RGB 输入为 89.8%，这表明它在很大程度上丢弃了颜色线索。
- 在真实的依赖颜色任务中，朴素增强使 SmolVLA 在正常照明下的成功率降至 47.5%，而基线为 77.5%。
- 在依赖颜色的任务中，ChromaGuard 使 SmolVLA 在正常照明和攻击照明下的成功率分别达到 97.5% 和 92.5%；在颜色不变任务中，两个条件下的成功率均为 70.0%。
- 对于 pi_0.5，ChromaGuard 在依赖颜色的任务中取得了 55.0% 的正常照明成功率和 70.0% 的攻击照明成功率；论文认为，其在正常照明下颜色辨别能力较低，部分原因在于预训练模型，其中颜色抓取错误占失败案例的 66.7%。
- 评估仅涵盖固定式聚光灯和有限的物理任务；作者没有测试随时间变化的照明或自适应闭环攻击。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.14698v1](https://arxiv.org/abs/2607.14698v1)
