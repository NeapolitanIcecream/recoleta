---
kind: ideas
granularity: day
period_start: '2026-07-07T00:00:00'
period_end: '2026-07-08T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software verification
- agentic code review
- trajectory diagnostics
- agent reliability
- developer learning
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-verification
- topic/agentic-code-review
- topic/trajectory-diagnostics
- topic/agent-reliability
- topic/developer-learning
language_code: zh-CN
---

# 编码智能体信任控制

## 摘要
编码智能体的采用正在转向在工作循环中加入外部检查：在 AI 拉取请求继续推进前进行代码仓库感知审查，用轨迹诊断判断哪些智能体运行值得信任，并为智能体系统依赖的 Python 库增加规范感知测试。

## 面向 AI 生成拉取请求的代码仓库感知审查循环
接收 AI 生成拉取请求的团队，可以增加一轮自动化审查，并要求它满足与人工审查者相同的最低证据标准：检查代码仓库、运行命令、决定批准或要求修改，并给出具体的修复指导。SWE-Review 为这种工作流提供了可行的形式。它的审查者接收代码仓库检出内容、问题描述和 AI 生成的 PR，然后给出合并决定以及修改诊断。

实际要处理的是这样一种 PR：差异内容看起来合理，但问题仍未在代码库的其他位置得到解决。在 SWE-Review 中，迭代式的生成、审查、修改流程将 Qwen3-30B-A3B PR 的 SWE-bench Verified 解决率从 27.5% 提高到 56.9%，将 Qwen3-Coder-30B-A3B PR 的解决率从 50.9% 提高到 68.8%。一项成本较低的内部测试可以在最近 50 个需要人工返工的 AI PR 上运行这一循环，然后比较三个数字：正确拒绝率、被接受的不良 PR 数量，以及审查后修复率。

### 资料来源
- Document 1788: SWE-Review 定义了了解代码仓库的审查者、批准或要求修改的输出、审查指导下的修改循环，以及报告的解决率提升。
- Document 1788: 论文介绍了基准测试设置、审查者输出，以及修改后的完成率、决策准确率和解决率指标。

## 用于编码智能体发布评估的轨迹诊断
智能体团队应在最终通过或失败的结果之外，结合轨迹证据评估编码智能体。TraceProbe 展示了一条具体的实现路径：将每次运行转换为规范化的操作类型，例如读取文件、写入文件、搜索、命令、规划和推理，然后附加失败、回退、合理和偏离锚点等效果标签。

这有助于处理一个常见的发布问题：两个智能体可能解决同一个问题，却带来截然不同的审查负担。在 TraceProbe 的 SWE-Bench pytest-7982 示例中，使用 Opus 4.6 的 Claude Code 用 10 个步骤解决了任务，且没有失败操作；使用 GLM-5 的 OpenCode 也解决了任务，但用了 49 个步骤，并反复出现失败和恢复片段。一项可行的采用检查是：对已接受的智能体补丁运行这种轨迹规范化流程，并在将这些运行作为正面示例使用前，把包含搜索循环、跳过验证、无依据完成声明或大段恢复过程的运行标记出来，交由人工审查。

### 资料来源
- Document 1785: TraceProbe 的摘要列出了九种操作类型、确定性的效果标签、反模式检查，以及在 2,500 条 SWE-Bench Verified 轨迹上进行的评估。
- Document 1785: 论文中的示例比较了两次成功运行，它们的步骤数和恢复行为差异很大。

## 面向智能体框架升级的规范感知回归测试
使用 LangChain、LlamaIndex、CrewAI 或类似库构建系统的团队，可以在将框架版本投入生产前，增加升级测试，生成有效但处于边界条件下的 API 调用。LogicHunter 提供了一种具体做法：从源代码、类型提示、Pydantic 模式、文档和代码仓库用法中提取信息，创建可执行的种子测试，再将有效调用变异为行为探针，以检查字段保留、幂等性、边界行为和返回类型一致性。

运行中的难点是失败分诊噪声很大。在智能体库中，ValueError 或 KeyError 可能表示正确拒绝、调用方误用或库缺陷；错误行为也可能静默发生，不抛出任何异常。LogicHunter 的 Agentic Oracle 会检查文档、源代码、复现脚本和运行时状态，然后再给异常标注。该研究在 LangChain、LlamaIndex 和 CrewAI 中发现了 40 个此前未知的错误，其中 30 个得到确认，26 个得到修复。这套流程的简化版本可以从每晚运行开始，覆盖少量涉及工具、记忆、回调和异步执行的框架 API。

### 资料来源
- Document 1784: LogicHunter 的摘要介绍了有效种子的生成、行为探针、Agentic Oracle，以及在 LangChain、LlamaIndex 和 CrewAI 中确认的错误结果。
- Document 1784: 论文解释了普通异常和静默语义错误为何会给纯 Python 智能体框架带来预言机问题。
