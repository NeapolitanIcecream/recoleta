---
source: arxiv
url: http://arxiv.org/abs/2604.08168v1
published_at: '2026-04-09T12:28:14'
authors:
- Jindi Lv
- Hao Li
- Jie Li
- Yifei Nie
- Fankun Kong
- Yang Wang
- Xiaofeng Wang
- Zheng Zhu
- Chaojun Ni
- Qiuping Deng
- Hengtao Li
- Jiancheng Lv
- Guan Huang
topics:
- robot-reinforcement-learning
- video-generation
- value-function
- vision-language-action
- real-world-manipulation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# ViVa: A Video-Generative Value Model for Robot Reinforcement Learning

## Summary
## 摘要
ViVa 把一个预训练的视频扩散模型当作机器人强化学习中的价值函数。它从当前图像和本体感觉预测未来机器人状态和当前任务价值，论文声称它能提供更好的价值信号，并在 RECAP 流水线中提升真实世界的箱体装配表现。

## 问题
- 基于视觉-语言模型构建的现有机器人价值模型主要读取静态帧，因此会错过对长时程操作很重要的时间动态，而这类任务又常常存在部分可观测和反馈延迟。
- 价值估计不准会拖累强化学习，因为 RECAP 依赖价值预测来做优势估计和策略改进。
- 这篇论文要做的是让价值估计能跟踪真实任务进度、识别执行错误，并迁移到新物体上。

## 方法
- ViVa 不训练标准的判别式视觉-语言价值模型，而是把预训练的视频生成器 Wan2.2 改作价值估计器。
- 输入是当前多视角 RGB 观测和当前机器人本体感觉。输出是 \(K=50\) 步之后的未来本体感觉状态，以及当前状态的一个标量价值。
- 模型先把图像、本体感觉和价值转成潜在帧，再用扩散去噪做预测，并以干净的当前观测作为条件，以带噪的未来本体感觉和价值帧作为目标。
- 价值监督使用一个归一化回报目标，它由 episode 进度以及最终成功或失败构成。成功 episode 的值映射到 \([0,1)\)，失败 episode 平移到 \([1,2)\)，这样同一阶段的成功和失败之间保持 1.0 的固定间隔。
- ViVa 用来替换 RECAP 里基于 VLM 的价值函数，其余流水线保持不变，这样可以直接比较不同价值模型设计。

## 结果
- 这段摘要没有给出完整的定量基准表，所以这里看不到准确的成功率提升数值。
- 论文声称，把 ViVa 接入 RECAP 后，在真实世界箱体装配上，成功率和吞吐量都出现了“显著提升”，优于之前的价值模型选择。
- 在 3 个真实任务上的定性结果显示，ViVa 对任务进度的跟踪比基于 VLM 的价值模型更平滑。这 3 个任务是衬衫折叠、箱体包装/装配、以及卫生纸整理。
- 在箱体装配中，ViVa 在 2 个标出的失败事件处出现明显的价值下降，而基于 VLM 的价值基本保持单调，漏掉了这些错误。
- 在卫生纸整理中，ViVa 在 2 个标出的里程碑处出现清晰的价值上升：卷筒对齐和标签贴附；基于 VLM 的价值基本保持平坦。
- 具体实现信息包括：3 个任务、单轮训练、batch size 192、预测时域 \(K=50\)、损失权重 \(\lambda_{prop}=1.0\) 和 \(\lambda_{val}=0.5\)、推理时 1 步去噪，以及在 8 张 NVIDIA A800 GPU 上训练。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.08168v1](http://arxiv.org/abs/2604.08168v1)
