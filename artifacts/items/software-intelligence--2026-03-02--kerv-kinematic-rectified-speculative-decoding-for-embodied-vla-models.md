---
source: arxiv
url: http://arxiv.org/abs/2603.01581v1
published_at: '2026-03-02T08:12:03'
authors:
- Zihao Zheng
- Zhihao Mao
- Maoliang Li
- Jiayu Chen
- Xinhao Sun
- Zhaobo Zhang
- Donggang Cao
- Hong Mei
- Xiang Chen
topics:
- vision-language-action
- speculative-decoding
- robot-kinematics
- embodied-ai
- kalman-filter
relevance_score: 0.72
run_id: materialize-outputs
---

# KERV: Kinematic-Rectified Speculative Decoding for Embodied VLA Models

## Summary
KERV提出一种把机器人运动学引入VLA推理解码的加速框架，用来解决具身VLA模型在Speculative Decoding下速度不够快且阈值难调的问题。核心思想是用轻量级运动学预测替代昂贵的重推理，并用运动学信号动态调整接受阈值，在几乎不损失成功率的情况下显著提速。

## Problem
- 具身VLA模型把动作表示成token逐步生成，但推理慢；直接套用Speculative Decoding后，遇到token错误通常要重推理，反而带来较高计算开销。
- 现有方法如SpecVLA依赖固定的宽松接受阈值，难以在不同任务/环境中同时兼顾速度与成功率；错误还会随时间累积。
- 论文指出token域的“错误大小”不一定等同于机器人运动学上的“动作可接受性”，因此只在token域调参是不够的，这对真实机器人控制很重要。

## Approach
- 提出KERV（Kinematic-Rectified Speculative Decoding）：把token域VLA解码和运动学域预测结合起来。
- 当SD草稿token在某位置首次出错时，不再对该动作片段剩余自由度做昂贵重推理，而是用基于运动学的Kalman Filter根据历史动作缓存直接预测并补全后续动作；文中设置Prediction Length=1、Action Context=10。
- 构建token到机器人动作的映射，并按7 DoF缓存历史动作（X/Y/Z、姿态角、夹爪），让KF在短时上下文里做低成本补偿。
- 设计基于运动学变异度`K_var`的动态阈值调整机制：不是使用固定接受阈值，而是根据当前动作误差映射到运动学后的变化，自适应更新接受阈值；多数任务预设`r_max=15`,`r_min=5`。
- 系统实现上采用CPU-GPU协同：草稿模型与验证模型放在GPU上，KF补偿和阈值调整放在CPU上，以利用其低FLOPs但逻辑控制较多的特点。

## Results
- 在LIBERO四个任务套件（Goal/Object/Spatial/Long）上测试，每任务50次试验；验证模型为finetuned OpenVLA，草稿模型为单层LLaMA block。
- 相比naive VLA+SD，KERV达到**1.48×-1.57×**加速，并声称**无成功率损失或几乎无损失**；摘要中给出的总体结论是**27%-37% acceleration with nearly no Success Rate loss**。
- 相比SpecVLA，论文称KERV实现**27%-37%**额外加速；文中还提到仅在两个环境上出现**1.5%**和**0.4%**的成功率下降。
- Goal环境：naive VLA+SD为**76.2% SR, 1.00×, 159.2 steps**；SpecVLA最佳速度约**1.23×**（`r=15`，但SR降到**71.0%**）；KERV为**75.6% SR, 1.54×, 153.5 steps**。
- Object环境：naive为**68.6% SR, 1.00×, 195.9 steps**；SpecVLA最高约**1.10×**；KERV达到**72.3% SR, 1.49×, 186.8 steps**，同时成功率还高于naive。
- 论文还给出naive集成失败原因的量化证据：在Goal/Object/Spatial/Long上，naive VLA+SD速度仅为**0.86×/0.96×/0.98×/0.91×**（相对AR），AFEP为**2.04/1.75/1.59/1.67**，说明频繁早期错误导致重推理抵消了SD收益。

## Link
- [http://arxiv.org/abs/2603.01581v1](http://arxiv.org/abs/2603.01581v1)
