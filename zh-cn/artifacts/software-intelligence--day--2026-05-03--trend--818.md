---
kind: trend
trend_doc_id: 818
granularity: day
period_start: '2026-05-03T00:00:00'
period_end: '2026-05-04T00:00:00'
topics:
- LLM software engineering
- static analysis
- vulnerability repair
- refactoring correctness
- agent context
- AI reliability
run_id: materialize-outputs
aliases:
- recoleta-trend-818
tags:
- recoleta/trend
- topic/llm-software-engineering
- topic/static-analysis
- topic/vulnerability-repair
- topic/refactoring-correctness
- topic/agent-context
- topic/ai-reliability
language_code: zh-CN
---

# 当软件任务给出窄证据时，LLM 更有可信度

## 概览
当天最强的研究把大语言模型（LLM）当作软件工件的有限审查者来使用。QASecClaw、VulKey 和 ACDL 显示了当前重点：给模型一个具体发现、补丁模式或上下文规范，然后测量或检查结果。关于控制和轨迹的近期工作在这里也很明显。

## 研究发现

### 安全审查与修复
安全工作有最清楚的实证信号。QASecClaw 先把 Semgrep 作为高召回扫描器，再让一个面向编码的 LLM 用源代码上下文判断每个候选发现。在 OWASP Benchmark v1.2 上，误报从 560 降到 64，召回率只下降 3.1%。对已经被扫描器噪声淹没的团队来说，这是一个划算的取舍。

VulKey 把同样的思路用在修复上。它不会只传入 CWE 标签，也不会只给完整示例补丁。它先预测一个修复模式，这个模式包含一个语法动作和一个安全相关的关键元素，然后把补丁生成过程建立在这个模式上。在 PrimeVul 上，它报告的修复准确率是 31.5%，比摘要里提到的最佳基线高 7.6 个百分点。这个结果支持一个实用结论：安全模型需要紧凑、任务相关的证据，而不只是漏洞名称。

#### 资料来源
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): QASecClaw design and OWASP Benchmark results, including false-positive reduction and recall tradeoff.
- [VulKey: Automated Vulnerability Repair Guided by Domain-Specific Repair Patterns](../Inbox/2026-05-03--vulkey-automated-vulnerability-repair-guided-by-domain-specific-repair-patterns.md): VulKey pattern-guided repair method and PrimeVul/Vul4J results.

### 维护正确性检查
重构正确性很适合用模型做分流，因为输入很具体，而且成对出现：原始 Java 代码、重构后的 Java 代码，以及一个正确性问题。refactoring-oracle 研究构建了 226 个真实 IDE bug 案例，覆盖 47 种重构类型。GPT-5.4 的首次运行准确率达到 93.8%，GPT-OSS-20B 达到 80.5%。作者也测试了在保持语义不变的代码修改下，结果是否稳定。

提交分类的表现要弱一些。Conventional Commit 研究使用 3,200 个 InfluxDB 提交和只靠提示词的开源模型。最好的一次运行准确率是 0.6154，few-shot 提示在平均表现上最好。这个结果仍然有用，但更像是给发布自动化提供提示词选择建议，而不是一个可直接上线的分类器。

#### 资料来源
- [Foundation Models as Oracles for Refactoring Correctness Detection](../Inbox/2026-05-03--foundation-models-as-oracles-for-refactoring-correctness-detection.md): Refactoring correctness dataset, model accuracies, and metamorphic testing.
- [Conventional Commit Classification using Large Language Models and Prompt Engineering](../Inbox/2026-05-03--conventional-commit-classification-using-large-language-models-and-prompt-engineering.md): Prompt-only Conventional Commit classification setup and reported accuracy/F1 results.

### Agent 上下文规范
Agent 工作越来越关注模型在每一步到底看到了什么。ACDL 给研究者一种方式，把上下文窗口描述成角色消息、信息片段、带时间索引的状态、条件、循环和多智能体上下文。它的价值在于可复现和可比较：两个 ReAct 风格的 agent 之所以不同，可能只是因为一个把推理轨迹保存在动作历史里，另一个没有。

Conclave 是一个实用对应物。它给 OpenCode 加上结构化的多模型辩论，使用 LEAD、SUPPORT、ALIGN、BUILD 和 CHALLENGE 信号，然后按认可分数选出赢家。这个项目目前还没有基准证据，而且它自己的成本核算很明确：3 个模型辩论 3 轮，每个用户消息要发出 9 次 API 调用。所以，这里的研究问题就是增加一次调用能带来多少可测的输出提升。

#### 资料来源
- [A Language for Describing Agentic LLM Contexts](../Inbox/2026-05-03--a-language-for-describing-agentic-llm-contexts.md): ACDL language scope, supported context constructs, and tooling.
- [Conclave – make LLMs debate each other before they respond](../Inbox/2026-05-03--conclave-make-llms-debate-each-other-before-they-respond.md): Conclave debate mechanism, provider mix, cost/latency notes, and lack of benchmark evidence.

### 人可验证的可靠性记录
可靠性讨论正在更明确地说明人应该检查什么。Knowledge Objects 立场论文提出，用结构化记录来表示主张、流程、证据、范围、验证状态和来源。它没有给出新的基准或用户研究，所以贡献是一个设计论证。

GitHub Actions 审计论文给出了同样需求的应用例子。4 个开源权重 LLM 按照 30 项检查表评估 95 个 Java 工作流，但模型之间的一致性只有一般水平，Fleiss’ kappa 只有 0.28。用 GPT-5 做裁决，再配合有针对性的人类复核，可以把验证工作量减少 81%，同时与专家判断保持 87% 一致。对高风险审计来说，这是一个有用的模式：模型投票可以减少复核负担，但专家检查仍然留在流程里。

#### 资料来源
- [Reliable AI Needs to Externalize Implicit Knowledge: A Human-AI Collaboration Perspective](../Inbox/2026-05-03--reliable-ai-needs-to-externalize-implicit-knowledge-a-human-ai-collaboration-perspective.md): Knowledge Objects proposal, validation metadata, and lack of new empirical evaluation.
- [How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing](../Inbox/2026-05-03--how-compliant-are-github-actions-workflows-a-checklist-based-study-with-llm-assisted-auditing.md): GitHub Actions checklist audit, agreement statistics, compliance results, and human-review process.
