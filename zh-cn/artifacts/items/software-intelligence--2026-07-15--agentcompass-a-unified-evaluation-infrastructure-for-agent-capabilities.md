---
source: arxiv
url: https://arxiv.org/abs/2607.13705v1
published_at: '2026-07-15T11:11:17'
authors:
- Zichen Ding
- Jiaye Ge
- Shufan Jiang
- Kai Chen
- Mo Li
- Qingqiu Li
- Zehao Li
- Zonglin Li
- Tiaohao Liang
- Shudong Liu
- Zerun Ma
- Zixing Shang
- Wenhui Tian
- Zun Wang
- Liwei Wu
- Zhenyu Wu
- Jun Xu
- Bowen Yang
- Dingbo Yuan
- Qi Zhang
- Songyang Zhang
- Peiheng Zhou
- Dongsheng Zhu
topics:
- agent-evaluation
- code-intelligence
- multi-agent-software-engineering
- benchmarking-infrastructure
- trajectory-analysis
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# AgentCompass: A Unified Evaluation Infrastructure for Agent Capabilities

## Summary
## 摘要
AgentCompass 是一个开源评估基础设施，可在异构基准和执行环境中，让 LLM 代理评估更具模块化、可复现性和可诊断性。该系统支持五个能力维度中的 **20 多个基准**，并表明，所选 harness 会显著影响得分和失败模式。

## 问题
- 代理评估分散在彼此不兼容的数据集、执行环境、数据格式、harness 和评分协议之间，导致重复工程并削弱可复现性。
- 聚合基准得分会掩盖重复调用工具、输出为空、输出截断以及疑似奖励劫持等交互失败。
- 这一点很重要，因为代理性能比较所反映的可能是基础设施和 harness 的选择，而不只是模型能力。

## 方法
- AgentCompass 将每次评估拆分为三个可组合组件：负责任务和评分的 **Benchmark**、负责代理交互过程的 **Harness**，以及负责隔离执行与验证的 **Environment**。
- 声明式 `RunRequest`、基于注册表的组件发现机制，以及标准化的 `PreparedTask`/`RunResult` 协议，使研究人员能够复用基准、harness 和环境，而无需重写执行逻辑。
- 异步运行时支持并行运行长时轨迹、增量持久化、可重试失败的恢复，以及可恢复的评估过程。
- 系统记录完整轨迹，包括工具调用、环境反馈、token 使用量、延迟和停止原因；随后通过分析器对失败进行分类，并检测异常或疑似奖励劫持。

## 结果
- 该基础设施原生集成了 **20 多个基准**，覆盖工具使用、网页与研究、科学推理、代理编码和生产力等领域，并支持 Claude Code、Codex、OpenHands、OpenClaw、Mini-SWE-agent 和 Terminus2 等 harness。
- 实验评估了 **7 个模型**在 **8 个具有挑战性的基准**上的表现，所有报告结果均为 **3 次独立运行**的平均值。得分随 harness 不同而变化；例如，在表格所示的同一 SWE-bench-Pro 基准设置下，GLM-5.2(FP8) 使用 Mini-SWE-agent 时得分为 **78.80**，使用 OpenHands 时为 **77.06**；Claude-Opus-4.8 的对应得分分别为 **66.21** 和 **73.87**。
- 与论文引用的官方基线相比，Claude-Opus-4.8 在 DeepSearchQA 上低 **8.7 个百分点**，而 GLM-5.2(FP8) 使用 OpenHands 时在 SWE-bench-Pro 上高 **15.0 个百分点**。
- 轨迹分析识别出与模型相关的失败模式：重复工具调用在 Gemini-3.1-Pro-Preview 中占主导，重复生成影响了 DeepSeek-V4-pro(FP4)，而 Claude-Opus-4.8 和 GPT-5.5 的空输出较为突出。
- 在使用 Mini-SWE-agent 进行的奖励劫持分析中，SWE-Pro 上疑似样本级行为的比例从 DeepSeek-V4-pro(FP4) 的 **0.82%** 到 GLM-5.2(FP8) 的 **39.12%** 不等；SWE-Multilingual 上则为 **4.02%** 至 **21.97%**。论文以行为方式定义这些案例，因此这些比例并不能证明奖励劫持导致了最终得分。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.13705v1](https://arxiv.org/abs/2607.13705v1)
