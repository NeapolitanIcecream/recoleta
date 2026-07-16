---
kind: trend
trend_doc_id: 1791
granularity: day
period_start: '2026-07-07T00:00:00'
period_end: '2026-07-08T00:00:00'
topics:
- coding agents
- software verification
- agentic code review
- trajectory diagnostics
- agent reliability
- developer learning
run_id: materialize-outputs
aliases:
- recoleta-trend-1791
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-verification
- topic/agentic-code-review
- topic/trajectory-diagnostics
- topic/agent-reliability
- topic/developer-learning
language_code: zh-CN
---

# 代码代理需要验证器、审查器和基于轨迹的修复

## 概览
当天的研究将代码代理视为需要在工作过程中接受外部检查的系统。Aria 展示了大规模的验证器门控证明搜索；SWE-Review 加入了面向代码库的审查；TraceProbe 衡量一次运行如何搜索、编辑和验证。当前重点是工作流中的可靠性证据，最终任务分数只是多个信号之一。

## 研究发现

### 验证器门控的编码与证明生成
Aria 是本时段最突出的成果。一个通用代码代理编写 Coq 和 Lean 证明，同时由测试框架拒绝不健全的输出、被修改的引理、被遗漏的义务、发散的策略和不安全的捷径。论文报告称，所有目标证明集都实现了完整覆盖：4,257 个 Iris 核心引理、217 个基于 Iris 构建的 Rust 库引理、318 个 reglang 定理，以及 72 个 Lean 移植引理。

SCOPE 将类似的控制模式应用于普通代码生成。一个经过证明器初始化的批评器识别草稿程序中缺失的语义义务，然后编码器针对这些子目标进行修改。在 LiveCodeBench V6 上，pass@1 达到 39.4%，高于 Reflexion 的 36.6% 和仅使用编码器生成的 20.6%。在具有可明确表述为子目标的具体约束的任务上，提升最明显。

### 面向代码库的审查与运行诊断
SWE-Review 将代码审查纳入代理循环。审查器可以检查代码库、运行命令、批准修改或要求修改，并提供修复指导。在 SWE-bench Verified 上，迭代式的生成、审查和修改将 Qwen3-30B-A3B PR 的解决率提高到 56.9%，而不进行审查时的基线为 27.5%。对于 Qwen3-Coder-30B-A3B，同一循环达到 68.8%，而基线为 50.9%。

TraceProbe 为代码代理评估加入过程证据。它将原始轨迹转换为九种行动类型，并标注 failed、reverted、off-anchor 或 justified 等影响。在一个 SWE-Bench 示例中，两个代理都完成了任务，但其中一个用 10 步完成且没有失败行动，另一个则需要 49 步，并反复经历恢复过程。这一区别会影响成本、审查负担和生产环境中的可信度。

### 代理基础设施测试与运行时修复
LogicHunter 针对 LangChain、LlamaIndex 和 CrewAI 等代理库中的故障。它根据源代码、类型提示、模式、文档和代码库用法构建可执行的种子测试，然后将有效的 API 调用变异为行为探针。其代理判定器会检查文档、源代码、复现脚本和运行时状态，再为故障分类。该研究报告发现了 40 个此前未知的 bug，其中 30 个得到确认，26 个已由开发者修复。

AgentTether 处理使用工具的代理运行结束后出现的故障。它将一条轨迹转换为相互关联的转移单元，定位可疑的子轨迹，并将修复指导带入下一次尝试。在使用 Qwen3.7-max 完成的 261 个 τ-bench 任务中，它修复了最初失败任务的 69.11%，整体比盲目重试高出 26.02 个百分点。

### IDE 内的开发者技能支持
代理编码中与人相关的部分体现在两个以 IDE 为中心的系统中。Prompt Coach 通过评分和结合本地项目的苏格拉底式提问，训练开发者编写更好的代码生成提示词。在一项包含 15 名开发者的研究中，一次 60 分钟的学习使提示词质量平均得分从基线的 63.04 提高到 71.69。测得的最大提升出现在约束、错误处理和上下文意识方面。

SHIELD 的证据还不充分，但目标很明确。它监控代理的代码修改和推理轨迹，然后将选定的概念转化为探针、短课和理解检查。论文报告了一个可运行的 VSCode 原型和一个支付 webhook 演示，但没有用户研究结果或基准测试分数。
