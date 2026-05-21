---
kind: trend
trend_doc_id: 1006
granularity: day
period_start: '2026-05-14T00:00:00'
period_end: '2026-05-15T00:00:00'
topics:
- coding agents
- software engineering
- agent safety
- open-ended coding
- sandbox infrastructure
- RAG
- program synthesis
run_id: materialize-outputs
aliases:
- recoleta-trend-1006
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-safety
- topic/open-ended-coding
- topic/sandbox-infrastructure
- topic/rag
- topic/program-synthesis
language_code: zh-CN
---

# 代码智能体正围绕可执行反馈和明确运行边界构建

## Overview
当天最强的信号是带有可执行检查的实用代码智能体工作。FrontierSmith 和 DIO-Agent 使用评分或执行错误，让编码任务更难也更有用。Orchard 表明，同样的需求也存在于沙盒规模上。安全论文将权限和第三方技能纳入核心设计问题。

## Clusters

### 开放式编码数据和程序发现
FrontierSmith 把开放式编码当作数据问题处理。它将封闭式竞赛编程任务变异为优化任务，按解法多样性筛选，并构建评分验证器。用 200 个合成问题训练 Qwen3.5 模型后，9B 模型在 FrontierCS 上提高 8.82 分，27B 模型提高 12.12 分，在 ALE-bench 上也有大幅提升。

DIO-Agent 处理一个相关缺口：只有输入输出示例时的代码合成。它运行一个进化循环，由大语言模型（LLM）编辑代码，执行过程给出具体错误，课程机制随时间加入更难的用例。在使用 DeepSeek V3.2 的 IO2CodeBench 上，它达到 58.63 的平均通过率，高于 CodeEvolve 的 49.60 和 AlphaEvolve 的 47.29。共同结论很直接：更强的编码系统需要比一个提示和一个答案更丰富的任务信号。

#### Evidence
- [FrontierSmith: Synthesizing Open-Ended Coding Problems at Scale](../Inbox/2026-05-14--frontiersmith-synthesizing-open-ended-coding-problems-at-scale.md): FrontierSmith 的概要、方法，以及在 FrontierCS 和 ALE-bench 上报告的提升。
- [From I/O to Code with Discovery Agent](../Inbox/2026-05-14--from-i-o-to-code-with-discovery-agent.md): DIO-Agent 的基准设置、进化方法、消融实验和通过率结果。

### 沙盒化训练基础设施
Orchard 把智能体训练变成系统问题。它的 Kubernetes 原生环境服务处理沙盒创建、命令执行、文件 I/O、网络策略和清理。同一层支持软件工程、浏览器使用和个人助理智能体。Orchard-SWE 报告称，在监督微调（SFT）和强化学习（RL）后，它在 SWE-bench Verified 上达到 67.5%，环境服务报告的平均命令延迟为 0.280 s。

两项范围更广的研究解释了这对采用的影响。一项涵盖 92 项主要研究的系统综述发现，工业界智能体使用集中在输出可由测试、编译器、日志、指标或持续集成状态检查的场景。一项对 12 家公司的访谈研究发现，大多数生产用途处于助手或任务智能体层级。4 家公司有更强的实验性智能体，但由于人工评审仍是主要准入方式，无法部署它们。

#### Evidence
- [Orchard: An Open-Source Agentic Modeling Framework](../Inbox/2026-05-14--orchard-an-open-source-agentic-modeling-framework.md): Orchard 的环境设计、训练配方、SWE-bench 结果、延迟和成本声明。
- [Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle](../Inbox/2026-05-14--assistance-to-autonomy-a-systematic-literature-review-of-agentic-ai-across-the-software-development-life-cycle.md): 关于 SDLC 阶段、工业场景和可执行反馈的系统综述证据。
- [Agentic AI in Industry: Adoption Level and Deployment Barriers](../Inbox/2026-05-14--agentic-ai-in-industry-adoption-level-and-deployment-barriers.md): 关于成熟度层级和部署障碍的行业访谈证据。

### 权限和智能体供应链风险
AuthBench 将最小权限访问变成可衡量的编码智能体任务。模型必须在终端任务运行前推断读取、写入和执行的允许列表。完全访问在敏感任务上带来较高任务成功率，但攻击成功率也达到 65.8%。黄金权限将攻击成功率保持在 0.0%。生成的策略仍要在效用和暴露之间取舍：Gemini 3.1 Pro 在敏感任务上达到 85.8% 的任务成功率，同时攻击成功率为 28.3%。

技能供应链论文显示了第二个控制缺口。Semantic Compliance Hijacking（SCH）把恶意意图藏在自然语言技能指令中，导致智能体自己编写并运行有害代码。在测试的平台和模型中，该攻击达到 36.00% 至 62.11% 的完全泄漏率，以及 30.56% 至 64.44% 的远程代码执行成功率。论文报告的扫描器对初始的纯文本技能检测率为 0.00%。

#### Evidence
- [Do Coding Agents Understand Least-Privilege Authorization?](../Inbox/2026-05-14--do-coding-agents-understand-least-privilege-authorization.md): AuthBench 的任务定义、权限指标、敏感任务结果和分解方法。
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](../Inbox/2026-05-14--exploiting-llm-agent-supply-chains-via-payload-less-skills.md): 无载荷技能攻击设置、评估范围、泄漏/RCE 结果和检测结果。

### 仓库和运行时上下文管理
多篇论文关注智能体如何选择并保留正确证据。软件工程检索增强生成（RAG）研究将查询处理、检索、上下文细化和生成分开分析。它的主要实证结论是，检索器选择对最终质量的影响通常大于生成器选择，并且 BM25 在测试的软件任务中仍表现强劲。

MemDocAgent 将类似关注点用于仓库文档。它在按依赖顺序进行的文档工作中维护一个长时间运行的记忆，验证事实一致性，并存储先前声明。在 20 个 Python 仓库上，它的 GPT-5-mini 运行生成 3,323 份文档，完整性得分 0.958，真实性得分 0.952，有用性得分 0.800。RCLAgent 将证据控制用于微服务故障：它把智能体分配给追踪 span，并沿追踪图合并局部发现，报告的准确率比第二好的根因定位方法高约 7.51%，速度比其他基于 LLM 的方法快 1.75 倍以上。

#### Evidence
- [Not All RAGs Are Created Equal: A Component-Wise Empirical Study for Software Engineering Tasks](../Inbox/2026-05-14--not-all-rags-are-created-equal-a-component-wise-empirical-study-for-software-engineering-tasks.md): 按组件划分的 RAG 研究设计、语料库规模和主要检索器侧结论。
- [Remember Your Trace: Memory-Guided Long-Horizon Agentic Framework for Consistent and Hierarchical Repository-Level Code Documentation](../Inbox/2026-05-14--remember-your-trace-memory-guided-long-horizon-agentic-framework-for-consistent-and-hierarchical-repository-level-code-documentation.md): MemDocAgent 的记忆设计、验证方法和仓库文档结果。
- [Towards In-Depth Root Cause Localization for Microservices with Multi-Agent Recursion-of-Thought](../Inbox/2026-05-14--towards-in-depth-root-cause-localization-for-microservices-with-multi-agent-recursion-of-thought.md): RCLAgent 的追踪 span 分解、基准、准确率声明和加速声明。
