---
source: hn
url: https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super
published_at: '2026-03-11T23:09:15'
authors:
- teleforce
topics:
- open-llm
- agentic-ai
- mixture-of-experts
- long-context
- open-source-models
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Nvidia boosts open models with Nemotron 3 Super 120B parameter, 1M token context

## Summary
Nvidia发布了开源大模型Nemotron 3 Super，一款面向复杂agentic AI系统的120B参数模型，主打更长上下文、更强推理和更开放的训练配方。其意义不仅在于模型性能，还在于同时开放权重、数据与训练方法，以推动开源生态发展。

## Problem
- 开源大模型生态常常只开放权重，不开放训练数据、后训练流程和评测配方，导致外部团队难以复现、定制和可靠落地。
- 面向复杂代理式AI系统的模型需要同时具备长上下文、强推理能力和高效率，否则在真实生产环境中成本高、速度慢、效果不稳定。
- 北美开源模型生态近期在影响力上受到中国开源模型挤压，因此需要更强、更透明的开放模型来增强生态竞争力。

## Approach
- Nvidia推出Nemotron 3 Super：120B参数、mixture-of-experts架构、1M token上下文窗口，定位为复杂agentic AI系统的基础模型。
- 核心机制可以简单理解为：让模型在超长文本范围内进行推理，并通过专家混合架构在不同任务上更高效地调用“专长模块”，从而提升速度和准确性。
- 除了开放模型权重，Nvidia还开放训练“data and recipes”，包括预训练与后训练数据集、训练环境以及评测流程。
- 该发布强调可复现与可定制，目标是帮助开发者和企业更容易基于同一方法做适配和部署。

## Results
- 在Artificial Analysis基准上，Nemotron 3 Super超过了来自OpenAI、Amazon和Google的若干模型，但文中未给出具体分数或完整对比表。
- Nvidia称其在推理工作负载上可比GPT-OSS快**2.2倍**。
- CrowdStrike表示，在提前接入后，该模型相较其此前生产中使用的模型，准确率提高了**3倍**，并且在内部threat hunting基准上表现“非常出色”。
- 模型规模为**120B参数**，上下文窗口为**100万token**。
- Nvidia还透露即将发布一个“**4倍更大**”的Ultra版本。
- 文中没有提供论文式的标准学术数据集、误差条或详细消融实验，因此定量证据主要来自基准排名描述与企业早期采用反馈。

## Link
- [https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super](https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super)
