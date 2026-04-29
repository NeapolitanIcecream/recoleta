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
## 摘要
这篇论文综述了机器人中视觉-语言-动作（VLA）模型的安全风险、防御方法、评估方法和部署问题。它的主要贡献是给出了一张统一的领域地图，按攻击发生的时间和防御施加的时间来组织相关工作。

## 问题
- VLA 模型把感知、语言和机器人控制连接到同一个策略中，因此故障可能造成物理伤害，而不只是生成错误文本。
- 其攻击面覆盖图像、语言提示、本体感觉状态、训练数据和长时动作序列，这让安全研究比纯文本模型或经典模块化机器人系统更难。
- 以往工作分散在对抗机器学习、机器人学习、对齐和自主系统等领域，缺少一个把威胁、防御、基准和部署风险放在一起的总览。

## 方法
- 论文将 VLA 安全界定为不同于 LLM 安全和经典机器人安全的独立主题，然后回顾标准的 VLA 组成：视觉编码器、语言主干、动作解码器、基于模仿学习的训练，以及部署时的推理机制。
- 它沿着两个时间轴组织文献：**攻击时机**（training-time vs inference-time）和 **防御时机**（training-time vs inference-time）。
- 在这一分类下，论文综述了训练阶段威胁，如数据投毒和后门；也综述了推理阶段威胁，如对抗补丁、跨模态扰动、越狱和冻结攻击。
- 论文还回顾了防御方法、安全基准与指标，以及六个应用领域中的部署问题，并列出开放问题，如面向轨迹的认证鲁棒性、物理可实现的防御、安全感知训练、运行时安全架构和标准化评估。

## 结果
- 这是一篇综述论文，因此摘录中没有报告新的实验基准数字，也没有新的模型精度结果。
- 论文称自己是**首篇全面聚焦 VLA 安全**的综述，覆盖攻击、防御、评估和部署。
- 它提出了一个**二维分类法**：攻击时机有 **2 类**（training-time、inference-time），防御时机也有 **2 类**（training-time、inference-time）。
- 论文指出，部署分析覆盖了 **6 个主要领域**。
- 背景部分总结了推动这篇安全综述的代表性 VLA 系统规模：**RT-1** 在 **17 个月**内基于来自 **13 台机器人**的 **13 万+** 条真实机器人演示进行训练；**Open X-Embodiment** 包含约 **100 万** 条演示，覆盖来自 **21 家机构**的 **22 种 embodiment**；**Octo** 使用约 **80 万** 条轨迹；**OpenVLA** 是一个 **7B** 模型，在 **970k** 个 episode 上微调；**RT-2** 建立在一个 **55B** 视觉语言模型之上。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23775v1](http://arxiv.org/abs/2604.23775v1)
