---
source: arxiv
url: https://arxiv.org/abs/2605.30280v1
published_at: '2026-05-28T17:36:31'
authors:
- Qiuyue Wang
- Mingsheng Li
- Jian Guan
- Jinhui Ye
- Sicheng Xie
- Yitao Liu
- Junhao Chen
- Zhixuan Liang
- Jie Zhang
- Xintong Hu
- Xuhong Huang
- Pei Lin
- Junyang Lin
- Dayiheng Liu
- Shuai Bai
- Jingren Zhou
- Jiazhao Zhang
- Haoqi Yuan
- Gengze Zhou
- Hang Yin
- Ye Wang
- Yiyang Huang
- Zixing Lei
- Wujian Peng
- Delin Chen
- Yingming Zheng
- Jingyang Fan
- Xianwei Zhuang
- Xin Zhou
- Haoyang Li
- Anzhe Chen
- Tong Zhang
- Xuejing Liu
- Yuchong Sun
- Ruizhe Chen
- Zhaohai Li
- "Chenxu L\xFC"
- Zhibo Yang
- Tao Yu
- Xionghui Chen
topics:
- vision-language-action
- robot-foundation-model
- generalist-robot-policy
- robot-data-scaling
- cross-embodiment
- sim2real
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# Qwen-VLA: Unifying Vision-Language-Action Modeling across Tasks, Environments, and Robot Embodiments

## Summary
## 概要
Qwen-VLA 是一个统一的视觉-语言-动作策略，适用于不同机器人形态下的操作、导航和轨迹预测。它在 Qwen3.5-4B 上加入了基于 DiT 的 flow-matching 动作解码器，并用机器人、人体、仿真、导航和视觉-语言数据的混合数据进行训练。

## 问题
- 具身 AI 模型通常只绑定一个任务族、一个机器人本体或一个基准，这限制了它们在操作、导航和新机器人平台上的迁移能力。
- 机器人控制数据使用不同的动作类型、控制频率、预测跨度和维度；如果没有统一的训练接口，要把这些数据一起扩展会很难。
- 这个问题很重要，因为机器人基础模型需要更广的数据混合，才能在物体、场景、光照、语言和具身形态变化时提升泛化能力。

## 方法
- 核心机制很直接：模型读取图像、语言指令和当前机器人的文本描述，然后预测未来的动作或轨迹片段。
- 主干是用于视觉-语言理解的 Qwen3.5-4B。一个约 1.15B 参数的 DiT flow-matching 动作解码器生成连续动作。
- 具身感知提示会指定机器人标签、机械臂配置、控制频率和预测跨度，这样一个模型就能处理不同平台，而不用单独的输出头。
- 动作和轨迹使用共享的张量形状，并通过填充和掩码处理。每个数据集保留自己的控制约定，而掩码会防止填充通道影响训练。
- 训练分四个阶段：文本到动作解码器预训练、多模态继续预训练、监督微调，以及在 SimplerEnv 中进行强化学习。

## 结果
- Qwen-VLA-Instruct 在 LIBERO 上报告 97.9% 成功率，在 Simpler-WidowX 上报告 73.7%。
- 它在 RoboTwin-Easy 上报告 86.1%，在 RoboTwin-Hard 上报告 87.2%。
- 在导航任务上，它在 R2R 上报告 69.0% OSR，在 RxR 上报告 59.6% SR。
- 在真实世界 ALOHA 分布外实验中，它报告平均 76.9% 成功率。
- 在 DOMINO 动态操作任务上，它报告 26.6% 零样本成功率。
- 这段摘录给出了各个基准上的指标值，但没有提供逐项基线对比数字。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.30280v1](https://arxiv.org/abs/2605.30280v1)
