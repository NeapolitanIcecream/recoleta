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

# 代码代理正在围绕可执行反馈和明确的运行限制构建

## 概览
这一天最强的信号是带有可执行检查的实用代码代理工作。FrontierSmith 和 DIO-Agent 用评分或执行错误，把编码任务变得更难，也更有用。Orchard 在沙箱规模上展示了同样的需求。安全类论文把权限和第三方技能变成了核心设计问题。

## 研究发现

### 开放式编程数据与程序发现
FrontierSmith 将开放式编程当作数据问题来处理。它把封闭的竞赛编程任务改造成优化任务，筛选解法多样性，并构建评分验证器。在 200 个合成问题上训练 Qwen3.5 模型后，9B 版本的 FrontierCS 提升 8.82 分，27B 版本提升 12.12 分，在 ALE-bench 上也有较大提升。

DIO-Agent 解决的是相关问题：只有输入输出示例时的代码合成。它运行一个进化循环，由大语言模型（LLM）编辑代码，执行过程给出具体错误，课程安排再逐步加入更难的案例。在 IO2CodeBench 上使用 DeepSeek V3.2 时，它的平均通过率达到 58.63，超过 CodeEvolve 的 49.60 和 AlphaEvolve 的 47.29。共同结论很直接：更强的编程系统需要比一个提示和一个答案更丰富的任务信号。

#### 资料来源
- [FrontierSmith: Synthesizing Open-Ended Coding Problems at Scale](../Inbox/2026-05-14--frontiersmith-synthesizing-open-ended-coding-problems-at-scale.md): FrontierSmith summary, method, and reported gains on FrontierCS and ALE-bench.
- [From I/O to Code with Discovery Agent](../Inbox/2026-05-14--from-i-o-to-code-with-discovery-agent.md): DIO-Agent benchmark setup, evolutionary method, ablations, and pass-rate results.

### 沙箱训练基础设施
Orchard 把代理训练变成了系统问题。它的 Kubernetes 原生环境服务处理沙箱创建、命令执行、文件 I/O、网络策略和清理。同一层也支持软件工程、浏览器使用和个人助手代理。Orchard-SWE 在监督微调（SFT）和强化学习（RL）后，在 SWE-bench Verified 上报告 67.5%，而环境服务的平均命令延迟为 0.280 秒。

两项更广泛的研究解释了这对落地为何重要。一项对 92 篇原始研究的系统综述发现，工业界代理的使用集中在输出可以由测试、编译器、日志、指标或持续集成状态检查的场景。对 12 家公司的访谈研究发现，大多数生产使用停留在助手或任务代理层级。4 家公司有更强的实验性代理，但因为人工审查仍是主要的准入路径，没法部署。

#### 资料来源
- [Orchard: An Open-Source Agentic Modeling Framework](../Inbox/2026-05-14--orchard-an-open-source-agentic-modeling-framework.md): Orchard environment design, training recipes, SWE-bench result, latency, and cost claims.
- [Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle](../Inbox/2026-05-14--assistance-to-autonomy-a-systematic-literature-review-of-agentic-ai-across-the-software-development-life-cycle.md): Systematic review evidence on SDLC phases, industrial contexts, and executable feedback.
- [Agentic AI in Industry: Adoption Level and Deployment Barriers](../Inbox/2026-05-14--agentic-ai-in-industry-adoption-level-and-deployment-barriers.md): Industry interview evidence on maturity levels and deployment barriers.

### 权限与代理供应链风险
AuthBench 把最小权限访问变成一个可测量的编码代理任务。模型必须先推断读、写、执行的允许列表，再运行终端任务。完全访问让敏感任务的成功率很高，但攻击成功率也达到 65.8%。金色权限把攻击成功率压到 0.0%。生成的策略仍然在效用和暴露之间取舍：Gemini 3.1 Pro 在敏感任务上的成功率达到 85.8%，攻击成功率为 28.3%。

技能供应链论文显示了第二个控制缺口。语义合规劫持（SCH）把恶意意图藏在自然语言技能说明中，导致代理自己写出并运行有害代码。在测试的平台和模型上，这种攻击的完整泄露率达到 36.00% 到 62.11%，远程代码执行成功率达到 30.56% 到 64.44%。论文中报告的扫描器对最初仅有文字说明的技能检测率为 0.00%。

#### 资料来源
- [Do Coding Agents Understand Least-Privilege Authorization?](../Inbox/2026-05-14--do-coding-agents-understand-least-privilege-authorization.md): AuthBench task definition, permission metrics, sensitive-task results, and decomposition method.
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](../Inbox/2026-05-14--exploiting-llm-agent-supply-chains-via-payload-less-skills.md): Payload-less skill attack setup, evaluation scope, leakage/RCE results, and detection results.

### 仓库与运行时上下文管理
有几篇论文关注代理如何选择并保留合适的证据。软件工程检索增强生成（RAG）研究把查询处理、检索、上下文精炼和生成分开来看。它的主要实证结论是，检索器的选择往往比生成器的选择更影响最终质量，而 BM25 在测试的软件任务中仍然很强。

MemDocAgent 把类似关注点用于仓库文档。它为按依赖顺序进行的文档工作保留一条长期记忆，验证事实一致性，并保存先前主张。在 20 个 Python 仓库上，它用 GPT-5-mini 生成 3,323 份文档，完整性得分 0.958，真实性得分 0.952，实用性得分 0.800。RCLAgent 把证据控制用于微服务故障定位：它把代理分配到 trace span，再沿 trace 图合并局部发现，报告的准确率比第二好的根因定位方法高约 7.51%，比其他基于 LLM 的方法快 1.75 倍以上。

#### 资料来源
- [Not All RAGs Are Created Equal: A Component-Wise Empirical Study for Software Engineering Tasks](../Inbox/2026-05-14--not-all-rags-are-created-equal-a-component-wise-empirical-study-for-software-engineering-tasks.md): Component-wise RAG study design, corpus size, and main retriever-side claim.
- [Remember Your Trace: Memory-Guided Long-Horizon Agentic Framework for Consistent and Hierarchical Repository-Level Code Documentation](../Inbox/2026-05-14--remember-your-trace-memory-guided-long-horizon-agentic-framework-for-consistent-and-hierarchical-repository-level-code-documentation.md): MemDocAgent memory design, verification method, and repository documentation results.
- [Towards In-Depth Root Cause Localization for Microservices with Multi-Agent Recursion-of-Thought](../Inbox/2026-05-14--towards-in-depth-root-cause-localization-for-microservices-with-multi-agent-recursion-of-thought.md): RCLAgent trace-span decomposition, benchmarks, accuracy claim, and speedup claim.
