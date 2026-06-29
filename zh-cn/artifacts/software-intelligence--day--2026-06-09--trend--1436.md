---
kind: trend
trend_doc_id: 1436
granularity: day
period_start: '2026-06-09T00:00:00'
period_end: '2026-06-10T00:00:00'
topics:
- coding agents
- software engineering
- multi-agent systems
- code security
- benchmarks
- test oracles
run_id: materialize-outputs
aliases:
- recoleta-trend-1436
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/multi-agent-systems
- topic/code-security
- topic/benchmarks
- topic/test-oracles
language_code: zh-CN
---

# 编码代理需要仓库级测试和上下文防护

## Overview
当天最强的信号是，围绕已经在处理多文件工作的编码代理，工程纪律开始变得更重要。DeNovoSWE、EsoLang-Bench 和 DeLM 都在测试代理能否构建完整仓库、通过执行进行适应，并且不浪费调用就共享已验证进展。安全论文给出明确警告：看起来正常的上下文，也能把生成或分析出来的代码带向不安全行为。

## Clusters

### Repository-scale coding benchmarks
DeNovoSWE 将整个代码仓库生成视为一个带可执行检查的训练问题。它的 4,818 个文档到仓库实例来自真实仓库，包含 Docker 环境、测试覆盖率筛选、沙箱清理，以及按能力级别编写的文档。用这个数据集对 Qwen3-30B-A3B 进行微调后，BeyondSWE-Doc2Repo 的表现从 5.8% 提升到 47.2%，这是一个幅度很大的提升，因为这项任务要求处理文件布局、API、依赖关系和组件间行为。

EsoLang-Bench 测的是另一种能力：在不熟悉的可执行接口里适应。最强的代理通常先写 Python、JavaScript 或 Rust 生成器来输出小众语言代码，再用本地解释器调试这些生成器。这个基准把已部署代理拉开了明显差距，六个代理的平均分差距达到 88.4 个百分点。这个结果让工具使用和本地执行在编码能力评测中有了明确位置。

#### Evidence
- [DeNovoSWE: Scaling Long-Horizon Environments for Generating Entire Repositories from Scratch](../Inbox/2026-06-09--denovoswe-scaling-long-horizon-environments-for-generating-entire-repositories-from-scratch.md): DeNovoSWE 数据集构建、规模，以及 BeyondSWE-Doc2Repo 的提升。
- [Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages](../Inbox/2026-06-09--frontier-coding-agents-use-metaprogramming-to-adapt-to-unfamiliar-programming-languages.md): EsoLang-Bench 设置、元编程机制，以及不同代理之间的分数差距。

### Shared state for multi-agent software work
DeLM 把协同变成评测的核心。代理认领排队中的子任务，读取共享的已验证上下文，并写回关于事实、失败尝试、约束和部分修复的简短更新。在 Gemini 3 Flash 上的 SWE-bench Verified 中，它报告的 Avg.@1 为 65.7%，每个任务成本 0.12 美元；强度最高的列出基线是 56.4% Avg.@1，而几种基线的成本大约是它的两倍。

MASTOR 把代理协同用在 REST API 测试上。它读取实现源码，记录端点约束和响应事实，然后生成状态、字段和跨操作的语义 oracle。在 13 个开源 RESTful API 项目上，它生成了 10,022 个 oracle，平均变异得分达到 75.4%。这里更有力的证据很实用：当代理输出绑定到源码证据，并经过复核步骤检查时，代理才真正有用。

#### Evidence
- [Decentralized Multi-Agent Systems with Shared Context](../Inbox/2026-06-09--decentralized-multi-agent-systems-with-shared-context.md): DeLM 共享已验证上下文、任务队列设计，以及 SWE-bench Verified 的准确率和成本。
- [MASTOR: A Multi-Agent Approach to Semantic Test Oracle Generation for RESTful APIs](../Inbox/2026-06-09--mastor-a-multi-agent-approach-to-semantic-test-oracle-generation-for-restful-apis.md): MASTOR 基于源码的 oracle 生成、基准规模、变异得分和成本。

### Context as a code security attack surface
两篇论文都把代码上下文本身当成了安全攻击面。对抗上下文研究表明，注释、文档、变量名和参考示例会在推理时把生成器引向有漏洞的代码。在 2,800 次试验中，对抗上下文把平均漏洞生成率从 3.5% 提高到 37.4%。靠近目标函数的上下文尤其有效：放在目标函数前 10 到 50 个 token 的提示，攻击成功率达到 62.1%。

自然后门论文增加了一个模型侧风险。它研究了 44 个场景下的 Code Language Models（CodeLMs），并报告说，正常训练的模型也可能包含类似触发器的代码特征，把输出推向目标标签。ScanNBT 通过触发器反演来寻找更多样的自然触发器。这里的数值细节少于对抗上下文研究，但它把问题从提示操纵扩展到了常规训练中学到的特征。

#### Evidence
- [Context-Based Adversarial Attacks on AI Code Generators: Vulnerability Analysis and Implications](../Inbox/2026-06-09--context-based-adversarial-attacks-on-ai-code-generators-vulnerability-analysis-and-implications.md): 受控的上下文对抗实验、漏洞生成率、迁移和检测器结果。
- [Securing Code Understanding: Detecting Natural Backdoor Vulnerability in Code Language Models](../Inbox/2026-06-09--securing-code-understanding-detecting-natural-backdoor-vulnerability-in-code-language-models.md): CodeLM 的自然后门范围、触发器反演方法，以及 ScanNBT 的检测主张。
