---
source: arxiv
url: http://arxiv.org/abs/2604.23775v1
published_at: '2026-04-26T15:58:19'
authors:
- Qi Li
- Bo Yin
- Weiqi Huang
- Ruhao Liu
- Bojun Zou
- Runpeng Yu
- Jingwen Ye
- Weihao Yu
- Xinchao Wang
topics:
- vision-language-action
- robot-safety
- adversarial-robustness
- survey-paper
- embodied-ai
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Vision-Language-Action Safety: Threats, Challenges, Evaluations, and Mechanisms

## Summary
## 概述
本文是一篇关于机器人中视觉-语言-行动（VLA）模型的安全风险、防御、评估方法和部署问题的综述。其主要贡献是按攻击发生时间和防御应用时间，给出了一张统一的领域地图。

## 问题
- VLA 模型把感知、语言和机器人控制放在同一个策略里，出错时造成的可能是物理伤害，而不只是错误文本输出。
- 它们的攻击面覆盖图像、语言提示、本体感知状态、训练数据和长动作序列，这让安全工作比只处理文本的模型或传统模块化机器人更难。
- 现有工作分散在对抗机器学习、机器人学习、对齐和自主系统安全等方向，没有一篇综述把威胁、防御、基准和部署风险系统地连在一起。

## 方法
- 论文把 VLA 安全定义为一个不同于 LLM 安全和传统机器人安全的主题，然后回顾标准 VLA 设置：视觉编码器、语言主干、动作解码器、模仿学习训练，以及部署时推理。
- 它按两个时间轴整理文献：**攻击时间**（训练时 vs 推理时）和 **防御时间**（训练时 vs 推理时）。
- 在这个分类下，论文综述了训练时威胁，如数据投毒和后门，以及推理时威胁，如对抗补丁、跨模态扰动、越狱和冻结攻击。
- 它还回顾了防御、 安全基准与指标，以及覆盖六个应用领域的部署问题，然后列出开放问题，例如轨迹的可认证鲁棒性、可在物理世界实现的防御、安全感知训练、运行时安全架构和标准化评估。

## 结果
- 这是一篇综述论文，所以摘录部分没有给出新的实验基准数值或新的模型准确率结果。
- 论文声称自己是**首篇**全面聚焦 VLA 安全、覆盖攻击、防御、评估和部署的综述。
- 它提出了一个**二维分类法**：攻击时间有**2 类**（训练时、推理时），防御时间有**2 类**（训练时、推理时）。
- 论文说明部署分析覆盖**6 个主要领域**。
- 背景部分总结了支撑这篇安全综述的代表性 VLA 系统规模：**RT-1** 在 **13 台机器人**上、历时 **17 个月**，用 **13 万以上**条真实机器人演示进行训练；**Open X-Embodiment** 包含来自 **21 家机构**、覆盖 **22 种 embodiment** 的约 **100 万**条演示；**Octo** 使用约 **80 万**条轨迹；**OpenVLA** 是一个 **7B** 模型，在 **97 万**个 episode 上微调；**RT-2** 建立在一个 **55B** 的视觉-语言模型之上。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23775v1](http://arxiv.org/abs/2604.23775v1)
