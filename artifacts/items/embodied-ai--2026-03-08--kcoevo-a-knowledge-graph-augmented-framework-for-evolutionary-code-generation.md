---
source: arxiv
url: http://arxiv.org/abs/2603.07581v1
published_at: '2026-03-08T10:39:48'
authors:
- Jiazhen Kang
- Yuchen Lu
- Chen Jiang
- Jinrui Liu
- Tianhao Zhang
- Bo Jiang
- Ningyuan Sun
- Tongtong Wu
- Guilin Qi
topics:
- code-migration
- knowledge-graph
- llm-code-generation
- api-evolution
- version-aware-reasoning
relevance_score: 0.06
run_id: materialize-outputs
---

# KCoEvo: A Knowledge Graph Augmented Framework for Evolutionary Code Generation

## Summary
KCoEvo提出了一个用知识图谱增强LLM进行跨版本代码迁移的框架，把“找出API如何演化”与“按这条演化路径生成新代码”分成两个阶段。核心目标是减少模型生成过时API、版本不兼容代码和不可执行输出的问题。

## Problem
- 论文解决的是**第三方库API持续演化导致旧代码失效、维护困难**的问题，这对现代软件开发很重要，因为项目通常依赖大量直接和间接包，版本变化会持续破坏兼容性。
- 现有LLM虽然能写代码，但缺少对**API跨版本关系与时间演化**的显式结构化表示，因此常输出过时API、语义不一致或版本不兼容代码。
- 普通RAG或提示方法只能给浅层上下文，难以进行**可控、可查询、可遍历**的版本迁移推理。

## Approach
- 先构建两类知识图：**静态API图**表示单个版本内部的结构关系，**动态图对齐图**表示跨版本的迁移关系，如 retain、remove、rename、relocate 等。
- 将代码迁移拆成两步：**evolution path retrieval** 先从图里找出从旧API到新API的可行迁移路径；**path-informed code generation** 再让LLM依据该路径生成新版本代码。
- 图构建基于开源仓库与包元数据，通过AST抽取函数、类、方法、参数、返回值、文档字符串等，再用规则从版本diff中挖掘跨版本变化。
- 查询时先检索相关子图，再用**BFS图遍历**和版本元数据动态对齐旧新API，得到候选演化轨迹。
- 训练监督来自**真实API diff自动生成的合成标注**，减少人工标注成本并提高可扩展性。

## Results
- 在VersiCode基准上，**所有模型在+KG设置下都优于原始Base模型**，指标包括 CDC@1 和 EM@1，说明结构化演化知识能显著提升代码迁移正确性与可执行性。
- **DeepSeek-V3** 在 Major→Major 上从 **59.52→96.83 (CDC@1)**、**59.52→100.00 (EM@1)**；在 Major→Minor 上从 **32.83→79.29**、**33.84→94.44**；在 Minor→Major 上从 **9.26→75.00**、**15.74→95.37**。
- **Qwen2.5-Coder-32B-Instruct** 提升很大：Major→Minor 的 **EM@1 16.16→92.42（+76.26）**，Minor→Major 的 **EM@1 7.41→87.96（+80.55）**。
- **Llama-3-70B-Instruct-Turbo** 在 Major→Minor 的 **EM@1 16.67→79.80（+63.13）**，Minor→Major 的 **EM@1 10.19→69.44（+59.25）**，显示复杂跨版本迁移受益明显。
- **Gemini-1.5-Pro-Latest** 在 Major→Minor 上达到 **92.93 CDC@1 / 98.48 EM@1**，在 Minor→Major 上达到 **72.22 CDC@1 / 98.15 EM@1**。
- 即使强模型 **GPT-5** 也有增益：Major→Major 的 **EM@1 95.23→100.00**，Minor→Minor 的 **EM@1 72.23→100.00**，说明显式结构化知识对高性能LLM仍然有价值；对比表3中的代码块RAG，普通检索提升有限，通常明显弱于KG方法。

## Link
- [http://arxiv.org/abs/2603.07581v1](http://arxiv.org/abs/2603.07581v1)
