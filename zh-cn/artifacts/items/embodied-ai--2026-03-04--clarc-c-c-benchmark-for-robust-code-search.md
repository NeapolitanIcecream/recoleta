---
source: arxiv
url: http://arxiv.org/abs/2603.04484v1
published_at: '2026-03-04T18:57:37'
authors:
- Kaicheng Wang
- Liyan Huang
- Weike Fang
- Weihang Wang
topics:
- code-search
- benchmark
- c-cpp
- retrieval-robustness
- program-understanding
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# CLARC: C/C++ Benchmark for Robust Code Search

## Summary
CLARC 是一个面向 C/C++ 代码检索的鲁棒性基准，重点测试模型是否真正理解代码语义，而不是依赖变量名、函数名等表面词汇线索。论文还提出一条自动化数据构建流程，并用真实 GitHub 项目、可编译代码、匿名化与低级语言变换来系统暴露现有检索模型的弱点。

## Problem
- 现有代码搜索基准大多偏向 Python，**缺少真实世界 C/C++ 文本到代码检索**评测，导致研究结论难以迁移到系统编程场景。
- 很多现有数据集中的代码片段**不可编译或上下文不完整**，无法反映真实开发中依赖类型、辅助函数和上下文理解的重要性。
- 现有基准很少测试**变量重命名、标识符匿名化、编译到 Assembly/Wasm**等扰动下的鲁棒性，因此高分可能只是利用词汇匹配，而不是真正理解代码语义；这很重要，因为真实环境中存在混淆、攻击和跨抽象层检索需求。

## Approach
- 构建了一个自动化流水线，从 **144 个真实 GitHub C/C++ 仓库**中抽取函数，并保留其依赖上下文；仅保留在预设环境中**可编译**的样本。
- 将样本按依赖复杂度分为三组：**Group 1** 仅依赖标准库，**Group 2** 使用自定义类型，**Group 3** 调用用户定义辅助函数；其中 Group 3 还分为 **Short/Long** 两种上下文形式。
- 使用 **LLM（o3-mini、grok-4）** 自动生成自然语言查询，并通过**人工双盲评分 + bootstrap 假设检验**验证查询质量是否可与人工描述相当。
- 为了隔离词汇特征影响，设计了多种鲁棒性设置：**neutralized**（通用占位符匿名化）、**randomized**（随机命名）、**assembly**、**webassembly**，从源代码逐步去除标识符与高层语义线索。
- 在该基准上评测了 **6 个检索模型**，包括 BM25、CodeT5+、OASIS、Nomic-emb-code、OpenAI text-embedding-large、Voyage-code-3。

## Results
- CLARC 数据规模为 **6,717 对 query-code 样本**，其中 **1,245** 用于评测、**5,472** 用于训练；评测集来自 **45 个仓库**，训练集来自 **99 个仓库**。
- 查询质量验证中，LLM 生成描述与人工描述相当或更好：例如 **Group 1** 中 LLM 分数 **86.0**，人工 **60.0**，p-value **99.99%**；**Group 2** 为 **76.5 vs 72.0**（p-value **76.32%**）；**Group 3** 为 **75.5 vs 71.5**（p-value **84.92%**）。
- 在标准设置下，强模型表现很高：**Group 2** 上 **Voyage** 达到 **NDCG 94.06 / MRR 92.10 / MAP 92.11 / R@1 85.93**，**Nomic** 达到 **NDCG 93.61 / MRR 91.61**；相比之下 **BM25** 仅 **NDCG 17.83 / MRR 14.64**。
- **Group 1** 标准设置中，最佳结果接近饱和：**OASIS** 达 **NDCG 89.08 / MRR 86.54 / R@20 98.48**，**Voyage** 达 **NDCG 88.99 / MRR 86.93**，明显优于 **CodeT5+** 的 **NDCG 64.54**。
- 对更复杂的 **Group 3 Short**，性能明显下降：最佳 **Voyage** 仅 **NDCG 66.66 / MRR 80.53 / MAP 50.93 / R@1 27.28**，说明辅助函数依赖和上下文复杂度显著增加了检索难度。
- 论文明确声称，在 **identifier anonymization** 以及编译到 **Assembly / Wasm** 后，六个 SOTA 模型的检索效果都出现**显著下降**；给定摘录未提供这些鲁棒性设置下的完整数值表，但作者的核心结论是：当前模型仍然**严重依赖词汇特征，而非稳健的代码语义理解**。

## Link
- [http://arxiv.org/abs/2603.04484v1](http://arxiv.org/abs/2603.04484v1)
