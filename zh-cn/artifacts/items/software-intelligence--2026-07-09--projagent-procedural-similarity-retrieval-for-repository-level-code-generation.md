---
source: arxiv
url: https://arxiv.org/abs/2607.08691v1
published_at: '2026-07-09T16:50:54'
authors:
- QiHong Chen
- Aaron Imani
- Iftekhar Ahmed
topics:
- code-generation
- repository-level-generation
- procedural-retrieval
- code-intelligence
- agentic-workflow
- static-analysis
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# ProjAgent: Procedural Similarity Retrieval for Repository-Level Code Generation

## Summary
## 摘要
ProjAgent 通过检索计算过程相似的函数来改进仓库级代码生成，即使这些函数的名称和所属领域不同。它将过程检索、词法检索和语义检索结合起来，并使用基于静态分析的代码修复。

## 问题
- 仓库级代码生成必须处理跨文件依赖、项目 API、类型和编码约定。
- BM25、稠密检索及相关方法可能遗漏有用函数：这些函数的实现步骤与目标相似，但使用不同的词汇或服务于其他领域。
- 缺少上下文或上下文存在误导时，模型可能虚构 API、生成无效代码，并降低生成准确率。

## 方法
- 将仓库函数和目标任务分解为逻辑实现步骤，例如输入验证或状态转换。
- 使用由隐藏状态得到的 LLM 推理子空间投影表示每个步骤，再通过余弦相似度比较步骤。
- 在相似度搜索前减去均值和第一主成分，以降低表示的各向异性。
- 使用智能体工作流识别并验证过程相似的函数，将这些函数与词法和语义上下文结合起来，再通过 Qwen2.5-Coder-14B-Instruct 生成目标函数。
- 对生成的代码运行编译器和静态分析反馈，并迭代修复检测到的错误。

## 结果
- ProjAgent 在 REPOCOD 仓库级代码生成基准测试上达到 41.14% 的 Pass@1。
- 论文称该结果优于现有的基于检索的基线方法，但提供的摘录没有包含基线分数或提升幅度。
- 尽管词法重叠较低且不存在直接调用依赖，该方法仍能检索跨领域的过程匹配项，例如 `BlackBody.evaluate` 和 `FLRW.m_nu` 中的验证步骤。
- 论文称 PCA 去偏能提高过程余弦相似度的判别价值；摘录没有提供单独的消融实验数值。
- 提供的文本没有包含各检索组件或静态分析修复的其他量化结果。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08691v1](https://arxiv.org/abs/2607.08691v1)
