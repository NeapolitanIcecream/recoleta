---
source: arxiv
url: http://arxiv.org/abs/2603.05117v2
published_at: '2026-03-05T12:42:53'
authors:
- Youqiang Gui
- Yuxuan Zhou
- Shen Cheng
- Xinyang Yuan
- Haoqiang Fan
- Peng Cheng
- Shuaicheng Liu
topics:
- robot-manipulation
- diffusion-policy
- long-horizon
- temporal-attention
- imitation-learning
relevance_score: 0.89
run_id: materialize-outputs
---

# SeedPolicy: Horizon Scaling via Self-Evolving Diffusion Policy for Robot Manipulation

## Summary
SeedPolicy解决了扩散策略在机器人操作中“看得越久反而越差”的长时序建模瓶颈。它通过一个可递归更新、带门控的时序状态模块，让更长观察窗口真正转化为更高成功率，并以远小于大规模VLA模型的参数量取得强结果。

## Problem
- 现有Diffusion Policy虽然能建模多模态专家行为，但随着**observation horizon**增大，性能反而下降，限制了长时程操作能力。
- 直接把多帧图像堆叠起来，难以捕捉复杂时间依赖；在长任务中，关键历史信息容易丢失，而噪声帧会干扰决策。
- 标准时序注意力虽可改善建模，但计算随时长二次增长，不利于实时机器人控制和边缘部署。

## Approach
- 提出**SEGA (Self-Evolving Gated Attention)**：维护一个固定大小、随时间演化的潜在状态，把长历史压缩进这个状态里，避免直接处理越来越长的原始帧序列。
- SEGA包含两条流：一条用当前观测更新历史状态；另一条用历史状态反向增强当前观测，再交给扩散动作专家预测动作序列。
- 核心门控**SEG**直接利用交叉注意力分数作为“相关性信号”，决定本次应保留多少新信息、保留多少旧状态；简单说，就是“只在当前帧真的有用时才更新记忆”。
- 将SEGA集成到Diffusion Policy中得到**SeedPolicy**，实现近似递归式的长时程建模，以适中开销扩展时域长度。

## Results
- 在**RoboTwin 2.0**的**50个操作任务**上，作者报告SeedPolicy达到IL方法SOTA；按CNN与Transformer骨干平均，较原始DP在**clean**环境下提升**36.8%**，在**randomized hard**环境下提升**169%**（相对提升）。
- 表1中，**Transformer骨干**下：DP从**33.10%**（Easy）/ **1.44%**（Hard）提升到SeedPolicy的**40.08%** / **4.28%**，对应绝对提升**6.98%**与**2.84%**。
- 表1中，**CNN骨干**下：DP从**28.04%**（Easy）/ **0.64%**（Hard）提升到SeedPolicy的**42.76%** / **1.54%**，对应绝对提升**14.72%**与**0.90%**。
- 与**RDT (1.2B参数)**相比，SeedPolicy在参数量上小得多：**33.36M**（Transformer）或**147.26M**（CNN）；其中Transformer版约比RDT小**36×**，而在Easy设置下CNN版成功率**42.76%**高于RDT的**34.50%**。
- 作者称SeedPolicy在**45/50**个任务（Transformer）和**44/50**个任务（CNN）上优于或持平基线DP。
- 按任务长度分组，SeedPolicy对长任务优势更大：Transformer在短/中/长任务上分别领先**+2.9% / +6.4% / +16.0%**，CNN分别领先**+13.6% / +12.9% / +21.9%**，支持其“horizon scaling”主张。

## Link
- [http://arxiv.org/abs/2603.05117v2](http://arxiv.org/abs/2603.05117v2)
