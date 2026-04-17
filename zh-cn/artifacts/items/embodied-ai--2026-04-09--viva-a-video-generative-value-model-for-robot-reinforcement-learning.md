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
ViVa 将一个预训练视频扩散模型用作机器人强化学习中的价值函数。它根据当前图像和本体感觉预测未来机器人状态以及当前任务价值。论文称，在 RECAP 流水线中，ViVa 能提供更好的价值信号，并提升真实世界中的盒子组装表现。

## 问题
- 现有基于视觉语言模型的机器人价值模型主要读取静态帧，因此会遗漏时间动态，而这些动态对部分可观测、反馈延迟的长时程操作任务很重要。
- 价值估计较弱会损害强化学习效果，因为 RECAP 依赖价值预测来进行优势估计和策略改进。
- 论文希望实现一种价值估计方法，能够跟踪真实任务进展、捕捉执行错误，并迁移到新物体上。

## 方法
- ViVa 没有训练一个标准的判别式视觉语言价值模型，而是将一个预训练视频生成器 Wan2.2 改造为价值估计模型。
- 输入：当前多视角 RGB 观测和当前机器人本体感觉。输出：时间范围 \(K=50\) 处的未来本体感觉状态，以及当前状态的一个标量价值。
- 模型将图像、本体感觉和价值转换为潜在帧，然后用扩散去噪进行预测，其中干净的当前观测作为条件，带噪声的未来本体感觉/价值帧作为目标。
- 价值监督使用归一化回报目标，该目标由轨迹进展以及最终成功或失败导出。成功轨迹对应的价值落在 \([0,1)\)；失败轨迹平移到 \([1,2)\)，因此在同一阶段，成功与失败之间保持 1.0 的固定间隔。
- ViVa 替换了 RECAP 中基于 VLM 的价值函数，其余流水线保持不变，因此可以直接比较不同价值模型设计。

## 结果
- 摘录中没有给出完整的定量基准表，因此这里无法提供确切的成功率提升数值。
- 论文称，当 ViVa 集成到 RECAP 中时，与此前的价值模型选择相比，它在真实世界盒子组装任务上的成功率和吞吐量都有“大幅提升”。
- 3 个真实世界任务上的定性结果——衬衫折叠、盒子包装/组装、厕纸整理——显示，ViVa 比基于 VLM 的价值模型更平滑地跟踪任务进展。
- 在盒子组装中，ViVa 在 2 个标出的失败事件处出现明显的价值下降，而基于 VLM 的价值基本保持单调，未能捕捉这些错误。
- 在厕纸整理中，ViVa 在 2 个标出的关键节点处显示出清晰的价值上升：卷筒对齐和贴标签；基于 VLM 的价值基本保持平坦。
- 具体实现细节包括：3 个任务、单轮训练、batch size 192、预测范围 \(K=50\)、损失权重 \(\lambda_{prop}=1.0\) 和 \(\lambda_{val}=0.5\)、推理时 1 步去噪，以及使用 8 张 NVIDIA A800 GPU 进行训练。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.08168v1](http://arxiv.org/abs/2604.08168v1)
