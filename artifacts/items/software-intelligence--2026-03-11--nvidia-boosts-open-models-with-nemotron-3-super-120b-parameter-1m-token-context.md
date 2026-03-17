---
source: hn
url: https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super
published_at: '2026-03-11T23:09:15'
authors:
- teleforce
topics:
- open-models
- large-language-models
- agentic-ai
- mixture-of-experts
- long-context
relevance_score: 0.68
run_id: materialize-outputs
---

# Nvidia boosts open models with Nemotron 3 Super 120B parameter, 1M token context

## Summary
Nvidia发布了面向复杂智能体系统的开源大模型Nemotron 3 Super，主打120B参数、MoE架构、100万token上下文以及更强推理能力。其核心卖点不仅是开放权重，还开放训练数据、配方与评测流程，以推动开放生态。

## Problem
- 复杂agentic AI系统需要更强的推理能力、更长上下文和更高吞吐，但现有开放模型在性能、效率和可复现性上仍有限。
- 许多“开源”模型只开放权重，不开放训练数据与方法，导致社区难以复现、定制和持续改进。
- 北美开放模型生态在与DeepSeek、Qwen等开放模型竞争时，需要更强且更透明的替代方案，这对企业采用和生态发展都很重要。

## Approach
- Nvidia推出Nemotron 3 Super：一个120B参数、面向复杂智能体系统的开放模型，采用mixture-of-experts架构并强调高级推理能力。
- 模型支持**1 million token**上下文窗口，目标是处理更长链路任务、跨文档推理和多步agent工作流。
- 除开放模型权重外，Nvidia还开放“data and recipes”，包括预训练与后训练数据集、训练环境以及评测配方，降低复现和二次开发门槛。
- 官方将其定位为比前代更高效、更准确、更快的升级版本，并计划后续推出“4倍更大”的Ultra模型。

## Results
- 在**Artificial Analysis benchmark**上，Nemotron 3 Super据称超过了来自**OpenAI、Amazon和Google**的若干模型，但文中未给出具体分数。
- 在推理工作负载上，Nvidia声称其可比**GPT-OSS快2.2倍**。
- 早期采用者**CrowdStrike**表示，该模型在生产环境中相较其此前使用的模型实现了**3倍更高的准确率**，并在内部威胁狩猎基准上表现“非常好”，但未披露具体基准名称和数值。
- 模型规格方面，文中给出的关键数字包括**120B参数**和**1M token上下文窗口**。
- 生态投入方面，报道称Nvidia计划未来**5年投入260亿美元**建设开放模型生态，但这属于战略投资信息，不是模型性能指标。

## Link
- [https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super](https://www.thedeepview.com/articles/nvidia-boosts-open-models-with-nemotron-3-super)
