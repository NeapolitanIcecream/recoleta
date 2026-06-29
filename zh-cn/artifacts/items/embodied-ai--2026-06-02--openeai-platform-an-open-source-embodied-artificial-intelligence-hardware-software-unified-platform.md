---
source: arxiv
url: https://arxiv.org/abs/2606.03392v1
published_at: '2026-06-02T09:34:08'
authors:
- Jinyuan Zhang
- Luoyi Fan
- Leiyu Wang
- Yeqiang Wang
- Yicheng Zhu
- Cewu Lu
- Nanyang Ye
topics:
- vision-language-action
- robot-foundation-model
- open-robot-hardware
- robot-data-scaling
- real-world-manipulation
- generalist-robot-policy
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# OpenEAI-Platform: An Open-source Embodied Artificial Intelligence Hardware-Software Unified Platform

## Summary
## 摘要
OpenEAI-Platform 将一款售价 $790 的开源 6+1 DoF 机械臂与 OpenEAI-VLA 配对，后者是一个用公开机器人数据和多模态数据训练的 Qwen3-VL-4B 机器人策略。它面向可复现的真实世界操作场景，这里封闭硬件、私有训练数据和不匹配的数据集格式会限制比较和数据采集。

## 问题
- 真实世界 VLA 工作常依赖私有数据集和不完整的训练代码，其他团队无法复现或扩展结果。
- 商用 6+1 DoF 机械臂价格约为 $1.5k-$40k+，低层控制接口也有限，这会阻碍低成本数据采集和控制器研究。
- 开源机器人数据集使用不同的状态/动作约定，这让跨数据集预训练和迁移更困难。

## 方法
- OpenEAI-Arm 是一款 6+1 DoF 桌面机械臂；其连杆几何由 NSGA-III 在 MDH 参数上优化，目标是操作可达性和耐久效率。
- 控制器结合了动力学前馈 PID、摩擦补偿、滚动动作块插值和受 jerk 约束的 S 曲线时序，把 VLA 动作块转成平滑的关节指令。
- OpenEAI-VLA 使用带可学习查询 token 的 Qwen3-VL-Instruct 4B，把图像、文本和指令特征压缩为固定长度条件输入。
- 一个 18 层、32 个注意力头的 Diffusion Transformer 动作头通过条件流匹配预测连续动作块。
- 训练分两阶段：先在转换后的 Open X-Embodiment 子集上预训练，再用少量 OpenEAI-Arm 演示数据进行微调，并混合 COCO、VQA-v2 和 PixMo-Points。

## 结果
- OpenEAI-Arm 的材料成本是 $0.79k；表中 ARX R5 为 $8.60k，AgileX Piper 为 $2.16k。
- 该机械臂重量为 3.3 kg；ARX R5 为 3.9 kg，Piper 为 4.2 kg。
- 操作可达性为 0.547，几乎与 ARX R5 的 0.546 持平，高于 Piper 的 0.179。
- 耐久效率为 0.567，高于 ARX R5 的 0.529，低于 Piper 的 0.846。
- 评测覆盖 4 个真实世界任务：Clean Table、Make Tea、Fold Towel 和 Fold T-shirt。
- 摘要称 OpenEAI-VLA 在使用有限公开预训练数据时，其成功率可与 π0 相当，但提供的文本没有给出成功率数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03392v1](https://arxiv.org/abs/2606.03392v1)
