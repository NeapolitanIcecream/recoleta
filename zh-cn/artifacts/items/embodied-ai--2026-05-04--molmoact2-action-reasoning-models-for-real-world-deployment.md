---
source: arxiv
url: https://arxiv.org/abs/2605.02881v2
published_at: '2026-05-04T17:51:21'
authors:
- Haoquan Fang
- Jiafei Duan
- Donovan Clay
- Sam Wang
- Shuo Liu
- Weikai Huang
- Xiang Fan
- Wei-Chuan Tsai
- Shirui Chen
- Yi Ru Wang
- Shanli Xing
- Jaemin Cho
- Jae Sung Park
- Ainaz Eftekhar
- Peter Sushko
- Karen Farley
- Angad Wadhwa
- Cole Harrison
- Winson Han
- Ying-Chun Lee
- Eli VanderBilt
- Rose Hendrix
- Suveen Ellawela
- Lucas Ngoo
- Joyce Chai
- Zhongzheng Ren
- Ali Farhadi
- Dieter Fox
- Ranjay Krishna
topics:
- vision-language-action
- robot-foundation-model
- embodied-reasoning
- robot-data-scaling
- action-tokenization
- bimanual-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# MolmoAct2: Action Reasoning Models for Real-world Deployment

## Summary
## 摘要
MolmoAct2 是一个面向真实机器人部署的开源视觉-语言-动作模型，发布了权重、代码和训练数据。它结合了具身推理 VLM、新的机器人数据集、动作分词器、连续动作专家，以及更快的场景变化推理。

## 问题
- 现有的 VLA 机器人策略难以部署，因为表现强的模型往往是闭源的，开源模型可能依赖昂贵硬件，而推理密集型策略对实时机器人控制来说又太慢。
- 经过微调的机器人策略在真实任务上的成功率仍然不稳定，尤其是在不同机器人本体和真实世界场景之间。
- 这很重要，因为研究人员和机器人开发者需要可复现、能在可负担平台上运行、并能适应本地数据的模型。

## 方法
- MolmoAct2 以 Molmo2-ER 为起点。Molmo2-ER 是一个 4B 的 VLM，在 330 万样本的具身语料上训练，覆盖空间推理和具身推理，然后又用通用多模态数据做了继续训练。
- 作者发布了三类主要机器人数据源：720 小时的双臂 YAM 数据、过滤后的 SO-100/101 社区数据，以及过滤后的 DROID Franka 子集。
- MolmoAct2-FAST Tokenizer 把连续的机器人轨迹转换成离散动作 token，让 VLM 可以用下一个 token 预测来学习动作。
- 后训练阶段加入了基于 flow matching 的连续动作专家。每一层专家都以上一层对应的 VLM 层的 key 和 value 作为条件，把 VLM 的对齐能力接到平滑的机器人动作上。
- MolmoAct2-Think 通过只对相邻时间步之间发生变化的场景区域重新预测深度 token 来加速推理。

## 结果
- Molmo2-ER 在 13 个具身推理基准上的报告平均值达到 63.8%，比 Molmo2 提升了 17 个百分点。
- 文中报告 Molmo2-ER 在 13 个具身推理基准中的 9 个上超过了 GPT-5 和 Gemini Robotics ER-1.5。
- BimanualYAM 数据集包含 34.5k 条示范、超过 720 小时的机器人数据，以及 28 个以上真实世界任务，采集系统成本低于 6,000 美元。
- SO-100/101 数据集由 377 名用户从 1,222 个公开 LeRobot 数据集中整理而来，包含 38,059 个 episode、1,980 万帧，以及约 184 小时的交互数据。
- 经过过滤掉空闲片段并要求有效语言指令后，DROID 子集包含 74,604 个有效成功 episode 和 17,758,044 帧。
- 摘要提到 MolmoAct2 在 7 个仿真和真实世界基准上超过了包括 π0.5 在内的强基线，但提供的文本没有给出任务成功率数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02881v2](https://arxiv.org/abs/2605.02881v2)
