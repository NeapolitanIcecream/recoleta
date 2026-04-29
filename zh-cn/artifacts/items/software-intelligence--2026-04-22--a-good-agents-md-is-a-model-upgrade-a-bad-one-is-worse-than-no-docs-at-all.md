---
source: hn
url: https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files
published_at: '2026-04-22T23:23:56'
authors:
- knes
topics:
- agents-md
- code-generation
- developer-documentation
- software-engineering-agents
- evaluation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# A good AGENTS.md is a model upgrade. A bad one is worse than no docs at all

## Summary
## 概要
这篇文章报告了一项内部研究，分析 `AGENTS.md` 文件如何改变编码代理在真实软件任务中的表现。好的文件带来的提升，作者将其比作从 Haiku 升级到 Opus；差的文件则会让结果比没有 `AGENTS.md` 还差。

## 问题
- 编码代理通常会读取本地文档，但团队并不清楚哪些 `AGENTS.md` 写法有助于完成任务，哪些写法会把代理带进无关文档、额外检查和不完整的代码。
- 同一份文档可能对一个任务有帮助，却对另一个任务有害。在同一模块中，一份文件让一次 bug 修复任务的 `best_practices` 提高了 25%，却让一次功能任务的 `completeness` 降低了 30%。
- 这很重要，因为 `AGENTS.md` 是少数几种几乎一定会被代理执行框架发现的文档位置之一，所以错误的指引会直接降低代码质量和开发速度。

## 方法
- 作者使用了 AuggieBench，这是一个基于大型 monorepo 中真实已合并 PR 构建的内部评测套件。对每个任务，代理都要复现对应工作，再将输出与经过评审的“golden PR”对比评分。
- 他们把范围筛到单模块或单应用的 PR，并且这些任务中 `AGENTS.md` 有合理可能提供帮助；随后每个任务都运行两次：一次带文件，一次不带文件。
- 他们追踪了代理在数百次会话中实际发现了哪些文档，包括 `AGENTS.md`、其引用的文档、目录 `README.md`、嵌套的 `README`，以及孤立文档。
- 他们比较了多种文档模式，例如简洁的主文件、流程性工作流、决策表、代码示例、领域规则，以及以警告为主或以架构说明为主的文档。

## 结果
- 表现最好的 `AGENTS.md` 大约为 100–150 行，外加少量聚焦的引用文档。在大约有 100 个核心文件的中等规模模块中，这类文件在各项指标上带来了 10–15% 的提升。
- 一个用于添加新集成的六步工作流，将缺少连接文件的 PR 比例从 40% 降到 10%，`correctness` 提高了 25%，`completeness` 提高了 20%。
- 在文中提到的状态管理例子里，用于在相似模式之间做选择的决策表使 `best_practices` 提高了 25%。
- 当文件包含 `createSlice`、`createAsyncThunk` 和类型化 selector 用法等模板时，小型真实代码示例让 `code_reuse` 提高了 20%。
- 失败模式的影响很大：偏重架构说明的文档让某个任务加载了大约 80K 个无关 token，读取了 12 份文档，并损失了 25% 的 `completeness`；一份包含 30 多条纯警告规则的文件让 PR 耗时变成 2 倍，并使 `completeness` 降低了 20%。
- 文档发现率并不均衡：`AGENTS.md` 在 100% 的情况下都会被自动发现；有需要时，被引用文档在 90%+ 的会话中会被读取；目录 `README.md` 为 80%+；嵌套 `README` 约为 40%；而孤立的 `_docs/` 内容在不到 10% 的会话中被读取。

## Problem

## Approach

## Results

## Link
- [https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files](https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files)
