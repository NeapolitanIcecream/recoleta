---
source: arxiv
url: https://arxiv.org/abs/2607.06074v1
published_at: '2026-07-07T09:44:46'
authors:
- Rohit Mehra
- Kapil Singi
- Vikrant Kaulgud
- Vibhu Saujanya Sharma
- Swapnajeet Gon Choudhury
- Swati Sharma
- Adam P. Burden
- Majd Sakr
topics:
- prompt-engineering
- code-generation
- agentic-tutor
- ide-assistant
- human-ai-interaction
- software-engineering-education
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Prompt Coach: An Empirical Evaluation of an Agentic Tutor for Learning Prompt Engineering in Software Development

## Summary
## 摘要
Prompt Coach 是一个 VSCode 导师，通过评分反馈和苏格拉底式提问，教开发者写出更好的代码生成提示词。在一项包含 15 名开发者的前后测研究中，单次 60 分钟学习将平均提示词质量分数从 63.04 提高到 71.69。

## 问题
- 开发者现在要求 LLM 生成代码时，需要表达意图、约束、上下文、输出格式、测试和边界情况。
- 静态课程、教程和提示词指南提供的是通用建议，无法根据开发者的代码库、任务、目标模型或技能缺口作出反应。
- 这项技能很重要，因为质量差的提示词可能漏掉约束、错误处理和验证细节，从而影响生成代码的质量。

## 方法
- Prompt Coach 在 VSCode 内运行，是一个多智能体系统，使用 CrewAI、Azure 后端服务、用于项目上下文检索的 ChromaDB，以及用于评判和指导的 GPT-4.1 构建。
- 它读取本地项目上下文，包括代码、设计说明、风格指南和可用的需求文档，然后将相关信息存入项目专属的向量数据库。
- 它从 8 个维度对每个开发者提示词进行 0 到 100 分评分：清晰度、具体性、上下文感知、适应性、约束包含、错误处理、输出要求和可测试性。
- 一个结果预览智能体会询问目标 LLM 当前提示词会生成什么，在内部使用可能的失败模式，并且不会向学习者展示生成的代码。
- 一个苏格拉底式指导智能体会把薄弱维度转化为有针对性的问题，同时一个开发者建模智能体会跟踪多轮迭代中的重复优势和缺口。

## 结果
- 研究规模为 15 名专业开发者，平均经验为 9.6 年，采用单组被试内前后测设计，覆盖 6 个 APPS 基准任务。
- 总体提示词质量分数从基线的 63.04 提高到学习后的 71.69，相对提升 13.73%，配对 Wilcoxon 检验 p<.001。
- 按任务复杂度划分，入门任务从 65.63 提高到 74.48（+13.93%，p=0.003），面试任务从 62.56 提高到 69.05（+10.38%，p=0.004），竞赛任务从 60.66 提高到 71.34（+17.71%，p=0.001）。
- 提升最大的维度是约束包含，从 50.51 提高到 66.49（+31.63%，p<.001）；错误处理从 52.56 提高到 68.67（+30.66%，p<.001）；上下文感知从 56.56 提高到 69.91（+23.61%，p=0.002）。
- 清晰度没有提高：从 79.87 到 79.71（-0.19%，p=0.577）。适应性从 66.89 提高到 69.58（+4.02%），但在 p=0.208 下不显著。
- 7 点李克特量表上的感知评分为正向：100% 的人同意这次学习提高了提示词写作技能，93.3% 的人同意信任该工具，86.7% 的人同意可能采用，80.0% 的人同意 Prompt Coach 比书籍、博客、教程、文章和 MOOC 更有用。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.06074v1](https://arxiv.org/abs/2607.06074v1)
