---
kind: trend
trend_doc_id: 1537
granularity: day
period_start: '2026-06-16T00:00:00'
period_end: '2026-06-17T00:00:00'
topics:
- "AI \u7F16\u7A0B\u667A\u80FD\u4F53"
- "\u8F6F\u4EF6\u5DE5\u7A0B\u8BC4\u4F30"
- "\u7A0B\u5E8F\u4FEE\u590D"
- "\u6D4B\u8BD5\u9884\u8A00\u673A"
- "\u667A\u80FD\u4F53\u8FD0\u884C\u6846\u67B6"
- "\u9AD8\u6548\u63A8\u7406"
run_id: materialize-outputs
aliases:
- recoleta-trend-1537
tags:
- recoleta/trend
- "topic/ai-\u7F16\u7A0B\u667A\u80FD\u4F53"
- "topic/\u8F6F\u4EF6\u5DE5\u7A0B\u8BC4\u4F30"
- "topic/\u7A0B\u5E8F\u4FEE\u590D"
- "topic/\u6D4B\u8BD5\u9884\u8A00\u673A"
- "topic/\u667A\u80FD\u4F53\u8FD0\u884C\u6846\u67B6"
- "topic/\u9AD8\u6548\u63A8\u7406"
language_code: zh-CN
---

# 编程智能体研究正转向证据、运行框架和有界计算

## Overview
当日研究把 AI 编程智能体视为需要运行时证据、有意义测试和关注运行框架评分的系统。PracRepair 和 LoopCoder-v2 显示，在仔细测量修复证据和潜在计算时可以获得增益；评估论文则推动报告组件级结果。

## Clusters

### 用于代码修复的运行时反馈
自动程序修复（APR）研究正在把执行证据作为一等输入。PracRepair 将静态代码上下文与失败测试轨迹、变量值、分支结果、验证诊断和轨迹差异结合起来。使用 GPT-4o 时，它报告在 Defects4J V1.2 上正确修复 162 个缺陷，在 V2.0 上正确修复 171 个缺陷，还包含许多 ReInFix 没有找到的修复。

另一项代码修正研究在更简单的循环中测试同一思路：生成代码，运行代码，返回编译器错误或失败测试细节，然后修改。GPT-o4-mini 在 450 题核心集上的 pass@1 领先；该研究还发现，语法和运行时失败比逻辑和算法错误更容易修复。

测试生成仍是弱点。在 86,156 个由智能体编写的测试文件补丁中，80.2% 包含弱预言机信号，或没有明确的预言机信号。这个发现很关键，因为测试文件可以执行代码，却仍然不检查任何预期行为。

#### Evidence
- [PracRepair: LLM-Empowered Automated Program Repair Inspired by Human-Like Debugging Practices](../Inbox/2026-06-16--pracrepair-llm-empowered-automated-program-repair-inspired-by-human-like-debugging-practices.md): PracRepair 方法和 Defects4J 修复数量。
- [Unlocking LLM Code Correction with Iterative Feedback Loops](../Inbox/2026-06-16--unlocking-llm-code-correction-with-iterative-feedback-loops.md): 迭代式代码修正设置、模型和 pass@1 结果。
- [All Smoke, No Alarm: Oracle Signals in Agent-Authored Test Code](../Inbox/2026-06-16--all-smoke-no-alarm-oracle-signals-in-agent-authored-test-code.md): 关于智能体编写测试中弱预言机信号的大规模证据。

### 关注运行框架的智能体评估
基准测试研究正在更谨慎地说明被测对象。一篇立场论文认为，编程智能体分数包含模型、运行框架、工具、环境、任务设置和验证器。论文引用的 Terminal-Bench 示例显示，固定使用 Claude Opus 4.6 时，ForgeCode 得分为 79.8% ± 1.6，Claude Code 得分为 58.0% ± 2.9，不同运行框架之间相差 21.8 分。

智能体技能评估论文把这一问题转化为测量流程。它根据每项技能生成任务和隐藏评分细则，在有无该技能的条件下运行智能体，并为指令遵循和目标完成打分。在约 500 项技能、1,000 个任务、19 种智能体-模型配置和 38,000 条有效轨迹中，相关技能带来的增益随模型而异，增加 5.5 到 22 分。

#### Evidence
- [Position: Coding Benchmarks Are Misaligned with Agentic Software Engineering](../Inbox/2026-06-16--position-coding-benchmarks-are-misaligned-with-agentic-software-engineering.md): 基准测试批评、运行框架组件和 Terminal-Bench 运行框架差异。
- [A Framework for Evaluating Agentic Skills at Scale](../Inbox/2026-06-16--a-framework-for-evaluating-agentic-skills-at-scale.md): 技能评估方法、规模和报告的分数增益。

### 代码模型和智能体的有界计算
LoopCoder-v2 为代码模型给出了具体的计算扩展结果。这个 7B Parallel Loop Transformer 在循环之间复用共享块，并用共享键值注意力降低缓存成本。在报告的测试套件中，两次循环把平均分从 38.0 提高到 46.5。在 SWE-bench Verified 上，分数从 43.0 升至 64.4，而三次和四次循环的分数大幅下降。

语料中的实践文章也把类似的有界系统视角用于智能体工作站。长时间运行的智能体需要隔离的计算机、独立端口、状态、依赖和 shell 访问。其实践主张是，质量取决于规格说明、测试、类型检查、lint、可观测性和最终 pull request 审查，而非人类持续编辑生成代码。

#### Evidence
- [LoopCoder-v2: Only Loop Once for Efficient Test-Time Computation Scaling](../Inbox/2026-06-16--loopcoder-v2-only-loop-once-for-efficient-test-time-computation-scaling.md): LoopCoder-v2 架构、训练设置和两次循环的基准增益。
- [What does software development look like when agents write 100% of the code?](../Inbox/2026-06-16--what-does-software-development-look-like-when-agents-write-100-of-the-code.md): 智能体隔离、长时间运行执行和验证工作流主张。
