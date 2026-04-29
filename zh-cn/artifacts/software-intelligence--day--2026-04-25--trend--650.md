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

# 可执行证据正在成为编码与智能体研究的门槛

## Overview
4 月 25 日的编码研究中，最有说服力的部分是主张能对上可执行证据。Simulating and Evaluating Agentic Systems 与 CUJBench 都坚持用完整运行、工具轨迹、状态变化和可复现产物来评判智能体。仓库级工作仍然很难：RAT 改善了环境配置，但真实提交研究仍然显示，生成之后依旧会出现编译、分析和测试失败。

## Clusters

### 评测正从转录检查转向完整运行证据
评测工作正在更接近智能体的完整行为。最典型的例子是一个面向 agentic systems 的 sim/eval 栈，它在一次运行中测试多步动作、工具使用、后端状态和用户可见结果。它把场景设计、模拟和评分分开，然后记录世界状态、工具轨迹、对话转录和界面产物。CUJBench 把同样对扎实证据的要求用于故障诊断。它把浏览器和后端证据冻结为可复现的事件快照，而当前智能体的准确率仍只有 19.7%。共同的结论很直接：对于通过工具和变化中的状态来执行动作的系统，只看转录评分太弱了。

#### Evidence
- [Simulating and Evaluating Agentic Systems](../Inbox/2026-04-25--simulating-and-evaluating-agentic-systems.md): 用于多步智能体行为的 sim/eval 设计、结构化日志和确定性断言。
- [CUJBench: Benchmarking LLM-Agent on Cross-Modal Failure Diagnosis from Browser to Backend](../Inbox/2026-04-25--cujbench-benchmarking-llm-agent-on-cross-modal-failure-diagnosis-from-browser-to-backend.md): 包含 87 个场景、准确率为 19.7% 的跨模态基准表明，即使证据更丰富，诊断仍然很难。

### 代码智能体正按能否运行、构建并通过项目检查来评判
仓库级编码在基础软件关卡上仍然会失败。RAT 针对环境配置，这是代码智能体经常连启动都做不到的一个常见原因；在其覆盖 2,000 多个仓库的基准中，它报告了高得多的环境配置成功率，其中 Python 为 63.2%，Rust 为 98.7%。另一项针对 8 个 C 项目中 212 个真实提交的研究说明了为什么这在完成配置后仍然重要：即使原始提交很小，生成的补丁仍然会编译失败、触发静态分析问题并漏过测试。这使执行、可构建性和仓库上下文继续处在代码智能体研究的中心。

#### Evidence
- [I reverse-engineered Claude Desktop's storage to give it memory](../Inbox/2026-04-25--i-reverse-engineered-claude-desktop-s-storage-to-give-it-memory.md): 仓库环境配置基准，以及跨语言的 ESSR 提升。
- [Can LLMs be Effective Code Contributors? A Study on Open-source Projects](../Inbox/2026-04-25--can-llms-be-effective-code-contributors-a-study-on-open-source-projects.md): 针对真实开源提交的研究记录了编译错误、静态分析失败，以及项目间成功率不均。

### 受限代码任务比广泛自主性带来了更清晰的收益
两篇论文把代码辅助推进到更窄、更具体的场景中。MOSAIC 处理在没有测试用例时的科学工作流生成。它使用师生蒸馏和紧凑的共享上下文，然后提升了 GPT-4o、Claude Sonnet 4 和 Gemini 2.5 Flash 在 SciCode 上的结果。另一项研究考察小型本地模型在离线 Python 缺陷检测中能做到什么。在 BugsInPy 的 349 个案例上，LLaMA 3.2 和 Mistral 的精确准确率约为 43% 到 45%，还有许多部分正确的回答能指出大致位置，但没有给出完整修复。实际模式是：在明确约束下提供定向帮助，而不是通用的自主编码。

#### Evidence
- [Knowledge Lever Risk Management for Software Engineering: A Stochastic Framework for Mitigating Knowledge Loss](../Inbox/2026-04-25--knowledge-lever-risk-management-for-software-engineering-a-stochastic-framework-for-mitigating-knowledge-loss.md): 在没有测试用例的情况下进行科学代码生成，并在 SciCode 上取得了可度量的提升。
- [An Empirical Evaluation of Locally Deployed LLMs for Bug Detection in Python Code](../Inbox/2026-04-25--an-empirical-evaluation-of-locally-deployed-llms-for-bug-detection-in-python-code.md): BugsInPy 上的离线缺陷检测结果，给出了精确和部分准确率的细分。
