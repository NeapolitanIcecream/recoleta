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
- build-aware-compilation
- self-evolving-system
relevance_score: 0.02
run_id: materialize-outputs
---

# His2Trans: A Skeleton First Framework for Self Evolving C to Rust Translation with Historical Retrieval

## Summary
His2Trans 是一个面向工业级 C→Rust 迁移的框架，试图解决大项目翻译中缺失构建上下文和缺少历史迁移知识的问题。它把“先搭可编译骨架”与“从历史迁移中检索规则”结合起来，以提升编译稳定性、Rust 习惯用法复用和持续演化能力。

## Problem
- 现有 C→Rust 自动迁移在大型工程中常因**缺少真实构建上下文**而陷入“dependency hell”，LLM 容易臆造类型、依赖和接口，导致无法编译。
- 仅靠通用 LLM 很难推断**项目私有 API 与领域特定迁移习惯**，因此在渐进式迁移中无法可靠复用历史上已经迁移过的 Rust 接口。
- 错误依赖会引发**级联修复循环**，使项目级自动迁移成本失控；这很重要，因为 C 的内存安全问题占大量安全漏洞，而 Rust 迁移正成为工业趋势。

## Approach
- 先通过**build tracing**恢复真实编译环境，构造一个项目级、严格类型一致、可编译的 **Project-Level Skeleton Graph**，把类型定义、全局变量、函数签名和跨模块引用先固定下来。
- 再将函数体生成与结构验证解耦：先保留 `unimplemented!` 的骨架，通过**拓扑调度**按依赖顺序逐步填充函数体，减少级联错误。
- 从历史 C/Rust 共演化仓库中进行**粗到细的配对与对齐**：文件级候选检索、函数级重排，然后挖掘两类规则：**API-level rules** 和 **fragment-level rules**。
- 在生成每个函数时，用 **RAG** 检索相关历史规则，把“骨架提供的严格编译上下文”与“历史迁移规则”一起喂给 LLM，引导其复用更符合项目习惯的 Rust 接口与代码片段。
- 若生成结果编译失败，则采用**编译器反馈闭环修复**：先规则修复，再 LLM 修复；已验证成功的翻译样本继续回流知识库，实现自演化。

## Results
- 在工业 OpenHarmony 模块上，His2Trans 声称达到 **99.75% incremental compilation pass rate**，并指出基线方法常因缺失构建上下文而失败。
- 在通用基准上，相比 **C2Rust**，其 **unsafe code ratio 降低 23.6 个百分点**，同时产生**最少的 warnings**。
- 知识积累实验显示：通过持续整合已验证的迁移模式，在**未见任务**上可将**修复开销降低约 60%**，支持其“自演化”主张。
- 评测覆盖 **5 个 OpenHarmony 工业子模块**与 **10 个通用 C 项目**；文中给出数据集规模，但当前摘录未提供每个基线在所有指标上的完整逐项数字表。
- 实验采用**零人工干预**设置：所有翻译、修复与结果统计均由框架自动完成，无人工后编辑或挑选结果。

## Link
- [http://arxiv.org/abs/2603.02617v1](http://arxiv.org/abs/2603.02617v1)
