---
kind: ideas
granularity: day
period_start: '2026-05-14T00:00:00'
period_end: '2026-05-15T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- coding agents
- software engineering
- agent safety
- open-ended coding
- sandbox infrastructure
- RAG
- program synthesis
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/agent-safety
- topic/open-ended-coding
- topic/sandbox-infrastructure
- topic/rag
- topic/program-synthesis
language_code: zh-CN
---

# 代码代理验证控制

## 摘要
代码代理工作正在收敛到团队现在就能构建和测试的运行控制：用于上线和资格判定的沙箱服务、针对 shell 访问和技能的按任务权限门控，以及带有可度量检索和文档质量的仓库上下文系统。共同的采用障碍是在真实工作流约束下完成验证。

## 用于代码代理上线和 CI 资格判定的 Kubernetes 沙箱服务
训练或评估软件工程代理的团队应把执行环境和代理 harness 分开。一个小型 Kubernetes 服务可以负责沙箱创建、命令执行、文件 I/O、网络策略、清理和日志，然后通过稳定的 API 暴露这些操作，用于训练运行、评估和内部试点。

Orchard 展示了这一层的形态：它把轻量级执行代理注入任务容器，避免在重复命令上走更慢的 Kubernetes exec 路径，并报告了 0.280 s 的平均命令延迟。同一个环境服务还支持软件工程、浏览器使用和生产力代理任务，这对已经为不同领域维护独立 harness 的团队很重要。

当沙箱接入可执行的资格判定时，这种做法最有价值：单元测试、编译器输出、CI 状态、日志和指标。对 92 篇研究的综述发现，工业界代理使用集中在带有可执行反馈的阶段；对 12 家公司的访谈研究发现，更强的实验性代理仍被挡在生产之外，因为人工审查仍是主要的资格路径。一个实际的起点是把现有代码代理试点接到沙箱 API 上，记录通过率、命令延迟、失败动作轨迹，以及多次运行下的 CI 可复现性。

### 资料来源
- [Orchard: An Open-Source Agentic Modeling Framework](../Inbox/2026-05-14--orchard-an-open-source-agentic-modeling-framework.md): Orchard describes the Kubernetes-native environment service, sandbox lifecycle operations, latency results, and SWE-bench Verified results.
- [Orchard: An Open-Source Agentic Modeling Framework](../Inbox/2026-05-14--orchard-an-open-source-agentic-modeling-framework.md): The paper reports Orchard-SWE results after SFT and RL and describes agent training through repeated sandbox interaction.
- [Assistance to Autonomy: A Systematic Literature Review of Agentic AI across the Software Development Life Cycle](../Inbox/2026-05-14--assistance-to-autonomy-a-systematic-literature-review-of-agentic-ai-across-the-software-development-life-cycle.md): The systematic review links industrial adoption to verifiable software phases and executable feedback loops.
- [Agentic AI in Industry: Adoption Level and Deployment Barriers](../Inbox/2026-05-14--agentic-ai-in-industry-adoption-level-and-deployment-barriers.md): The interview study identifies verification as the blocker that keeps stronger experimental agents out of active workflows.

## 在代码代理 shell 访问前按任务设置读、写、执行策略
代码代理部署需要在代理接触仓库或终端之前先做一次预检权限步骤。这个步骤应为请求的任务生成按路径划分的读、写、执行允许列表，审计每一项授权是否与任务相关、是否暴露敏感内容，然后在沙箱中按该策略运行代理。

AuthBench 给团队提供了一个具体的评估模式。完全访问在敏感任务上的任务成功率达到 94.0%，攻击成功率为 65.8%。人工审查的黄金权限把任务成功率做到 81.7%，攻击成功率为 0.0%。生成的策略仍然留下暴露：Gemini 3.1 Pro 在敏感任务上的任务成功率达到 85.8%，攻击成功率为 28.3%。

同样的门槛也应覆盖第三方技能。Semantic Compliance Hijacking 把恶意意图藏在自然语言技能说明里，让代理在正常工作中写入并运行有害代码。在报告的测试里，仅有散文内容被篡改的技能在论文引用的扫描器下检测率为 0.00%，而在测试配置中，完整泄露和远程代码执行的成功率都很高。一个有用的内部检查是做一个小型红队套件，包含带密钥的仓库任务、正常技能、投毒技能和预期允许列表，并按任务成功率和攻击成功率打分。

### 资料来源
- [Do Coding Agents Understand Least-Privilege Authorization?](../Inbox/2026-05-14--do-coding-agents-understand-least-privilege-authorization.md): AuthBench defines permission-boundary inference and reports task success and attack success under full access, golden permissions, and generated policies.
- [Do Coding Agents Understand Least-Privilege Authorization?](../Inbox/2026-05-14--do-coding-agents-understand-least-privilege-authorization.md): The paper frames least-privilege authorization as a deployment requirement for agents with shell, repository, and file access.
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](../Inbox/2026-05-14--exploiting-llm-agent-supply-chains-via-payload-less-skills.md): The skill-supply-chain paper describes SCH, its attack setup, leakage and RCE success ranges, and scanner detection results.
- [Exploiting LLM Agent Supply Chains via Payload-less Skills](../Inbox/2026-05-14--exploiting-llm-agent-supply-chains-via-payload-less-skills.md): The content chunk reports peak confidentiality and RCE success rates and the 0.00% detection rate for manipulated skill files.

## 使用检索器对比和依赖顺序文档的代码代理仓库上下文测试
开发工具团队可以把仓库上下文当作一个可度量的子系统，从而提高代码代理的可靠性。先为代理实际要做的任务做一次检索器对比：漏洞修复、代码摘要和代码生成。把 BM25 作为基线，比较稠密检索和混合检索，并追踪检索到的文件是否支持最终补丁或答案。

这篇 RAG 研究把查询处理、检索、上下文精炼和生成拆开，然后在 Python 软件任务上测试这些部分。它的主要实证结论是，检索器的选择往往比生成器更影响最终质量，而 BM25 在测试任务中仍然有竞争力。这个发现对那些把大部分精力花在更换模型、却没有度量检索的团队很有用。

文档也可以放进同一个上下文层。MemDocAgent 按依赖顺序生成仓库文档，把先前结论保存在记忆中，检查一致性，并把接受的文档留给后续步骤使用。在 20 个 Python 仓库上，GPT-5-mini 运行生成了 3,323 份文档，完整性得分 0.958，真实性得分 0.952，实用性得分 0.800。一个可行的上线方式是先为一个服务生成文档，对最近的 issue 或 pull request 做一次检索评估，再检查代理补丁是否引用了人工审阅者认为相关的文件和文档。

### 资料来源
- [Not All RAGs Are Created Equal: A Component-Wise Empirical Study for Software Engineering Tasks](../Inbox/2026-05-14--not-all-rags-are-created-equal-a-component-wise-empirical-study-for-software-engineering-tasks.md): The RAG study compares pipeline components and reports that retriever-side choices often matter more than generator choice for software tasks.
- [Not All RAGs Are Created Equal: A Component-Wise Empirical Study for Software Engineering Tasks](../Inbox/2026-05-14--not-all-rags-are-created-equal-a-component-wise-empirical-study-for-software-engineering-tasks.md): The paper describes the component-wise RAG evaluation across query processing, retrieval, context refinement, and generators.
- [Remember Your Trace: Memory-Guided Long-Horizon Agentic Framework for Consistent and Hierarchical Repository-Level Code Documentation](../Inbox/2026-05-14--remember-your-trace-memory-guided-long-horizon-agentic-framework-for-consistent-and-hierarchical-repository-level-code-documentation.md): MemDocAgent reports dependency-ordered repository documentation, memory, verification, and aggregate documentation quality scores.
- [Remember Your Trace: Memory-Guided Long-Horizon Agentic Framework for Consistent and Hierarchical Repository-Level Code Documentation](../Inbox/2026-05-14--remember-your-trace-memory-guided-long-horizon-agentic-framework-for-consistent-and-hierarchical-repository-level-code-documentation.md): The content chunk explains repository documentation as context for human developers and coding agents navigating large codebases.
