---
source: arxiv
url: https://arxiv.org/abs/2605.07474v1
published_at: '2026-05-08T09:20:56'
authors:
- Yuhao Zhou
- Yunpeng Zhu
- Yang Zhou
- Jindi Lyu
- Jian Lan
- Zhangyuan Wang
- Dan Si
- Thomas Seidl
- Qing Ye
- Jiancheng Lyu
topics:
- vision-language-action
- federated-learning
- robot-data-scaling
- language-annotation
- non-iid-robotics
- manipulation-benchmarks
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# ForgeVLA: Federated Vision-Language-Action Learning without Language Annotations

## Summary
## 摘要
ForgeVLA 使用分布式视觉-动作日志训练 VLA 机器人策略，不需要人工语言标注，也不需要汇集原始数据。它加入了端侧指令分类、对比规划损失和服务器端自适应聚合，用于在非独立同分布机器人数据下改进联邦 VLA 训练。

## 问题
- VLA 模型需要视觉-语言-动作三元组，但许多已部署机器人只记录同步图像和动作。
- 机器人日志通常不能集中存放，因为它们来自工厂、医院、仓库或其他私有场景。
- 联邦 VLA 训练会受到客户端异质性的影响；论文指出，视觉-语言特征坍塌是一种失败模式，其中任务嵌入会失去区分度。

## 方法
- 服务器在一个小型公开 VLA 数据集上微调预训练 VLM，构建具身指令分类器。
- 每个客户端在本地用该分类器处理自己的视觉-动作对，并将每个样本映射到预定义指令集，在设备端生成伪 VLA 三元组。
- 客户端训练基于 InternVLA-M1 的 VLA 模型，使用常规动作损失，并加入对比规划损失，使每个样本靠近其预测指令对应的全局任务嵌入。
- 服务器保存并更新一个由客户端任务嵌入组成的全局任务表示库。
- 服务器用自适应目标聚合客户端模型更新，在保持每个客户端更新方向的同时，接近加权平均。

## 结果
- 在 LIBERO-Goal 上，ForgeVLA 达到 55.2% 成功率和 100% Pass@50；相比之下，FedAvg 为 28.8% 成功率和 80% Pass@50；集中式上界为 75.8% 成功率。
- 在 LIBERO-Object 上，ForgeVLA 达到 98.6% 成功率和 100% Pass@50；相比之下，FedAvg 为 97.6% 成功率，集中式模型为 98.8%。
- 在 LIBERO-Spatial 上，ForgeVLA 达到 72.6% 成功率和 100% Pass@50；相比之下，FedAvg 为 68.6% 成功率和 90% Pass@50；集中式模型达到 85.8%。
- 在 LIBERO-10 上，ForgeVLA 达到 63.6% 成功率和 100% Pass@50；相比之下，FedAvg 为 52.8% 成功率，集中式模型为 79.0%。
- 相对 FedAvg 的报告增益为：LIBERO-Goal +26.4 个百分点，LIBERO-Object +1.0 个百分点，LIBERO-Spatial +4.0 个百分点，LIBERO-10 +10.8 个百分点。
- ForgeVLA 的主要实验使用 3,882.72M 参数的 InternVLA-M1 模型，其中可训练参数为 128.10M；实验设置为 10 个客户端、20 轮通信、每轮 5 个本地 epoch。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07474v1](https://arxiv.org/abs/2605.07474v1)
