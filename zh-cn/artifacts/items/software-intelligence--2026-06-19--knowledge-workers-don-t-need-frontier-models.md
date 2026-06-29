---
source: hn
url: https://mukulsingh105.github.io/articles/slm-routing-knowledge-workers.html
published_at: '2026-06-19T23:09:41'
authors:
- azhenley
topics:
- model-routing
- small-language-models
- knowledge-work
- domain-tuning
- cost-latency
- code-intelligence
relevance_score: 0.64
run_id: materialize-outputs
language_code: zh-CN
---

# Knowledge workers don't need frontier models

## Summary
## 摘要
文章认为，多数知识工作者任务可以交给小型、面向领域调优的语言模型，并由低成本路由器选择模型；前沿模型只处理更难的情况。它的主要主张是，在 GDPVal 和 Microsoft MAI 示例中，这种做法能降低成本和延迟，同时质量接近只用前沿模型的系统。

## 问题
- 知识工作者常在电子表格、电子邮件和文档中处理结构化任务。对这些任务来说，上下文、速度和可靠性通常比最高推理能力更重要。
- 许多任务适合小模型时，把每个请求都发给前沿模型会提高推理成本和延迟。
- 成本差距在规模化时影响很大：文章使用的前提是，80% 的请求可以使用成本低 10×、速度快 2× 的模型。

## 方法
- 一个 nano-model 路由器会分类每个用户任务，并把困难任务发送给 GPT-5.5，把较简单的任务发送给 GPT-5.4 Mini。
- 路由器会在会话中锁定所选模型，以保留提示缓存并保持输出行为稳定。
- 文中称路由开销低于每个请求 $0.01。
- 文章把路由与领域后训练结合使用：蒸馏、强化学习，以及基于干净数据的领域适配，并通过 Microsoft MAI 和 Frontier Tuning 示例说明。

## 结果
- 在 GDPVal-AA 上，GPT-5.4 Mini 单独得分为 1417 ELO，GPT-5.5 单独得分为 1769 ELO，路由后的 GPT-5.5/GPT-5.4 Mini 配置得分为 1759 ELO。
- 文中称，该路由配置在 368 个模型配置中总排名第 #2，并且与单独使用 GPT-5.5 的差距在 10 ELO 分以内。
- 文章称 GPT-5.5 的成本超过 GPT-5.4 Mini 的 10×，而路由系统相较单独使用 GPT-5.5 只损失 10 ELO 分。
- 文中称，MAI-Code-1-Flash 约有 5B 个活跃参数，在所有测试的编码基准上都超过 Claude Haiku 4.5，包括 SWE-Bench Pro 上 51.2% 对 35.2%，同时 token 用量最多减少 60%。
- 文中称，MAI-Thinking-1 有 35B 个活跃参数，在 SWE-Bench Pro 上追平 Claude Opus 4.6，在 AIME 2025 上得分 97%，并在覆盖 1,276 个任务的盲测人类偏好测试中胜过 Sonnet 4.6。
- 文章称，面向 Excel 的 Frontier-Tuned MAI 达到 GPT-5.4 的水平，推理成本最多低 10×；整体的路由加调优 SLM 配置可降低 75–90% 成本，并带来 2–3× 的延迟改善。

## Problem

## Approach

## Results

## Link
- [https://mukulsingh105.github.io/articles/slm-routing-knowledge-workers.html](https://mukulsingh105.github.io/articles/slm-routing-knowledge-workers.html)
