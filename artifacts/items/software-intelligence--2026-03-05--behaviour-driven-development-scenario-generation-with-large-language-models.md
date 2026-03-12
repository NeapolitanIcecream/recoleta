---
source: arxiv
url: http://arxiv.org/abs/2603.04729v1
published_at: '2026-03-05T02:05:48'
authors:
- Amila Rathnayake
- Mojtaba Shahin
- Golnoush Abaei
topics:
- bdd-scenario-generation
- large-language-models
- software-testing
- requirements-engineering
- llm-evaluation
relevance_score: 0.88
run_id: materialize-outputs
---

# Behaviour Driven Development Scenario Generation with Large Language Models

## Summary
本文评估了 GPT-4、Claude 3 和 Gemini 在自动生成行为驱动开发（BDD）场景上的能力，并构建了一个包含 500 条工业级用户故事、需求描述与对应 BDD 场景的数据集。研究表明，不同模型和提示策略各有最优配置，而且高质量需求描述比单独用户故事更关键。

## Problem
- 论文要解决的是：如何用大语言模型自动生成高质量的 BDD/Gherkin 场景，以减少人工编写测试场景的时间、经验门槛和覆盖不足问题。
- 这很重要，因为手工编写 BDD 场景在敏捷和持续交付环境中既慢又不稳定，容易遗漏边界情况，成为测试与交付瓶颈。
- 现有工作对该任务的系统性评估不足，尤其缺少跨模型、跨提示方式、跨输入类型、跨评估维度的全面比较。

## Approach
- 构建了一个新的数据集：来自 4 个工业软件产品的 500 条样本，每条包含 user story、requirement description 和人工编写的参考 BDD scenario。
- 使用 3 个 LLM 生成 BDD 场景：GPT-4o、Claude 3 Opus、Gemini 1.5 Flash，并比较它们在该任务上的表现。
- 采用多维评估框架：文本相似度、语义相似度、LLM-as-a-judge 评估，以及人工专家评估，而不只看语法是否正确。
- 系统考察 4 个因素：基础生成效果、提示策略（zero-shot、few-shot、chain-of-thought）、输入形式（仅 user story、仅 requirement description、两者结合）、采样参数（temperature、top_p）。
- 核心机制可以简单理解为：把自然语言需求喂给 LLM，让它直接生成 Given/When/Then 格式的 BDD 场景，再用自动指标和人工评价判断生成质量。

## Results
- 数据集规模为 **500** 条样本，来源于 **4** 个真实工业软件产品；作者声称这是首个此类公开 BDD 场景数据集。
- 在文本与语义相似度指标上，**GPT-4** 得分更高；但在 **人工专家评价** 和 **LLM-based evaluation** 中，**Claude 3** 生成的场景被评为最佳。
- 作为自动评审器时，**DeepSeek** 与人工判断的相关性强于它与文本/语义相似度指标之间的相关性；摘要未提供具体相关系数数值。
- 提示效果具有明显模型依赖性：**GPT-4 最适合 zero-shot**，**Claude 3 从 chain-of-thought 中获益最大**，**Gemini 在 few-shot 下最佳**。
- 输入质量显著影响结果：**详细 requirement description 单独使用就能生成高质量场景**，而**仅使用 user story 会得到较低质量结果**；摘要未给出具体分数差值。
- 采样参数方面，跨模型最优设置为 **temperature = 0**、**top_p = 1.0**，作者称该配置生成的 BDD 场景质量最高；提供文本中未给出具体绝对指标数值或统计显著性。

## Link
- [http://arxiv.org/abs/2603.04729v1](http://arxiv.org/abs/2603.04729v1)
