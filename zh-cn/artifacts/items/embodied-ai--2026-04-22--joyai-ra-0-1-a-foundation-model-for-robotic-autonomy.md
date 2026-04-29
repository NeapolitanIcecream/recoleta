---
source: arxiv
url: http://arxiv.org/abs/2604.20100v2
published_at: '2026-04-22T01:51:48'
authors:
- Tianle Zhang
- Zhihao Yuan
- Dafeng Chi
- Peidong Liu
- Dongwei Li
- Kejun Hu
- Likui Zhang
- Junnan Nie
- Ziming Wei
- Zengjue Chen
- Yili Tang
- Jiayi Li
- Zhiyuan Xiang
- Mingyang Li
- Tianci Luo
- Hanwen Wan
- Ao Li
- Linbo Zhai
- Zhihao Zhan
- Xiaodong Bai
- Jiakun Cai
- Peng Cao
- Kangliang Chen
- Siang Chen
- Yixiang Dai
- Shuai Di
- Yicheng Gong
- Chenguang Gui
- Yucheng Guo
- Peng Hao
- Qingrong He
- Haoyang Huang
- Kunrui Huang
- Zhixuan Huang
- Shibo Jin
- Yixiang Jin
- Anson Li
- Dongjiang Li
- Jiawei Li
- Ruodai Li
- Yihang Li
- Yuzhen Li
- Jiaming Liang
- Fangsheng Liu
- Jing Long
- Mingxi Luo
- Xing Pan
- Hui Shen
- Xiaomeng Tian
- Daming Wang
- Song Wang
- Junwu Xiong
- Hang Xu
- Wanting Xu
- Zhengcheng Yu
- He Zhang
- Jiyao Zhang
- Lin Zhao
- Chen Zhou
- Nan Duan
- Yuzheng Zhuang
- Liang Lin
topics:
- vision-language-action
- robot-foundation-model
- cross-embodiment-transfer
- generalist-robot-policy
- sim2real
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# JoyAI-RA 0.1: A Foundation Model for Robotic Autonomy

## Summary
## 摘要
JoyAI-RA 0.1 是一个用于机器人操作的视觉-语言-动作基础模型，混合使用网页数据、人类第一视角视频、仿真轨迹和真实机器人示范。论文称，这种数据组合加上统一动作空间，提高了跨 embodiment 迁移能力，并提升了仿真环境和真实人形机器人上的成功率。

## 问题
- 机器人操作模型难以在开放世界中泛化，因为机器人数据集获取成本高、任务覆盖窄，对长尾交互的支持也弱。
- 来自人类、模拟器和不同机器人的数据使用不同的身体结构和动作格式，这使得行为在不同 embodiment 之间迁移很困难。
- 这很重要，因为通用机器人自主能力需要策略能够处理新的任务、场景和硬件，而不是每次都重新收集大量新的机器人数据。

## 方法
- JoyAI-RA 在四类数据上训练一个 VLA 模型：多模态网页数据、名为 EgoLive 的内部第一视角人类操作数据集、仿真数据集，以及包括 JDAgibot 和开源语料在内的真实机器人数据集。
- 核心机制是显式的统一动作空间：将动作和本体感觉映射到一个固定的共享表示中，主要使用相机坐标系下的末端执行器坐标，并对不同机器人缺失的自由度进行掩码处理。
- 模型包含一个用于语义和空间理解的视觉-语言骨干网络，以及一个基于 Perceiver 的动作专家模块，用 flow-matching 目标预测连续动作块。
- 训练分为三个阶段：在多模态任务上进行 VLM 共同预训练、在对齐的异构数据上进行带动作学习的 VLA 共同预训练，以及在目标机器人 embodiment 上进行后训练。
- 来自 EgoLive 的人手轨迹会被估计并重定向到 ALOHA、Fourier 和 Agibot G1 等机器人 embodiment 上，以支持跨 embodiment 学习。

## 结果
- 在 RoboTwin 2.0 上，JoyAI-RA 在 Easy 上报告 **90.48%** 的成功率，在 Hard 上报告 **89.28%**，超过 π0（**65.92/58.40**）、π0.5（**82.74/76.76**）、Motus（**88.66/87.02**）和 LingBot-VLA（**88.56/86.68**）。
- 在 RoboCasa GR1 Tabletop 上，JoyAI-RA 报告 **63.2%** 的平均成功率，高于 ABot-M0（**58.3%**）、DualCoT-VLA（**55.1%**）、TwinBrainVLA（**54.6%**）、Being-H0.7（**49.2%**）、GR00T-N1.6（**47.6%**）和 Qwen3PI（**43.9%**）。
- 在真实世界 AgiBot 基准上，跨任务平均成功率从 π0.5 的 **0.62** 提高到 JoyAI-RA 的 **0.74**，覆盖六个任务，每个任务 20 次试验。
- 论文强调了 RoboCasa 长时程任务上的较大提升：相比此前最佳结果，**CanToDrawerClose +16.0**、**MilkToMicrowaveClose +24.0**、**TrayToPot +18.0**。
- RoboTwin 2.0 上的 EgoLive 消融实验显示，**JDAgibot + full EgoLive** 的成功率为 **87.42%**，相比之下，无预训练为 **81.64%**，仅 JDAgibot 为 **77.62%**，**JDAgibot + 10% EgoLive** 为 **81.40%**。
- 摘录给出了数据集规模细节，没有提供预训练 token 总量或模型规模。文中称 EgoLive 覆盖 **1,969** 个物体类别、**1,796** 个动作类别，以及超过 **10k** 个任务，场景包括家庭、零售和物流。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.20100v2](http://arxiv.org/abs/2604.20100v2)
