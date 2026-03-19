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
- c-cpp
- benchmark
- retrieval-robustness
- semantic-retrieval
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# CLARC: C/C++ Benchmark for Robust Code Search

## Summary
CLARC 是一个面向 C/C++ 代码检索的鲁棒性基准，强调真实仓库、可编译代码和去除词法线索后的稳健评测。论文表明当前主流检索模型在匿名化标识符和低级表示下会明显退化，说明它们仍严重依赖表面词法特征。

## Problem
- 现有代码搜索基准大多偏向 Python，较少覆盖真实世界 C/C++ 检索场景，导致系统编程语言上的评测缺口明显。
- 许多数据集缺少完整依赖与可编译上下文，无法真实衡量模型是否理解代码功能及其上下文需求。
- 现有评测很少系统测试变量重命名、标识符匿名化、Assembly/Wasm 等扰动，因此高分可能只是来自词法匹配，而非语义理解；这对代码搜索、RAG 和开发者生产力都很重要。

## Approach
- 构建自动化数据管线：从 144 个热门 GitHub C/C++ 仓库挖掘函数，保留可编译样本，并抽取完整依赖上下文；最终得到 6,717 对 query-code，其中训练集 5,472、评测集 1,245。
- 按依赖复杂度将样本分为三组：仅依赖标准库、依赖自定义类型、依赖用户自定义 helper function；其中 Group 3 还区分 short/long 上下文形式。
- 用 LLM 生成自然语言查询，并通过双盲人工评分、bootstrap 假设检验和一致性分析验证其质量是否可比或优于人工描述。
- 设计多种鲁棒性设置来剥离词法线索：Neutralized、Randomized、Assembly、WebAssembly，以测试模型是否真正依赖代码语义进行检索。
- 在基准上评测 6 个检索模型，包括 BM25、CodeT5+、OASIS、Nomic-emb-code、OpenAI-text-embedding-large 和 Voyage-code-3。

## Results
- 数据规模与统计：CLARC 含 6,717 对样本，其中评测集 1,245、训练集 5,472；评测集平均 query 长度 84.8 tokens，原始代码平均 244.2 tokens、24.8 LOC、圈复杂度 3.4。
- LLM 查询质量验证：在 125 个样本/组的双盲评测中，Group 2 与 Group 3 的 LLM 描述接近或优于人工（Group 2: LLM 76.5 vs Human 72.0，p=76.32%；Group 3: 75.5 vs 71.5，p=84.92%）；Group 1 更高（86.0 vs 60.0，p=99.99%）。Krippendorff’s α 为 65.51–74.77，说明标注一致性可接受。
- 标准设置下，最佳模型在简单/中等依赖样本上已很强：Group 1 中 OASIS 的 NDCG 89.08、MRR 86.54、R@1 79.85，高于 BM25 的 NDCG 10.50；Group 2 中 Voyage 的 NDCG 94.06、MRR 92.10、R@1 85.93，Nomic 也达到 NDCG 93.61。
- 更复杂的 Group 3 Short 明显更难：最佳 Voyage 仅 NDCG 66.66、MAP 50.93、R@1 27.28；Nomic 为 NDCG 65.39、R@1 25.33；BM25 只有 NDCG 10.50、R@1 2.35，表明辅助函数依赖显著增加检索难度。
- 论文的核心结论是：在标识符匿名化、随机化及编译到 Assembly/Wasm 后，六个 SOTA 模型的检索效果都会“显著下降”；给定摘录未提供这些设置下的完整数值表，但作者明确将其解释为当前模型仍主要依赖词法特征，而非稳健的代码语义理解。
- 作者还声称，即使做常规监督微调，标准设置与匿名化设置之间的性能鸿沟依然存在，说明朴素微调不足以解决鲁棒性问题；摘录中未给出对应具体数值。

## Link
- [http://arxiv.org/abs/2603.04484v1](http://arxiv.org/abs/2603.04484v1)
