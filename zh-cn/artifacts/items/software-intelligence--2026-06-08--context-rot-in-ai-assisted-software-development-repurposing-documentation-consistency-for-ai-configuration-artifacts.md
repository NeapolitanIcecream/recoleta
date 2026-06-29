---
source: arxiv
url: https://arxiv.org/abs/2606.09090v1
published_at: '2026-06-08T06:36:38'
authors:
- Christoph Treude
- Sebastian Baltes
topics:
- ai-coding-assistants
- context-files
- documentation-consistency
- code-intelligence
- software-maintenance
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Context Rot in AI-Assisted Software Development: Repurposing Documentation Consistency for AI Configuration Artifacts

## Summary
## 摘要
本文定义了 context rot：AI 编程助手配置文件过时，和仓库当前状态不一致。它表明，现有的文档一致性检查可以发现指向已删除或已重命名代码元素的引用。

## 问题
- AI 编程助手会读取持续存在的项目文件，例如 `CLAUDE.md`、`AGENTS.md`、`.cursorrules`、`copilot-instructions.md` 和 `GEMINI.md`；其中的过时内容会让助手导入已删除的模块、调用不存在的函数，或遵循已经废弃的约定。
- 这些文件的变化不在编译器和测试反馈回路之内，所以漂移可能一直存在，却不会触发可见的失败。
- 这个问题很重要，因为论文引用的前人研究把 `AGENTS.md` 文件和更低的 agent 运行时与 token 使用量联系起来，所以不准确的配置会降低 AI 辅助开发的质量和效率。

## 方法
- 论文把这种失效模式命名为 context rot：AI 配置工件与当前代码库、工具、架构或工作流之间的不一致。
- 它直接复用了 DOCER，一个用于 README/wiki 一致性检查的工具，没有针对 AI 配置文件做调参。
- DOCER 会从当前配置文件中提取候选代码元素，检查这些元素在该文件首次提交时是否存在，再检查它们在仓库 HEAD 版本中是否还存在。
- 在首次提交时存在、但在 HEAD 中不存在的元素会被归类为过时；同时不在两个快照中的元素会被当作噪声丢弃。
- 研究重点是引用性漂移，并把其他文档一致性方法映射为未来对行为指令、MCP 工具描述、架构声明和依赖引用的检查。

## 结果
- 样本覆盖 356 个仓库和 612 个 AI 配置文件，来自 4,420 个仓库中的 8,213 个符合条件的文件；样本在仓库层面以 95% 置信度和 5% 误差范围为目标。
- DOCER 提取了 29,454 个候选元素，并验证了 18,048 个在配置文件首次提交时存在的引用。
- 它发现了 230 个过时引用，占已验证引用的 1.27%；17,818 个引用，即 98.73%，在 HEAD 版本中仍然有效。
- 在仓库层面，356 个仓库中有 82 个至少包含一个过时引用，占 23.0%，95% 置信区间为 18.8–27.2%。
- 对 50 条过时分类的人工检查发现 32 条是真实案例，占 64%；12 条是假阳性，6 条有歧义。
- 各文件类型的过时率分别为：`CLAUDE.md` 1.42%，`AGENTS.md` 1.04%，Copilot 指令文件 1.42%，`GEMINI.md` 0.75%，`.cursorrules` 0.00%，其他文件 2.99%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09090v1](https://arxiv.org/abs/2606.09090v1)
