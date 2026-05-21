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

## Summary
在输入已经受限的场景中，LLM 采用更可信：一个扫描器告警、一个按固定清单检查的工作流文件，或一组重构前后代码对。可行做法是在生产门禁之前加一个小型复核层，设置明确的回退规则，并做本地准确性检查。

## 面向 Semgrep 安全告警的 LLM 假阳性过滤
已经使用 Semgrep 的安全团队可以在扫描器之后加入一个 LLM 复核步骤，只把 Semgrep 发现项、CWE 标签、文件位置和附近源码上下文作为输入。输出应是结构化的真阳性或假阳性判断，并附一条简短理由。如果模型超时或返回格式错误的 JSON，工作流应保留原始 Semgrep 告警，不要关闭。

QASecClaw 为这种做法提供了一个有用的测试案例。在 OWASP Benchmark v1.2 上，它把 Semgrep 的假阳性从 560 个降到 64 个，同时召回率下降 3.1%。这些证据足以支持在噪声较大的规则族上做有限试点，例如注入、XSS 和弱密码学。第一个本地检查应把模型过滤后的告警与近期人工分诊决策对比，并同时报告假阳性减少量和漏掉的真实问题。

### Evidence
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): QASecClaw 使用 Semgrep 发现项和代码上下文进行 LLM 判断，并报告假阳性、召回率、精确率和 F1 结果。
- [QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing](../Inbox/2026-05-03--qasecclaw-a-multi-agent-llm-approach-for-false-positive-reduction-in-static-application-security-testing.md): 摘要说明了 OWASP Benchmark 评估、假阳性从 560 个降到 64 个，以及召回率下降 3.1%。

## 用于 GitHub Actions 工作流合规的清单审计队列
拥有大量 GitHub Actions 工作流的团队可以把文档化的 CI 实践转成固定审计清单，并且只把不确定的案例交给人工处理。有用的检查单位是一个工作流文件，对照具体的 YES、NO 或 NOT APPLICABLE 问题进行检查，例如最小权限、固定版本的 actions、密钥处理、缓存和失败通知。

GitHub Actions 审计研究说明了队列为什么需要处理分歧。4 个开放权重模型在 95 个 Java 工作流上的一致性只达到一般水平，Fleiss’ kappa 为 0.28。研究接受一致或近乎一致的答案，把分歧案例交给 GPT-5，并对未解决条目做有针对性的人工复核。这个流程在与专家判断保持 87% 一致的同时，把验证工作量减少了 81%。实际落地可以从权限控制周报开始，因为研究发现该项合规率只有 4%。

### Evidence
- [How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing](../Inbox/2026-05-03--how-compliant-are-github-actions-workflows-a-checklist-based-study-with-llm-assisted-auditing.md): 该研究定义了一个包含 30 项的 GitHub Actions 合规清单，报告了模型一致性，并描述了 GPT-5 加人工复核流程。
- [How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing](../Inbox/2026-05-03--how-compliant-are-github-actions-workflows-a-checklist-based-study-with-llm-assisted-auditing.md): 摘要描述了工作流风险、30 条标准、一般水平的模型一致性，以及合规结果。
- [How Compliant Are GitHub Actions Workflows? A Checklist-Based Study with LLM-Assisted Auditing](../Inbox/2026-05-03--how-compliant-are-github-actions-workflows-a-checklist-based-study-with-llm-assisted-auditing.md): 论文解释了为什么 actionlint 和 yamllint 等 linter 会漏掉文档化最佳实践违规。

## 用于 Java 重构正确性的前后对照 LLM 检查
IDE 厂商和 Java 团队可以测试一种面向高风险重构的 LLM 复核步骤：只向模型提供原始代码、重构后代码和一个正确性问题。这个检查适合重构场景，因为证据是成对且具体的，模型也可以返回一段简短解释供开发者查看。

这项重构判定器研究构建了 226 个真实 Java 重构 bug 案例，覆盖 47 种重构类型，其中包括编译错误和行为变化案例。GPT-5.4 首次运行准确率达到 93.8%，GPT-OSS-20B 达到 80.5%。一个有用的采用测试是，对 Move Method、Inline Method、Pull Up Method、Extract Local Variable 和 Rename Method 等高频重构给出非阻塞警告，并将结果与编译器结果、现有测试以及开发者接受或驳回行为进行对比。

### Evidence
- [Foundation Models as Oracles for Refactoring Correctness Detection](../Inbox/2026-05-03--foundation-models-as-oracles-for-refactoring-correctness-detection.md): 论文报告了包含 226 个案例的 Java 重构数据集、47 种重构类型、模型准确率和验证方法。
- [Foundation Models as Oracles for Refactoring Correctness Detection](../Inbox/2026-05-03--foundation-models-as-oracles-for-refactoring-correctness-detection.md): 摘要摘录给出了 GPT-OSS-20B 和 GPT-5.4 的准确率，并描述了开发工作流中的轻量分诊用途。
