---
source: arxiv
url: https://arxiv.org/abs/2606.17598v1
published_at: '2026-06-16T07:04:13'
authors:
- Xingyuming Liu
- Ruichun Ma
- Heyu Guo
- Qixiu Li
- Qingwen Yang
- Lin Luo
- Shiqi Jiang
- Chenren Xu
- Jiaolong Yang
- Baining Guo
topics:
- vision-language-action
- multimodal-sensing
- dexterous-manipulation
- robot-data-scaling
- sensor-selection
- simulated-sensor-data
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# MuseVLA: An Adaptive Multimodal Sensing Vision-Language-Action Model for Robotic Manipulation

## Summary
## 摘要
MuseVLA 是一个用于灵巧操作的 VLA 模型，可根据任务和场景选择热成像、音频、mmWave 或 RGB 传感。它把选中的传感器读数转换为类似 RGB 的 grounded sensor image，使一个视觉编码器能够将其与语言和机器人状态合并处理。

## 问题
- 只使用 RGB 的 VLA 策略会漏掉温度、声源位置、雷达响应等物理线索，而这些线索是拿起热饮或寻找藏在盒子里的物体等任务所需的。
- 多传感器机器人数据成本高：论文收集了 720 个真实遥操作 episode，而其合成流水线从仅 RGB 的数据集中增加了 9.6K 个 episode 和 1.05M 帧。
- 固定传感器融合会处理可能无关的传感器，并把策略绑定到固定的传感器集合。

## 方法
- 模型先读取指令和 RGB 图像，然后生成一个传感器 token，例如 <Thermal>、<Acoustic>、<mmWave> 或 <None>，以及一个目标描述，例如 the mugs。
- 分割模型 SAM3 会为描述的物体生成掩码，选中的传感器热力图会叠加到该掩码上，形成 grounded sensor image。
- grounded sensor image 会被送回基于 PaliGemma-2/VITRA 的 VLM，并由 diffusion transformer action expert 预测动作片段。
- 训练结合了用于传感器和目标生成的交叉熵损失，以及 diffusion MSE 动作损失；动作损失权重为 1e-2。
- 合成流水线向 RGB 机器人 episode 中注入传感器相关词，使用 GPT-5.2 生成目标描述，分割目标，并叠加颜色编码掩码来模拟传感器线索。

## 结果
- 在使用热成像、声学和 mmWave 传感的真实灵巧手任务中，经过合成预训练的 MuseVLA 在已见任务上的平均成功率达到 80.6%：热成像 87.5%，声学 70.8%，mmWave 83.3%。
- 在不使用合成预训练的直接任务对比表中，MuseVLA 的平均成功率达到 76.4%，相比之下 π0-RGB 为 20.8%，π0.5-RGB 为 19.4%，π0-Raw 为 27.8%，MuseVLA-Raw 为 33.3%。
- 表 1 中，MuseVLA 报告的传感阶段成功率为 95.8%，操作阶段成功率为 77.8%，任务得分为 0.868。
- 合成预训练将未见任务的平均成功率提升到 66.7%，而未预训练的 MuseVLA 为 27.1%，MuseVLA-Raw 为 25.0%。
- 经过预训练后，自适应传感器选择在未见任务上的传感器 token 准确率达到 100%，目标描述准确率达到 82.0%；PaliGemma-2 单独在相同指标上得分为 0% 和 9.5%。
- 真实训练集包含 720 个演示，覆盖 10 条子任务指令、7 个物体和 3 种传感模态；合成集包含 9.6K 个 episode、1.05M 帧和超过 1000 个物体。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.17598v1](https://arxiv.org/abs/2606.17598v1)
