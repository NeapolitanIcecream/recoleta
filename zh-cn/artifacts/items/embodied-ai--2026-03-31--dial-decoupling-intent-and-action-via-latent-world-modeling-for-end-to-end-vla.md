---
source: arxiv
url: http://arxiv.org/abs/2603.29844v1
published_at: '2026-03-31T15:02:27'
authors:
- Yi Chen
- Yuying Ge
- Hui Zhou
- Mingyu Ding
- Yixiao Ge
- Xihui Liu
topics:
- vision-language-action
- latent-world-model
- robot-foundation-model
- sim2real
- generalist-robot-policy
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# DIAL: Decoupling Intent and Action via Latent World Modeling for End-to-End VLA

## Summary
## 摘要
DIAL 是一种端到端视觉-语言-动作模型，通过潜在世界模型把高层意图和低层控制分开。它用 VLM 预测未来视觉特征作为意图信号，再由策略将这个信号和当前观测转换为机器人动作。

## 问题
- 现有端到端 VLA 往往直接把视觉-语言特征映射到低层动作，这会让训练不稳定，并损害 VLM 预训练得到的语义特征。
- 分层机器人系统会把高层规划和低层控制分开，但它们之间的接口通常不可微，因此动作反馈无法用于改进规划器。
- 以往也引入过世界模型目标，但很多方法里预测的未来只是辅助信号，因此策略仍然可能忽略它并学习捷径。

## 方法
- DIAL 构建了一个双模块策略：**System-2** 是预训练 VLM，用于预测时间跨度 **H = 16** 的未来观测潜在表示；**System-1** 是动作策略，使用这个预测未来和当前状态输出一个动作块。
- 核心机制是一个**潜在意图瓶颈**：VLM 不向控制器传递文本计划或像素，而是在用于感知的同一 ViT 特征空间中预测未来视觉特征。这个未来特征张量就是模型的意图。
- System-2 在 **Qwen2.5-VL-3B** 这类 VLM 之上使用可学习查询 token，并用 **MSE world-model loss** 训练，使其匹配未来帧 \(o_{t+H}\) 的 ViT 特征。
- System-1 是一个潜在逆动力学策略，包含一个**4 层自注意力融合模块**和一个**16 层 DiT**，通过 **flow matching** 训练来生成接下来的 **16-step** 动作块。
- 训练分两个阶段：先进行解耦预热，由 System-2 预测未来潜变量，System-1 在真实未来特征指导下学习控制；然后进行端到端联合训练，同时使用世界模型损失和动作损失，让动作梯度可以在不完全破坏 VLM 表征的情况下调整 VLM。

## 结果
- 在 **RoboCasa GR1 Tabletop** 基准上，论文声称相比现有方法达到**新的最佳结果**。
- 主要的定量效率结论是：使用的机器人示范数据比以往方法少 **10×**，但表现仍然更好；摘录中给出的 few-shot 设置是 **2,400 trajectories**，而全量数据设置是 **24,000 trajectories**。
- 仿真评测覆盖 **24 tasks**，每个任务测试 **50 episodes**，其中包括 **18** 个 pick-and-place 任务和 **6** 个 articulated 任务。
- 在跨具身学习中，DIAL 使用 **27,419** 条 EgoDex 人类 pick-and-place 轨迹，据称提升了三种 OOD 设置下的零样本泛化：未见外观（**18 tasks**）、未见组合（**14 tasks**）和未见物体类型（**32 tasks**）。
- 在 **IRON-R01-1.11** 人形机器人上的真实世界实验中，每个任务训练使用 **120 robot trajectories**，另加一个混合预训练集，其中包含 **32k** 条机器人轨迹和 **30k** 条 EgoDex 轨迹。论文称其能稳定执行，并能零样本迁移到新物体和新配置。
- 这段摘录**没有给出确切成功率、相对基线优势或各方法的表格**，因此最明确的结论是：在 RoboCasa 上达到 SOTA、数据效率提高 **10×**，并且在仿真和真实测试中表现出较强的零样本迁移能力。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29844v1](http://arxiv.org/abs/2603.29844v1)
