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
## 总结
GuidedVLA 通过把动作解码器的注意力头分别分配给对象定位、技能阶段识别和基于深度的几何信息，提升了 VLA 机器人策略表现。

## 问题
- 端到端 VLA 训练会让动作 token 关注背景纹理、相机伪影或其他虚假线索，从而降低域外成功率。
- 论文针对的是动作解码器，因为任务相关因素通常在这里被隐式学习，而且不同注意力头、不同场景之间会有变化。
- 这对操作任务很重要，因为目标对象、子技能或三维位姿只要有小错误，任务就可能失败。

## 方法
- GuidedVLA 在预训练 VLA 策略上加入了一个类似 ControlNet 的残差注意力分支，并用零初始化融合层，让训练开始时保留基础策略的行为。
- 对象头使用来自 Qwen3-VL 提示、SAM2 传播和人工核验的真实对象掩码来训练，让注意力集中在这些区域上。
- 技能头使用 KL 损失训练，在未来时间范围内预测任务阶段的软标签，例如抓取和放置。
- 深度头只关注来自冻结深度编码器的 key 和 value，因此特定头可以接收三维结构信息，而不需要深度标注。
- 总损失把基础 flow-matching 动作损失与对象和技能辅助损失结合起来；深度引导是结构性的，不依赖额外损失。

## 结果
- 在 LIBERO-Plus 上，启用全部头的 GuidedVLA 平均成功率达到 75.4%，高于 π0 基座模型的 68.2%、DreamVLA 的 69.9%、OpenVLA-OFT 的 69.6% 和 RIPT-VLA 的 68.4%。
- LIBERO-Plus 的消融结果显示，每个因素都有帮助：对象头 73.4%，技能头 72.5%，深度头 71.7%，全部头 75.4%。
- 在 LIBERO-Plus 扰动测试中，完整模型相对 π0 在各项设置上都有提升：相机 73.7% 对 62.3%，机器人状态 51.4% 对 39.8%，光照 94.6% 对 86.0%，背景 89.0% 对 82.8%，布局 79.9% 对 69.6%，长时程任务 66.2% 对 60.1%。
- 在 RoboTwin 2.0 上，完整模型在 8 个操作任务、随机未见设置下的平均成功率为 90.63%；节选没有提供该基准上 π0 的平均值。
- 在 6 个真实世界任务、每个任务 20 次试验的测试中，GuidedVLA 相比基础策略的平均成功率更高：域内 75.8% 对 55.8%，场景 67.5% 对 44.2%，光照 79.2% 对 57.5%。
- 标注流程显示，92% 的 episode 不需要人工修正，50 个 episode 大约 4 分钟就能标注完，而人工标注大约需要 43.5 分钟。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12369v1](https://arxiv.org/abs/2605.12369v1)
