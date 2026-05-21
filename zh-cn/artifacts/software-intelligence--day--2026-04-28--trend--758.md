---
kind: trend
trend_doc_id: 758
granularity: day
period_start: '2026-04-28T00:00:00'
period_end: '2026-04-29T00:00:00'
topics:
- coding agents
- code editing
- agent harnesses
- software testing
- agent infrastructure
- model efficiency
run_id: materialize-outputs
aliases:
- recoleta-trend-758
tags:
- recoleta/trend
- topic/coding-agents
- topic/code-editing
- topic/agent-harnesses
- topic/software-testing
- topic/agent-infrastructure
- topic/model-efficiency
language_code: zh-CN
---

# 编码代理的进展来自模型周围的接口

## Overview
可执行评估仍是这一时期的基准。最强的主张来自模型外部组件：SWE-Edit 的读写拆分、Agentic Harness Engineering 的 rollout 驱动 harness 编辑，以及 SAFEdit 的测试支撑修复循环。这些工作把上下文、工具、存储、安全提醒和推理成本视为代理性能中可度量的部分。

## Clusters

### 代码编辑接口
当文件读取、补丁编写和修复被拆成更小的任务时，代码库代理的收益最大。SWE-Edit 使用 Viewer 返回相关代码块，并用 Editor 执行补丁，把探索性文件内容排除在主推理上下文之外。在 SWE-bench Verified 上，它报告修复率从 69.9% 提高到 72.0%，编辑成功率从 93.4% 提高到 96.9%，总推理成本下降 17.9%。

SAFEdit 把同样的拆分用于按指令进行的编辑。Planner 编写编辑计划，Editor 只修改目标代码，Verifier 运行真实单元测试，最多进行三轮修复。在 EditBench 上，它报告任务成功率为 68.6%，高于其 GPT-4.1 ReAct 基线的 60.0%。一份 Claude Code 回归报告展示了另一侧的运行风险：Read 和 Grep 结果中反复出现的恶意软件提醒，导致某个已报告工作流中的 5 个 Opus 4.7 子代理有 3 个拒绝执行普通重构任务。

#### Evidence
- [SWE-Edit: Rethinking Code Editing for Efficient SWE-Agent](../Inbox/2026-04-28--swe-edit-rethinking-code-editing-for-efficient-swe-agent.md): SWE-Edit 设计，以及 SWE-bench Verified 上的成本、编辑成功率和修复率结果。
- [SAFEdit: Does Multi-Agent Decomposition Resolve the Reliability Challenges of Instructed Code Editing?](../Inbox/2026-04-28--safedit-does-multi-agent-decomposition-resolve-the-reliability-challenges-of-instructed-code-editing.md): SAFEdit 的多代理编辑、验证循环和 EditBench 任务成功率结果。
- [Regression: malware reminder on every read still causes subagent refusals](../Inbox/2026-04-28--regression-malware-reminder-on-every-read-still-causes-subagent-refusals.md): Claude Code 回归报告显示，反复出现的系统提醒导致子代理拒绝任务并增加 token 开销。

### Harness 工程
编码模型周围的 harness 现在被当作一个可编辑系统，并有自己的度量。Agentic Harness Engineering (AHE) 将提示、工具、中间件、技能、子代理设置和记忆作为文件暴露出来。它使用清理后的 rollout 轨迹提出修改，记录预测收益和风险，然后在保留编辑前检查结果。经过 10 次迭代后，AHE 报告 Terminal-Bench 2 在 89 个任务上的 pass@1 从 69.7% 升至 77.0%。它的冻结 harness 在 SWE-bench-verified 上也比种子 harness 使用更少 token。

Mesa 和代理安全文章以产品形式处理同类问题，但度量较弱。Mesa 为代理提供持久的 POSIX 兼容文件系统，包含分支、diff、回滚、审计轨迹和有范围的挂载。安全文章通过 HTTP 代理注入凭据，把真实凭据留在 AI SRE 容器之外，并在应用忽略代理设置时考虑使用 gVisor 做网络拦截。

#### Evidence
- [Agentic Harness Engineering: Observability-Driven Automatic Evolution of Coding-Agent Harnesses](../Inbox/2026-04-28--agentic-harness-engineering-observability-driven-automatic-evolution-of-coding-agent-harnesses.md): AHE 组件、rollout 证据循环、Terminal-Bench 2 结果、迁移结果和 token 使用数据。
- [Mesa: A Versioned Filesystem for Agents](../Inbox/2026-04-28--mesa-a-versioned-filesystem-for-agents.md): Mesa 文件系统为持久、有权限、带版本的代理工作提供的功能。
- [Proxies, Sandboxes and Agent Security](../Inbox/2026-04-28--proxies-sandboxes-and-agent-security.md): 用于代理安全的凭据注入代理设计和沙箱观察。

### 来自未覆盖代码的 bug 报告
IssueSpecter 让大型语言模型 (LLM) 检查当前测试从未执行的代码，把自动化软件修复推进到更早的流程阶段。SlipCover 找出未覆盖的 Python 片段。GPT-5-mini 生成候选 issue 报告，包括严重性、复现步骤、受影响操作系统和建议修复。随后用排序步骤筛选出需要人工审查的问题。

报告规模已经足够有用，但仍有噪声。在 13 个活跃 Python 项目中，该系统生成了 10,467 份 issue 报告。人工审查 130 份排名靠前的报告后，发现 49 个有效 bug、61 个需要进一步调查的问题，以及 20 份无效报告。作者还报告，基于 LLM 的排序在 precision@3 上比基于规则的排序高 50%，平均倒数排名高 41%。

#### Evidence
- [LLM-Guided Issue Generation from Uncovered Code Segments](../Inbox/2026-04-28--llm-guided-issue-generation-from-uncovered-code-segments.md): IssueSpecter 流程、人工标注结果、排序收益和 bug 分类覆盖。

### 推理成本和可观测性
软件工程模型中的效率主张有具体数据。Carbon-Taxed Transformers (CTT) 面向代码模型，结合神经架构搜索、结构化剪枝、量化和蒸馏。它报告内存最多减少 49×，克隆检测延迟降低 8–10×，生成延迟降低 4–7×，推理 CO2 排放最多降低 81%。代码生成是最难的场景：pass@1 保留率最高达到 68%。

另一项可观测性综述认为，生产 LLM 系统需要把模型内部、置信度、行为、运行和基础设施追踪信号连接起来。它汇总了多项研究，证据不均衡，但运行层面的结论与代理论文一致：只有把模型行为与工具、轨迹和基础设施指标关联起来，失败和成本才可见。

#### Evidence
- [Carbon-Taxed Transformers: A Green Compression Pipeline for Overgrown Language Models](../Inbox/2026-04-28--carbon-taxed-transformers-a-green-compression-pipeline-for-overgrown-language-models.md): CTT 压缩方法，以及报告的内存、延迟、CO2 和任务保留结果。
- [AI Observability for Large Language Model Systems: A Multi-Layer Analysis of Monitoring Approaches from Confidence Calibration to Infrastructure Tracing](../Inbox/2026-04-28--ai-observability-for-large-language-model-systems-a-multi-layer-analysis-of-monitoring-approaches-from-confidence-calibration-to-infrastructure-tracing.md): 对 LLM 可观测性层、示例和跨层关联未解决问题的综述。
