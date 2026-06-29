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
DIAL 是一个端到端的视觉-语言-动作模型，通过潜在世界模型把高层意图和低层控制分开。它用 VLM 预测未来的视觉特征作为意图信号，再由策略把这个信号和当前观测转换成机器人动作。

## 问题
- 现有的端到端 VLA 往往直接把视觉-语言特征映射到低层动作，这会让训练不稳定，并损害 VLM 预训练得到的语义特征。
- 分层机器人系统把高层规划和低层控制分开，但接口通常不可微，这会阻止动作反馈改进规划器。
- 以前也加入过世界模型目标，但在很多方法里，预测的未来只是辅助信号，所以策略仍然可以忽略它，转而学捷径。

## 方法
- DIAL 构建了一个两部分策略：**System-2** 是一个预训练 VLM，预测时间跨度为 **H = 16** 的未来观测潜表示；**System-1** 是一个动作策略，使用这个预测未来和当前状态输出一个动作块。
- 关键机制是 **潜在意图瓶颈**：控制器接收的不是文本规划或像素，而是 VLM 在与感知相同的 ViT 特征空间里预测出的未来视觉特征。这个未来特征张量就是模型的意图。
- System-2 在 **Qwen2.5-VL-3B** 这类 VLM 上使用可学习的查询 token，并用 **MSE 世界模型损失** 训练，使其与未来帧 \(o_{t+H}\) 的 ViT 特征匹配。
- System-1 是一个潜在逆动力学策略，包含一个 **4 层自注意力融合模块** 和一个 **16 层 DiT**，通过 **flow matching** 训练，生成接下来 **16 步** 的动作块。
- 训练分两阶段：先是解耦热身阶段，System-2 预测未来潜表示，System-1 在真实未来特征指导下学习控制；然后进行联合端到端训练，同时使用世界模型损失和动作损失，让动作梯度在不完全破坏表示的情况下微调 VLM。

## 结果
- 在 **RoboCasa GR1 Tabletop** 基准上，论文声称相比已有方法达到 **新的最优结果**。
- 主要的数据效率结果是：在仍然优于已有方法的情况下，只需要 **10 倍更少的机器人示范**；摘要中给出的少样本设定是 **2,400 条轨迹**，对比完整数据设定的 **24,000 条轨迹**。
- 仿真评测覆盖 **24 个任务**，每个任务测试 **50 个 episode**，其中包括 **18 个** 拾取放置任务和 **6 个** 具身任务。
- 在跨具身学习中，DIAL 使用 **27,419** 条 EgoDex 人类拾取放置轨迹，并报告在三个 OOD 设定上提升了零样本泛化：未见外观（**18 个任务**）、未见组合（**14 个任务**）和未见物体类型（**32 个任务**）。
- 在 **IRON-R01-1.11** 类人机器人上的真实世界实验中，训练使用每个任务 **120 条机器人轨迹**，再加上一个混合预训练集，包含 **32k** 条机器人轨迹和 **30k** 条 EgoDex 轨迹。论文声称该方法可以稳定执行，并能零样本迁移到新物体和新配置。
- 摘要没有给出确切的成功率、基线差距或逐方法表格，因此最明确的结论是：DIAL 在 RoboCasa 上达到 SOTA、数据效率高出 10 倍，并且在仿真和真实世界测试中都有稳定的零样本迁移。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2603.29844v1](http://arxiv.org/abs/2603.29844v1)
