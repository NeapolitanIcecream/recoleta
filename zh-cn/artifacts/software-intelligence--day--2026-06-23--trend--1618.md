---
kind: trend
trend_doc_id: 1618
granularity: day
period_start: '2026-06-23T00:00:00'
period_end: '2026-06-24T00:00:00'
topics:
- coding agents
- software engineering
- agent safety
- secure code generation
- research automation
run_id: materialize-outputs
aliases:
- recoleta-trend-1618
tags:
- recoleta/trend
- topic/coding-agents
- topic/software-engineering
- topic/agent-safety
- topic/secure-code-generation
- topic/research-automation
language_code: zh-CN
---

# 编码代理需要普查数据、成本控制和安全证据

## Overview
这一时期的重点是编码代理问责：测量真实使用情况、控制工具成本，并在代码运行后检查安全性。最有力的证据来自 1.8 亿仓库普查、贝叶斯控制和 BigBag；产品项目补充了治理需求，但评估较少。

## Clusters

### 开源代理活动测量
最明确的实证信号来自对 1.8 亿多个 Git 仓库中 AI 编码代理的多方法普查。结果显示，只查找机器人账号会漏掉大部分活动。在 V2510 快照中，多方法扫描找到 Claude Code 的 850,157 次提交，而机器人账号查找只找到 28,154 次。V2604 快照将 1,772,677 次提交归因于代理，其中 Claude Code 占一半。相比只依赖拉取请求、机器人名称或配置文件等单一渠道痕迹，这为软件供应链研究提供了更可靠的基础。

#### Evidence
- [Detecting AI Coding Agents in Open Source: A Validated Multi-Method Census of 180 Million Repositories](../Inbox/2026-06-23--detecting-ai-coding-agents-in-open-source-a-validated-multi-method-census-of-180-million-repositories.md): 摘要报告了 1.8 亿仓库普查、四个检测渠道、提交数量和召回差距。

### 关注成本的编码代理编排
代理工作正被当作带有明确成本的控制问题处理。贝叶斯控制论文维护一个后验信念，用来估计候选程序能否通过验证，然后决定是运行低成本评审器、重新生成、验证，还是停止。评估覆盖六个生成器和九个编码基准。报告中的收益在验证成本高、低成本评审器信号不完全准确时最强。BigBag 将类似约束用于依赖修复：它要求代理生成可执行的 Java 抽象语法树转换，然后在受同一库更新影响的多个客户端之间复用这些转换。最佳设置在原始损坏客户端上达到 78.6% 的修复率，整体跨项目修复率为 33.3%。

#### Evidence
- [Bayesian control for coding agents](../Inbox/2026-06-23--bayesian-control-for-coding-agents.md): 摘要给出了贝叶斯控制器、动作选择、评估规模和高验证成本下的结果。
- [Agentic Generation of AST Transformation Rules for Fixing Breaking Updates](../Inbox/2026-06-23--agentic-generation-of-ast-transformation-rules-for-fixing-breaking-updates.md): 摘要给出了 BigBag 的 AST 转换流程、数据集规模、修复率和迁移结果。

### 代理编写软件的安全检查
语料中的安全研究要求可执行证明和可读控制。Kauge 使用 OWASP 和 CERT 原则以及漏洞利用测试，将安全编码知识、代码执行能力以及二者之间的差距分开评估。论文报告称，模型常常知道相关原则，却无法在正确的代码边界实施防护。AutoSpec 处理安全问题的另一部分。它用带标签的执行轨迹修订大型语言模型（LLM）代理的符号安全规则，然后保留能提高轨迹级得分的编辑。在代码执行和具身代理领域的 291 条轨迹上，它报告的 F1 分数为 0.98 和 0.93，并将误报最多降低 94%。Postman Passport 提供了产品侧示例：API 调用方收到凭据引用，真实密钥留在客户的保险库中，并通过带范围检查的代理解析。

#### Evidence
- [SoK: AI Secure Code Generation: Progress, Pitfalls, and Paths Forward](../Inbox/2026-06-23--sok-ai-secure-code-generation-progress-pitfalls-and-paths-forward.md): 摘要描述了 Kauge 的知识、执行和差距层，以及报告中的知识-执行差距。
- [AutoSpec: Safety Rule Evolution for LLM Agents via Inductive Logic Programming](../Inbox/2026-06-23--autospec-safety-rule-evolution-for-llm-agents-via-inductive-logic-programming.md): 摘要给出了 AutoSpec 的规则编辑方法、轨迹数量、F1 分数和误报降低结果。
- [Postman launches passport for securing API secret access](../Inbox/2026-06-23--postman-launches-passport-for-securing-api-secret-access.md): 摘要描述了 Passport 的凭据引用设计和基于代理的范围检查。

### 大规模研究和文档代理
多项工作将多代理系统用于研究和软件知识工作。Agon 为想法、提案、实验和论文运行可复用的生产者-评审者循环。它的证据来自运行规模：444 次循环迭代、18 个角色、覆盖 10 多个科学领域的项目，以及一个月的调度器运行。论文明确指出，主张判断仍需要人类。LLM4MTLs 提供了一个规模更小、更容易测试的软件工程案例。它在 47 个示例、四种语言和三个大型语言模型上评估生成的模型转换语言代码。少样本示例提高了四种语言的语法表现，但语义正确性取决于语言和任务。

#### Evidence
- [Agon: An Autonomous Large-Scale Omnidisciplinary Research System Built on Prompt Economy](../Inbox/2026-06-23--agon-an-autonomous-large-scale-omnidisciplinary-research-system-built-on-prompt-economy.md): 摘要报告了 Agon 的生产者-评审者循环、运行规模，以及缺少量化主张有效性基准。
- [LLM4MTLs: Automated Generation and Empirical Evaluation of Model Transformation Languages](../Inbox/2026-06-23--llm4mtls-automated-generation-and-empirical-evaluation-of-model-transformation-languages.md): 摘要给出了 LLM4MTLs 的评估设置，以及语法收益和语义正确性不均衡之间的差异。
