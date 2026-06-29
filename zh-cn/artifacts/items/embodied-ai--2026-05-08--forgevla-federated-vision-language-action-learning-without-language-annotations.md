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
ForgeVLA 从分布式视觉-动作日志训练 VLA 机器人策略，不需要人工语言标注，也不需要把原始数据集中到一起。它加入了设备端指令分类、对比式规划损失和服务器端自适应聚合，用来提升非独立同分布机器人数据下的联邦 VLA 训练效果。

## 问题
- VLA 模型需要视觉-语言-动作三元组，但很多已部署机器人只记录同步图像和动作。
- 机器人日志往往不能集中，因为它们来自工厂、医院、仓库或其他私密场景。
- 联邦 VLA 训练在客户端异质性下表现较差；论文把视觉-语言特征坍塌识别为一种失败模式，在这种情况下任务嵌入会失去区分度。

## 方法
- 服务器先用一个小型公开 VLA 数据集微调预训练 VLM，构建一个具身指令分类器。
- 每个客户端在本地对自己的视觉-动作对运行这个分类器，并把每个样本映射到预定义指令集合，在设备端生成伪 VLA 三元组。
- 客户端训练一个基于 InternVLA-M1 的 VLA 模型，使用常规动作损失和对比式规划损失；后者把每个样本拉向其预测指令对应的全局任务嵌入。
- 服务器维护并更新一个全局任务表示库，来源于客户端任务嵌入。
- 服务器用一个自适应目标聚合客户端模型更新，在保持每个客户端更新方向的同时，尽量接近加权平均。

## 结果
- 在 LIBERO-Goal 上，ForgeVLA 的成功率为 55.2%，Pass@50 为 100%；FedAvg 的成功率为 28.8%，Pass@50 为 80%；集中式上限为 75.8%。
- 在 LIBERO-Object 上，ForgeVLA 的成功率为 98.6%，Pass@50 为 100%；FedAvg 的成功率为 97.6%；集中式模型为 98.8%。
- 在 LIBERO-Spatial 上，ForgeVLA 的成功率为 72.6%，Pass@50 为 100%；FedAvg 的成功率为 68.6%，Pass@50 为 90%；集中式模型为 85.8%。
- 在 LIBERO-10 上，ForgeVLA 的成功率为 63.6%，Pass@50 为 100%；FedAvg 的成功率为 52.8%；集中式模型为 79.0%。
- 报告中相对 FedAvg 的提升分别为：LIBERO-Goal 提升 26.4 个百分点，LIBERO-Object 提升 1.0 个百分点，LIBERO-Spatial 提升 4.0 个百分点，LIBERO-10 提升 10.8 个百分点。
- 主要实验使用了一个 3,882.72M 参数的 InternVLA-M1 模型，其中 128.10M 参数可训练；设置为 10 个客户端、20 轮通信、每轮 5 个本地 epoch。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.07474v1](https://arxiv.org/abs/2605.07474v1)
