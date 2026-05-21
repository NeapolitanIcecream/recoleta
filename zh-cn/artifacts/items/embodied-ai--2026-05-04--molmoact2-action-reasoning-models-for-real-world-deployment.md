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
MolmoAct2 是一个面向真实机器人部署的开放视觉-语言-动作模型，已发布权重、代码和训练数据。它结合了具身推理 VLM、新机器人数据集、动作分词器、连续动作专家，以及更快的场景变化推理。

## 问题
- 当前 VLA 机器人策略难以部署，因为强模型通常不开源，开放模型可能依赖高成本硬件，而推理较重的策略对实时机器人控制来说可能太慢。
- 经过微调的机器人策略在现实任务上仍达不到稳定可靠的成功率，尤其是在不同机体和真实场景之间迁移时。
- 这很重要，因为研究人员和机器人开发者需要可复现的模型，这些模型能在易获得的平台上运行，并适应本地数据。

## 方法
- MolmoAct2 基于 Molmo2-ER，后者是一个 4B VLM，在包含 330 万样本的具身语料上接受空间和具身推理训练，随后用通用多模态数据进行复训。
- 作者发布了三个主要机器人数据来源：720 小时的双臂 YAM 数据、经过筛选的 SO-100/101 社区数据，以及经过筛选的 DROID Franka 子集。
- MolmoAct2-FAST Tokenizer 将连续机器人轨迹转换为离散动作 token，使 VLM 能通过下一个 token 训练来学习动作。
- 后训练加入了一个基于流匹配的连续动作专家。每个专家层都以对应 VLM 层的键和值为条件，将 VLM 的感知 grounding 连接到平滑的机器人动作。
- MolmoAct2-Think 通过只对相邻时间步之间发生变化的场景区域重新预测深度 token 来加快推理。

## 结果
- 报告称，Molmo2-ER 在 13 个具身推理基准上的平均成绩达到 63.8%，比 Molmo2 高 17 个百分点。
- 报告称，Molmo2-ER 在 13 个具身推理基准中的 9 个上超过 GPT-5 和 Gemini Robotics ER-1.5。
- BimanualYAM 数据集包含 3.45 万条演示、超过 720 小时的机器人数据，以及 28 个以上真实世界任务，采集设备成本低于 6,000 美元。
- SO-100/101 数据集从 377 名用户发布的 1,222 个公开 LeRobot 数据集中整理而来，包含 38,059 个 episode、1,980 万帧，以及约 184 小时的交互数据。
- DROID 子集在过滤空闲片段并要求有效语言指令后，包含 74,604 个有效成功 episode 和 17,758,044 帧。
- 摘录称 MolmoAct2 在 7 个仿真和真实世界基准上优于包括 π0.5 在内的强基线，但所给文本没有提供任务成功率数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.02881v2](https://arxiv.org/abs/2605.02881v2)
