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
## 总结
StarVLA 是一个开源代码库，把多种视觉-语言-动作和世界模型机器人策略设计放在同一个模块化接口下。它的核心贡献是共享的 backbone 加 action head 结构、通用训练配方，以及覆盖主要机器人基准的统一评测栈。

## 问题
- VLA 研究分散在不兼容的架构、代码库和基准协议里，比较和复现都很难。
- 现有系统常把 backbone、action decoder、数据管线和评测设置绑在一起，换其中一部分通常就要重写其他部分。
- 这会影响通用机器人策略的进展，因为进展依赖公平的消融实验、可复用的基线，以及更容易在不同 embodiment 和基准之间迁移。

## 方法
- StarVLA 定义了一个统一的策略视图：把观测和语言映射到一个 action chunk，训练损失写成 action loss 加上可选的辅助损失。
- 代码库把每种方法拆成一个视觉-语言 backbone 和一个可插拔的 action head。两部分都可以替换，而不改训练循环或评测接口。
- 它在这种共享设计下实现了四种 action decoding 变体：自回归 action tokenization（StarVLA-FAST）、并行回归（StarVLA-OFT）、flow-matching 去噪（StarVLA-π），以及带 DiT action 模块的双系统推理（StarVLA-GR00T）。
- 它同时支持 Qwen-VL/Qwen3-VL 这类 VLM backbones 和 Cosmos/Cosmos-Predict2 这类 world-model backbones，也支持多模态共训练和跨 embodiment 训练的共享配方。
- 它把 LIBERO、SimplerEnv、RoboTwin 2.0、RoboCasa-GR1 和 BEHAVIOR-1K 的评测与部署统一起来，仿真和真机使用同一个接口。

## 结果
- 表 1 声称，StarVLA 支持 7 个集成基准；列出的开源基线中，OpenPI 是 2 个，Isaac-GR00T 是 6 个，OpenVLA-OFT 是 1 个，Dexbotic 是 5 个，X-VLA 是 5 个。
- 表 1 也声称，StarVLA 是列出的框架里唯一同时具备这些能力的：模块化 action heads、可替换的 VLM backbones、可替换的 world-model backbones、混合数据加载、开放的多模态共训练、开放的跨 embodiment 共训练，以及多基准共训练。
- 摘要说，它简单的单基准配方在多个基准上，使用 VLM 和 world-model backbones 时都能达到或超过之前的方法。
- 摘要没有给出基准分数、成功率，或相对已命名基线的精确提升，所以这里的定量性能证据还不完整。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05014v1](http://arxiv.org/abs/2604.05014v1)
