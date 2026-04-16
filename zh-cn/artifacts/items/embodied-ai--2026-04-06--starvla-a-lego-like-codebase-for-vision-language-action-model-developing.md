---
source: arxiv
url: http://arxiv.org/abs/2604.05014v1
published_at: '2026-04-06T17:59:21'
authors:
- StarVLA Community
topics:
- vision-language-action
- robot-foundation-model
- world-model
- generalist-robot-policy
- benchmarking
- open-source-codebase
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# StarVLA: A Lego-like Codebase for Vision-Language-Action Model Developing

## Summary
## 摘要
StarVLA 是一个开源代码库，用一个模块化接口统一了多种 vision-language-action 和 world-model 机器人策略设计。它的主要贡献是共享的 backbone-plus-action-head 结构、通用训练配方，以及覆盖主要机器人基准的统一评测栈。

## 问题
- VLA 研究分散在不兼容的架构、代码库和基准协议中，这使比较和复现变得困难。
- 现有系统常常把 backbone、动作解码器、数据流水线和评测设置绑在一起，所以替换一个部分通常就需要重写其余部分。
- 这很重要，因为通用机器人策略的进展依赖公平的消融实验、可复用的基线，以及在不同 embodiment 和基准之间更容易迁移。

## 方法
- StarVLA 定义了一个通用的策略视图：将观测和语言映射为一个动作块，训练损失写成动作损失加上可选的辅助损失。
- 代码库将每种方法拆分为视觉-语言 backbone 和可插拔的动作头。任一部分都可以替换，而不需要改动训练循环或评测接口。
- 它在这个共享设计下实现了四种动作解码变体：自回归动作标记化（StarVLA-FAST）、并行回归（StarVLA-OFT）、flow-matching 去噪（StarVLA-π），以及带有 DiT 动作模块的双系统推理（StarVLA-GR00T）。
- 它同时支持 VLM backbones，如 Qwen-VL/Qwen3-VL，以及 world-model backbones，如 Cosmos/Cosmos-Predict2，并提供多模态联合训练和跨 embodiment 训练的共享配方。
- 它统一了 LIBERO、SimplerEnv、RoboTwin 2.0、RoboCasa-GR1 和 BEHAVIOR-1K 的评测与部署，对仿真和真实机器人使用同一套接口。

## 结果
- 表 1 称，StarVLA 支持 7 个已集成基准，而列出的开源基线支持 1 到 6 个：OpenPI（2）、Isaac-GR00T（6）、OpenVLA-OFT（1）、Dexbotic（5）和 X-VLA（5）。
- 表 1 还称，StarVLA 是列出框架中唯一同时具备以下能力的框架：模块化动作头、可替换的 VLM backbones、可替换的 world-model backbones、混合数据加载、开放的多模态联合训练、开放的跨 embodiment 联合训练，以及多基准联合训练。
- 摘要称，它的简单单基准训练配方在多个基准上，使用 VLM 和 world-model backbones 时都能达到或超过先前方法。
- 这段摘录没有给出基准分数、成功率或相对具名基线的精确增益，因此这里的定量性能证据还不完整。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05014v1](http://arxiv.org/abs/2604.05014v1)
