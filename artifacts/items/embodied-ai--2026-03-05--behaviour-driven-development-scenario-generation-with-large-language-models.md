---
source: arxiv
url: http://arxiv.org/abs/2603.04729v1
published_at: '2026-03-05T02:05:48'
authors:
- Amila Rathnayake
- Mojtaba Shahin
- Golnoush Abaei
topics:
- llm-evaluation
- bdd-scenario-generation
- software-testing
- prompt-engineering
- dataset-release
relevance_score: 0.03
run_id: materialize-outputs
---

# Behaviour Driven Development Scenario Generation with Large Language Models

## Summary
本文评估 GPT-4、Claude 3 和 Gemini 在自动生成 BDD（行为驱动开发）场景上的能力，并构建了一个包含 500 条工业真实用户故事、需求描述和对应 BDD 场景的数据集。结论是：不同模型的最优提示策略不同，且详细需求描述比单独用户故事更关键；在综合评价中 Claude 3 更接近人工偏好，而 DeepSeek 作为评审器与人工判断相关性更强。

## Problem
- 论文解决的是**如何用大语言模型自动生成高质量 BDD 场景**的问题，以减少人工编写 Given/When/Then 测试场景的时间成本、经验依赖和覆盖不足。
- 这很重要，因为手工编写 BDD 场景在敏捷开发中是瓶颈：耗时、质量不稳定，且容易遗漏边界条件，影响测试覆盖和交付速度。
- 现有研究通常只看语法正确性或小规模数据，缺少**跨模型、跨提示方式、跨输入类型、跨评估维度**的系统比较。

## Approach
- 构建了一个**500 样本工业数据集**，来自 4 个专有软件产品，每个样本包含用户故事、需求描述和人工编写的 BDD 场景；作者声称这是首个此类公开数据集。
- 让 3 个 LLM（GPT-4o、Claude 3 Opus、Gemini 1.5 Flash）从不同输入生成 BDD 场景，并系统比较 4 个研究维度：基础效果、提示策略、输入类型、模型参数。
- 评估不是只看字符串匹配，而是采用**多维评价框架**：文本相似度、语义相似度、LLM 评审，以及人工专家评审。
- 进一步测试不同 prompting 策略（zero-shot、few-shot、chain-of-thought）、不同输入组合（用户故事+需求描述、仅用户故事、仅需求描述），以及不同解码参数（temperature、top_p）。

## Results
- 数据规模方面：实验基于**500** 条真实工业样本，覆盖 **4** 个软件产品；相较文中提到的近似对比工作仅 **≈50** 条公开样本，规模更大。
- 模型表现方面：**GPT-4** 在**文本相似度和语义相似度指标**上得分更高；但**Claude 3** 在**人工专家评审**和**LLM-based 评审**中被评为最佳。摘要未提供具体分数。
- 评审器方面：作为自动评审模型时，**DeepSeek 与人工判断的相关性强于其与文本/语义相似度指标的相关性**，说明基于 LLM 的评审可能比表面相似度更贴近真实质量。摘要未给出相关系数数值。
- 提示策略方面：最优方法**依模型而异**——**GPT-4 最适合 zero-shot，Claude 3 受益于 chain-of-thought，Gemini 在 few-shot 下最佳**。
- 输入类型方面：**详细 requirement description 单独使用就能生成高质量场景**；而**仅使用 user story 会得到较低质量结果**。这表明输入信息质量比输入格式本身更关键。
- 解码参数方面：跨所有模型，**temperature = 0、top_p = 1.0** 产生了最高质量的 BDD 场景；但论文摘录**未提供具体定量指标或提升幅度**。

## Link
- [http://arxiv.org/abs/2603.04729v1](http://arxiv.org/abs/2603.04729v1)
