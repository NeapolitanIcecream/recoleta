---
source: arxiv
url: http://arxiv.org/abs/2603.07326v1
published_at: '2026-03-07T20:11:30'
authors:
- Zhiwei Fei
- Yue Pan
- Federica Sarro
- Jidong Ge
- Marc Liu
- Vincent Ng
- He Ye
topics:
- issue-reproduction
- test-generation
- code-retrieval
- execution-feedback
- code-graph
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Echo: Graph-Enhanced Retrieval and Execution Feedback for Issue Reproduction Test Generation

## Summary
Echo 是一个面向软件 issue 的自动复现测试生成代理，重点解决“如何找到对的代码上下文、真正跑起来测试、并可靠判断是否复现成功”的问题。它把代码图检索、自动执行、以及基于补丁版本的 fail-to-pass 校验结合起来，在 SWT-Bench Verified 上报告了新的开源 SOTA。

## Problem
- 许多 bug 报告没有可执行的复现测试，开发者需要手动理解代码库、补全环境与测试框架细节，成本高且耗时。
- 现有方法常依赖较弱的文件级检索或预设执行命令，难以在真实仓库中准确找到相关代码/测试，也难以稳定执行生成的测试。
- 仅凭 LLM 语义判断测试是否“真的复现了问题”不可靠；更关键的标准是测试在 buggy 版本失败、在 patched 版本通过（fail-to-pass）。

## Approach
- 将仓库构造成异构代码图（文件、AST 节点、文本片段及其关系），并基于 Neo4j 做多策略检索，以获取 focal code 和相关回归测试。
- 引入自动 query refinement：LLM 先评估当前检索结果是否足够，再针对缺失信息迭代改写查询，从而提高上下文的精确性与紧凑性。
- 生成测试时，把 issue 描述、检索到的 focal code、相关测试示例和候选补丁一起喂给 LLM，要求产出一个独立、最小化、符合项目风格的单个复现测试文件。
- 自动推断并执行该测试的仓库特定命令，但严格限制为只读、只运行生成的测试文件、不修改仓库、不跑全量测试，以获得可用执行反馈。
- 使用候选补丁构造 patched 版本，做规则化 dual-version check：若测试在原始版本失败且在补丁版本通过，则视为成功；否则把日志反馈给生成器继续迭代，最多重试两次。

## Results
- 在 **SWT-Bench Verified** 上，Echo 报告 **66.28% success rate**，论文称其为**开源方法中的新 SOTA**。
- 相比很多先生成并排序多个候选测试的方法，Echo 选择**每个 issue 只重点生成 1 个测试并迭代改进**，主张具有更好的**cost-performance trade-off**。
- 论文明确声称其自动执行生成测试是 **first-of-its-kind feature**，强调该能力更贴近真实开发工作流。
- 文本中给出的核心量化结果主要是 **66.28%**；当前摘录未提供更细的 baseline 对比数字、消融提升幅度或成本数值。

## Link
- [http://arxiv.org/abs/2603.07326v1](http://arxiv.org/abs/2603.07326v1)
