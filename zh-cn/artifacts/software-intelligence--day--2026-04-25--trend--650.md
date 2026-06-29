---
kind: trend
trend_doc_id: 650
granularity: day
period_start: '2026-04-25T00:00:00'
period_end: '2026-04-26T00:00:00'
topics:
- agent-evaluation
- coding-agents
- benchmarks
- software-engineering
- repository-execution
run_id: materialize-outputs
aliases:
- recoleta-trend-650
tags:
- recoleta/trend
- topic/agent-evaluation
- topic/coding-agents
- topic/benchmarks
- topic/software-engineering
- topic/repository-execution
language_code: zh-CN
---

# 可执行证据正在抬高编码和代理研究的门槛

## Overview
4 月 25 日的编码研究，最强的地方在于主张能碰到可执行证据。Simulating and Evaluating Agentic Systems 和 CUJBench 都坚持用完整运行、工具轨迹、状态变化和可复现产物来评判代理。仓库工作仍然很难：RAT 改善了配置，但真实提交研究还是显示生成之后会出现编译、分析和测试失败。

## Clusters

### 评估正在从对话记录检查转向整轮运行证据
评估工作正在向完整代理行为靠近。最强的例子是一个面向 agentic systems 的 sim/eval 栈，它在一次运行中测试多步动作、工具使用、后端状态和用户可见结果。它把场景设计、模拟和评分分开，再记录世界状态、工具轨迹、对话记录和表层产物。CUJBench 把同样的证据要求用在故障诊断上。它把浏览器和后端证据冻结成可复现的事故快照，而当前代理的准确率仍只有 19.7%。共同的结论很直接：对于通过工具和状态变化来行动的系统，只看对话记录打分远远不够。

#### Evidence
- [Simulating and Evaluating Agentic Systems](../Inbox/2026-04-25--simulating-and-evaluating-agentic-systems.md): Sim/eval design for multi-step agent behavior, structured logs, and deterministic assertions.
- [CUJBench: Benchmarking LLM-Agent on Cross-Modal Failure Diagnosis from Browser to Backend](../Inbox/2026-04-25--cujbench-benchmarking-llm-agent-on-cross-modal-failure-diagnosis-from-browser-to-backend.md): Cross-modal benchmark with 87 scenarios and 19.7% accuracy shows diagnosis remains hard even with richer evidence.

### 代码代理正在按能否运行、构建并通过项目检查来评判
仓库级编码在基本软件关卡上仍然会失败。RAT 针对环境配置，这是代码代理连开始都开始不了的常见原因，并在它的 2000 多个仓库基准上报告了高得多的环境配置成功率，其中 Python 为 63.2%，Rust 为 98.7%。另一项对 8 个 C 项目中 212 个真实提交的研究说明了这件事在配置之后为什么仍然重要：生成的补丁还是会编译失败、触发静态分析、漏过测试，即使原始提交很小也是如此。这让执行、可构建性和仓库上下文继续处在编码代理研究的中心。

#### Evidence
- [I reverse-engineered Claude Desktop's storage to give it memory](../Inbox/2026-04-25--i-reverse-engineered-claude-desktop-s-storage-to-give-it-memory.md): Repository environment configuration benchmark and ESSR gains across languages.
- [Can LLMs be Effective Code Contributors? A Study on Open-source Projects](../Inbox/2026-04-25--can-llms-be-effective-code-contributors-a-study-on-open-source-projects.md): Real open-source commit study documents compile errors, static-analysis failures, and uneven project success.

### 受约束的代码任务正在带来更清晰的收益，而不是更宽泛的自主性
两篇论文把代码辅助推进到更窄、更具体的场景里。MOSAIC 处理没有测试用例时的科学工作流生成。它使用师生蒸馏和紧凑的共享上下文，然后在 GPT-4o、Claude Sonnet 4 和 Gemini 2.5 Flash 上都提升了 SciCode 结果。另一项研究询问小型本地模型离线时能为 Python 漏洞检测做什么。在 349 个 BugsInPy 案例上，LLaMA 3.2 和 Mistral 的完全准确率大约在 43% 到 45%，还有很多部分正确的回答能指出大致区域，但没能给出完整修复。实际模式是，在明确约束下提供定向帮助，而不是通用的自主编码。

#### Evidence
- [Knowledge Lever Risk Management for Software Engineering: A Stochastic Framework for Mitigating Knowledge Loss](../Inbox/2026-04-25--knowledge-lever-risk-management-for-software-engineering-a-stochastic-framework-for-mitigating-knowledge-loss.md): Scientific code generation without test cases, with measured gains on SciCode.
- [An Empirical Evaluation of Locally Deployed LLMs for Bug Detection in Python Code](../Inbox/2026-04-25--an-empirical-evaluation-of-locally-deployed-llms-for-bug-detection-in-python-code.md): Offline bug detection results on BugsInPy with exact and partial accuracy breakdowns.
