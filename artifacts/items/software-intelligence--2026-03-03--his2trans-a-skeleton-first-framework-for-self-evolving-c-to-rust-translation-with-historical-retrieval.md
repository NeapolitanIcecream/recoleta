---
source: arxiv
url: http://arxiv.org/abs/2603.02617v1
published_at: '2026-03-03T05:42:08'
authors:
- Shengbo Wang
- Mingwei Liu
- Guangsheng Ou
- Yuwen Chen
- Zike Li
- Yanlin Wang
- Zibin Zheng
topics:
- c-to-rust
- code-translation
- retrieval-augmented-generation
- build-aware
- self-evolving
- code-migration
relevance_score: 0.96
run_id: materialize-outputs
---

# His2Trans: A Skeleton First Framework for Self Evolving C to Rust Translation with Historical Retrieval

## Summary
His2Trans 是一个面向工业级 C 到 Rust 迁移的框架，核心思想是先构建可编译、强类型的项目骨架，再结合历史迁移知识检索来逐步生成函数逻辑。它试图解决大项目迁移中的构建上下文缺失、领域 API 映射缺失和修复循环失控问题。

## Problem
- 现有 C→Rust 自动迁移方法在工业项目中常因 **build context 缺失** 而无法恢复精确类型与依赖，导致“dependency hell”和幻觉式依赖。
- 仅靠通用 LLM 很难推断 **领域特定 API 与历史演化模式**，因此无法复用已有 Rust 接口，容易生成不地道甚至无法集成的代码。
- 大项目通常需要 **渐进式迁移**，若每次修复都会引发级联编译错误，自动化成本会迅速失控；这很重要，因为 C 的内存安全问题被文中引用为约 **70% 安全漏洞** 的来源之一，而 Rust 迁移正是工业界的重要方向。

## Approach
- 先做 **build tracing**，从真实构建过程恢复宏、类型、条件编译和依赖，生成一个可编译的 **Project-Level Skeleton Graph**；简单说，就是先把整个 Rust 项目的“空架子”搭好，并确保类型是对的。
- 骨架中保留目录结构、模块关系、类型定义、全局状态和函数签名，函数体先用 `unimplemented!` 占位，把 **结构验证** 和 **逻辑生成** 分开。
- 再从历史 C/Rust 迁移仓库中自动挖掘 **API-level rules** 和 **fragment-level rules**，形成可累积的知识库；检索时用 BM25 + reranker + RAG，把相似历史样例喂给 LLM。
- 函数体翻译按依赖图 **自底向上拓扑调度**：先翻译依赖少的函数，再翻译上层函数；每步都用编译器反馈做规则修复或 LLM 修复，必要时回退到 C2Rust 的 unsafe 代码以保住可编译性。
- 已通过验证的翻译结果会重新写回知识库，形成 **self-evolving** 闭环，让后续未见任务更容易修复。

## Results
- 在工业级 **OpenHarmony** 模块上，His2Trans 报告 **99.75% incremental compilation pass rate**，并声称能修复基线方法因缺失构建上下文而失败的问题。
- 在通用基准上，相比 **C2Rust**，其 **unsafe code ratio 降低了 23.6 个百分点**，同时产生 **最少 warnings**。
- 在知识积累实验中，随着持续加入已验证迁移模式，未见任务的 **repair overhead 下降约 60%**，表明系统具有“越用越强”的演化能力。
- 评测覆盖 **5 个 OpenHarmony 子模块** 和 **10 个通用 C 项目**；文中还列出多种基线（如 C2Rust、PTRMAPPER、EvoC2Rust、Tymcrat 等），但摘录中未给出完整逐项对比表与全部数值明细。
- 实验设置强调 **zero-human-intervention**，即评测期间无人工后编辑或 cherry-picking。

## Link
- [http://arxiv.org/abs/2603.02617v1](http://arxiv.org/abs/2603.02617v1)
