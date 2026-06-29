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
本文报告了一项内部研究，考察 `AGENTS.md` 文件如何改变编码代理在真实软件任务上的表现。好的文件带来的输出提升，作者把它比作从 Haiku 升级到 Opus；坏的文件会让结果比没有 `AGENTS.md` 还差。

## Problem
- 编码代理经常读取本地文档，但团队并不清楚哪些 `AGENTS.md` 模式能帮助任务完成，哪些模式会把代理引向无关文档、额外检查和不完整代码。
- 同一个文档会对不同任务产生相反效果。在同一个模块里，一个文件让 `best_practices` 在一次修复 bug 的任务中提升了 25%，却让一次功能任务的 `completeness` 下降了 30%。
- 这很重要，因为 `AGENTS.md` 是少数几个几乎一定会被代理执行环境发现的文档位置之一，所以错误的指引会直接拉低代码质量和速度。

## Approach
- 作者使用了 AuggieBench，这是一个由大型 monorepo 中真实合并的 PR 构成的内部评估套件。对每个任务，都会让代理复现同样的工作，并把输出和经过审核的“golden PR”打分比较。
- 他们筛选出单模块或单应用的 PR，并要求 `AGENTS.md` 有可能提供帮助，然后把每个任务跑两次：一次有文件，一次没有文件。
- 他们追踪了在数百次会话中代理实际发现了哪些文档，包括 `AGENTS.md`、被引用的文档、目录 `README.md`、嵌套的 `README` 和孤立文档。
- 他们比较了多种文档模式，例如简洁的主文件、流程化工作流、决策表、代码示例、领域规则，以及警告很多或架构内容很多的文档。

## Results
- 表现最好的 `AGENTS.md` 文件大约有 100–150 行，再加少量重点引用文档。在大约 100 个核心文件的中等规模模块里，它们让各项指标提升了 10–15%。
- 一个用于新增集成的六步工作流，把缺少连接文件的 PR 比例从 40% 降到 10%，把 `correctness` 提高了 25%，把 `completeness` 提高了 20%。
- 一个在相似模式之间做选择的决策表，在文中提到的状态管理示例里把 `best_practices` 提高了 25%。
- 小型、真实代码示例让 `code_reuse` 提高了 20%，前提是文件里包含了 `createSlice`、`createAsyncThunk` 和类型化 selector 用法等模板。
- 失败模式幅度很大：偏架构的文档让一个任务加载了约 8 万个无关 token，读了 12 份文档，`completeness` 下降了 25%；一份包含 30 多条仅警告规则的文件让 PR 耗时变成 2 倍，并把 `completeness` 降低了 20%。
- 发现率差异很大：`AGENTS.md` 在 100% 的情况下会被自动发现；需要时，引用文档在 90% 以上的会话中被读取，目录 `README.md` 在 80% 以上，嵌套 `README` 约 40%，而孤立的 `_docs/` 内容在少于 10% 的会话中被读到。

## Link
- [https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files](https://www.augmentcode.com/blog/how-to-write-good-agents-dot-md-files)
