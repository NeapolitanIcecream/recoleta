---
source: arxiv
url: http://arxiv.org/abs/2603.08604v1
published_at: '2026-03-09T16:52:27'
authors:
- Tianyi Li
- Satya Samhita Bonepalli
- Vikram Mohanty
topics:
- llm-sensemaking
- human-ai-collaboration
- hypothesis-generation
- fact-extraction
- prompting
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# What to Make Sense of in the Era of LLM? A Perspective from the Structure and Efforts in Sensemaking

## Summary
本文探讨在复杂sensemaking任务中，LLM如何与人类协作，并以虚构恐怖袭击线索分析为案例比较GPT-4与众包新手分析者。初步结果表明，LLM更擅长提出更广覆盖的假设，而人类在事实提取的完整性上更强。

## Problem
- 论文要解决的问题是：在面对复杂、模糊、多文档信息时，LLM应如何帮助人类完成sensemaking，以及这种帮助在哪些环节最有效。
- 这很重要，因为复杂分析任务既需要从原始材料中提取可靠事实，也需要在不完整信息下形成合理假设，而LLM虽然强于综合推断，却容易幻觉和失真。
- 作者特别关心：LLM与人类相比，在“提取事实”和“生成与答案键一致的假设”两方面各自表现如何。

## Approach
- 使用一个包含10份文档的数据集，任务是围绕虚构恐怖活动提出若干合理假设。
- 将GPT-4的两种使用方式与既有众包新手基线对比：一种是**holistic**，直接让模型整体生成替代性假设；另一种是**step-by-step**，要求模型按预定义步骤产出中间分析结果。
- 评估采用两个核心指标：**Coverage**（覆盖了多少相关事实/假设）和**Comprehensiveness**（覆盖内容在细节上是否完整、准确）。
- 核心机制可以最简单理解为：比较“让LLM自由总体分析”与“让LLM按人类分析流程逐步做”这两种协作模式，看哪种更适合复杂sensemaking。

## Results
- 在**事实提取**上，众包分析覆盖了**17个关键事实**，且**17个都是comprehensive**；这是文中最强的人类基线结果。
- 在**holistic**方式下，LLM仅隐式覆盖了**6个事实**，且**0个comprehensive**，说明它会直接跳向假设而忽略扎实列证。
- 在**step-by-step**方式下，LLM事实提取提升到**9个事实**，其中**5个comprehensive**；相较holistic有改进，但仍明显弱于人类基线的17个全面事实。
- 在**假设生成**上，众包分析覆盖了**15个预定义假设中的4个**，且**4个都是comprehensive**。
- **holistic** LLM在假设层面表现最强：覆盖了**10/15个假设**，其中**6个comprehensive**，显著高于众包的**4/15**覆盖。
- **step-by-step** LLM在假设上反而较弱，仅**comprehensively covered 3 hypotheses**；论文未给出更完整的总覆盖数，但明确说明其假设表现低于holistic。

## Link
- [http://arxiv.org/abs/2603.08604v1](http://arxiv.org/abs/2603.08604v1)
