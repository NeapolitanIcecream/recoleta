---
kind: ideas
granularity: day
period_start: '2026-05-03T00:00:00'
period_end: '2026-05-04T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- LLM software engineering
- static analysis
- vulnerability repair
- refactoring correctness
- agent context
- AI reliability
tags:
- recoleta/ideas
- topic/llm-software-engineering
- topic/static-analysis
- topic/vulnerability-repair
- topic/refactoring-correctness
- topic/agent-context
- topic/ai-reliability
language_code: zh-CN
---

# 有边界的 LLM 复核门禁

## 摘要
当输入已经被限定时，LLM 采用最可信：一个扫描器告警、一个按固定清单检查的工作流文件，或者一对重构前后的代码。实际做法是加一层小型复核，并设置明确的回退规则，在接触生产门禁之前先做本地准确率检查。

## LLM 对 Semgrep 安全告警的假阳性过滤
已经运行 Semgrep 的安全团队可以在扫描器后面加一层 LLM 审查，只把 Semgrep 告警、CWE 标签、文件位置和附近源代码上下文作为输入。输出应当是结构化的真阳性或假阳性判断，再加一句简短理由。如果模型超时或返回格式错误的 JSON，流程应保留原始 Semgrep 告警。

QASecClaw 提供了一个合适的测试样例。在 OWASP Benchmark v1.2 上，它把 Semgrep 的假阳性从 560 降到 64，同时召回率下降了 3.1%。这已经足够支持在注入、XSS 和弱加密这类噪声较多的规则族上做一次有限试点。第一步本地检查应把模型过滤后的告警与最近的人工分流结果对比，并同时报告假阳性减少和漏掉的真实问题。

### 资料来源
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): QASecClaw uses Semgrep findings plus code context for LLM judgment and reports false-positive, recall, precision, and F1 results.
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): The abstract states the OWASP Benchmark evaluation, false-positive reduction from 560 to 64, and 3.1% recall reduction.

## GitHub Actions 工作流合规性的清单审计队列
有大量 GitHub Actions 工作流的团队可以把文档化的 CI 做法整理成固定审计清单，只把不确定的案例交给人工。合适的检查单位是单个 workflow 文件，按明确的 YES、NO 或 NOT APPLICABLE 问题逐项检查，例如最小权限、固定版本的 actions、密钥处理、缓存和失败通知。

GitHub Actions 审计研究说明了为什么队列需要处理分歧。四个开源权重模型在 95 个 Java 工作流上的一致性只有一般，Fleiss’ kappa 只有 0.28。研究接受全体一致或接近全体一致的答案，把分歧案例送到 GPT-5，再对未解决项做定向人工复核。这个流程把验证工作量减少了 81%，同时与专家判断保持 87% 一致。实际落地可以先做权限控制的每周报告，因为研究发现那里的合规率只有 4%。

### 资料来源
- [How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing](../Inbox/2026-05-03--how-compliant-are-github-actions-workflows-a-checklist-based-study-with-llm-assisted-auditing.md): The study defines a 30-item GitHub Actions compliance checklist, reports model agreement, and describes GPT-5 plus human review.
- [How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing](../Inbox/2026-05-03--how-compliant-are-github-actions-workflows-a-checklist-based-study-with-llm-assisted-auditing.md): The abstract describes workflow risks, the 30 criteria, fair model agreement, and compliance results.
- [How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing](../Inbox/2026-05-03--how-compliant-are-github-actions-workflows-a-checklist-based-study-with-llm-assisted-auditing.md): The paper explains why linters such as actionlint and yamllint miss documented best-practice violations.

## 用于 Java 重构正确性的前后对照 LLM 检查
IDE 厂商和 Java 团队可以给模型原始代码、重构后代码和一个正确性问题，测试 LLM 对高风险重构的复核。这个检查适合重构，因为证据是成对且具体的，模型也可以返回一段简短说明供开发者查看。

这项重构判定研究整理了 226 个真实的 Java 重构缺陷案例，覆盖 47 种重构类型，包括编译错误和行为变化两类。GPT-5.4 的首次运行准确率达到 93.8%，GPT-OSS-20B 达到 80.5%。一个实用的采用测试，是对 Move Method、Inline Method、Pull Up Method、Extract Local Variable 和 Rename Method 这类高频重构给出非阻塞警告，并把结果与编译器输出、现有测试和开发者接受或忽略的行为对照。

### 资料来源
- [Foundation Models as Oracles for Refactoring Correctness Detection](../Inbox/2026-05-03--foundation-models-as-oracles-for-refactoring-correctness-detection.md): The paper reports the 226-case Java refactoring dataset, 47 refactoring types, model accuracies, and validation approach.
- [Foundation Models as Oracles for Refactoring Correctness Detection](../Inbox/2026-05-03--foundation-models-as-oracles-for-refactoring-correctness-detection.md): The abstract excerpt gives GPT-OSS-20B and GPT-5.4 accuracy and describes lightweight triage use in development workflows.
