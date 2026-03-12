---
source: arxiv
url: http://arxiv.org/abs/2603.05147v1
published_at: '2026-03-05T13:14:41'
authors:
- Riccardo Andrea Izzo
- Gianluca Bardaro
- Matteo Matteucci
topics:
- vision-language-action
- adaptive-inference
- ood-detection
- robot-safety
- uncertainty-estimation
relevance_score: 0.62
run_id: materialize-outputs
---

# Act, Think or Abstain: Complexity-Aware Adaptive Inference for Vision-Language-Action Models

## Summary
本文提出一种面向视觉-语言-动作模型（VLA）的复杂度感知自适应推理框架，根据当前状态自动选择直接执行、额外思考或拒绝执行。核心价值是在提升泛化与安全性的同时，避免对简单任务一律使用高开销推理。

## Problem
- 现有VLA常通过链式推理等机制提升泛化，但这会**无差别增加**计算成本和推理延迟。
- 这些方法通常缺乏对任务复杂度与不确定性的显式判断，容易在分布外任务上**过度自信并导致灾难性失败**。
- 机器人部署需要同时兼顾**实时性、泛化性与安全性**，而固定推理策略难以满足这三者。

## Approach
- 将VLA的预训练视觉-语言骨干从“被动特征提取器”改造成“复杂度检测器”：从视觉、文本和融合表征中提取嵌入。
- 先用PCA把特征降到64维，再用**GMM**（全局分布）和**1-NN/kNN**（局部异常）对样本新颖度/OOD程度打分。
- 把这些分数组成一个小向量，输入轻量MLP，输出三类路由决策：**Act**（已知任务直接执行）、**Think**（模糊任务触发额外推理）、**Abstain**（明显OOD时停止执行）。
- Think分支只在每个episode首时刻触发一次，通过补充场景线索和子目标到prompt中来增强动作生成。
- 训练时将LIBERO视为ID、LIBERO-PRO视为部分OOD，并引入来自其他桌面操作数据的OOD样本；还使用mixup合成中间态特征来学习“Think”边界。

## Results
- 在**LIBERO / LIBERO-PRO**与真实机器人实验中，作者声称方法有效；摘要中给出：**vision-only配置仅用5%训练数据即可达到80% F1-score**，作为可靠高效的任务复杂度检测器。
- 全量数据评估下，**MLP + GMM (vision-only)** 达到 **Macro F1 = 84.34%**，为最佳配置；相比之下 **MLP + kNN (vision)** 为 **73.90%**。
- 直接在原始特征上训练的**baseline MLP**只有 **63.81% Macro F1**；且**86% 的“Think”样本被误判为“Act”**，说明其对模糊场景过度自信。
- 多模态并非总是更好：**MLP + GMM(all) + kNN ensemble** 为 **71.41% F1**，**text-only** 仅 **54.76% F1**，表明文本/融合特征会削弱复杂度判别。
- 数据效率方面，作者在 **{0.1%, 1%, 5%, 10%, 25%}** 训练比例上测试，称**5%数据（少于约1,000样本量级到接近收敛）**已接近峰值表现；baseline则在各数据规模下都停留在约 **F1≈0.60**。
- GMM组件数消融显示最佳为 **k=3**；文中还声称vision-only GMM混淆矩阵中对**fully OOD到“Act”路径的泄漏为0**，强化了安全性主张。

## Link
- [http://arxiv.org/abs/2603.05147v1](http://arxiv.org/abs/2603.05147v1)
