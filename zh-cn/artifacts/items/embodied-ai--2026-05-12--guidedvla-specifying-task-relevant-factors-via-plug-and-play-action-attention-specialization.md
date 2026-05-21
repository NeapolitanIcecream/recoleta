---
source: arxiv
url: https://arxiv.org/abs/2605.12369v1
published_at: '2026-05-12T16:38:40'
authors:
- Xiaosong Jia
- Bowen Yang
- Zuhao Ge
- Xian Nie
- Yuchen Zhou
- Cunxin Fan
- Yufeng Li
- Yilin Chai
- Chao Jing
- Zijian Liang
- Qingwen Bu
- Haidong Cao
- Chao Wu
- Qifeng Li
- Zhenjie Yang
- Chenhe Zhang
- Hongyang Li
- Zuxuan Wu
- Junchi Yan
- Yu-Gang Jiang
topics:
- vision-language-action
- robot-foundation-models
- attention-specialization
- robot-manipulation
- robot-generalization
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# GuidedVLA: Specifying Task-Relevant Factors via Plug-and-Play Action Attention Specialization

## Summary
## 摘要
GuidedVLA 通过把动作解码器注意力头分配给对象定位、技能阶段识别和基于深度的几何信息，提升了 VLA 机器人策略。

## 问题
- 端到端 VLA 训练可能让动作 token 关注背景纹理、相机伪影或其他伪相关线索，从而降低分布外成功率。
- 论文针对动作解码器；任务因素通常在这里被隐式学习，并且可能随注意力头和场景变化。
- 这对操作任务很重要，因为目标对象、子技能或 3D 位姿上的小误差都可能导致任务失败。

## 方法
- GuidedVLA 在预训练 VLA 策略上加入一个 ControlNet 风格的残差注意力分支，并使用零初始化融合，使基础策略行为在训练开始时保持不变。
- 对象头经过训练，将注意力质量放在由 Qwen3-VL 提示、SAM2 传播和人工核验得到的真实对象掩码上。
- 技能头使用 KL 损失进行训练，在未来时域内预测任务阶段的软标签，例如 pick 和 place。
- 深度头只关注来自冻结深度编码器的键和值，因此特定注意力头可以在没有深度标签的情况下接收 3D 结构信息。
- 总损失结合了基础流匹配动作损失与对象和技能辅助损失；深度引导通过结构实现，而非基于损失。

## 结果
- 在 LIBERO-Plus 上，使用全部注意力头的 GuidedVLA 达到 75.4% 的平均成功率，高于其 π0 基础模型的 68.2%、DreamVLA 的 69.9%、OpenVLA-OFT 的 69.6% 和 RIPT-VLA 的 68.4%。
- LIBERO-Plus 消融实验显示，每个因素都有帮助：对象头 73.4%，技能头 72.5%，深度头 71.7%，全部注意力头 75.4%。
- 在 LIBERO-Plus 扰动设置下，完整模型相对 π0 有提升：相机 73.7% 对 62.3%，机器人状态 51.4% 对 39.8%，光照 94.6% 对 86.0%，背景 89.0% 对 82.8%，布局 79.9% 对 69.6%，长时域任务 66.2% 对 60.1%。
- 在 RoboTwin 2.0 上，完整模型在随机化未见设置下的 8 个操作任务中报告了 90.63% 的平均成功率；摘录未提供该基准上 π0 的平均值。
- 在 6 个真实世界任务中，每个任务进行 20 次试验，GuidedVLA 相比基础策略提高了平均成功率：分布内 75.8% 对 55.8%，场景 67.5% 对 44.2%，光照 79.2% 对 57.5%。
- 标注流程报告称，92% 的 episode 不需要人工修正，50 个 episode 的标注约需 4 分钟，而纯人工标注约需 43.5 分钟。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12369v1](https://arxiv.org/abs/2605.12369v1)
