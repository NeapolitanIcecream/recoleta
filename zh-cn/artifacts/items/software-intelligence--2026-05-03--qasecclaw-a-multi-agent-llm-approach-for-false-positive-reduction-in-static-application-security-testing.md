---
source: arxiv
url: https://arxiv.org/abs/2605.01885v1
published_at: '2026-05-03T14:05:52'
authors:
- Mohd Ruhul Ameen
- Md Takrim Ul Alam
- Akif Islam
topics:
- code-intelligence
- sast
- llm-agents
- software-security
- false-positive-reduction
- multi-agent-software-engineering
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# QASecClaw: A Multi-Agent LLM Approach for False Positive Reduction in Static Application Security Testing

## Summary
## 摘要
QASecClaw 先用 Semgrep 查找候选安全问题，再由面向代码的 LLM 代理读取代码上下文，抑制可能的误报。在 OWASP Benchmark v1.2 上，相比独立使用 Semgrep，它报告的精确率和 F1 明显更高，召回率小幅下降。

## 问题
- SAST 工具匹配到高风险模式时，如果遗漏附近的上下文，例如清理、编码、验证或参数化 API，常会把安全代码标记为有漏洞。
- 误报会浪费开发人员和安全审查人员的时间，降低对扫描器输出的信任，并可能导致真实漏洞被忽略。
- 论文的目标是在保留 SAST 作为高召回候选发现来源的同时减少误报。

## 方法
- QASecClaw 先运行 Semgrep，并将其告警作为候选漏洞处理，而不让 LLM 搜索整个代码库。
- SAST Filter Agent 将每个发现、CWE 类型、文件位置和源代码上下文发送给 Qwen 3.5 Plus，并要求判断是真阳性还是假阳性。
- Mission Orchestrator 协调用于测试规划、基于 Semgrep 的验证、证据关联、LLM 过滤和报告生成的代理。
- 系统按每批 15 个文件处理发现，并将 LLM 响应验证为结构化 JSON。
- 如果 LLM 失败、超时或返回格式错误的 JSON，QASecClaw 会保留原始 Semgrep 发现，以免隐藏可能存在的真实问题。

## 结果
- 评估使用完整的 OWASP Benchmark v1.2：2,740 个 Java 测试用例，覆盖 11 个 CWE 类别，其中 1,415 个有漏洞用例，1,325 个安全用例。
- QASecClaw 报告的 F1 = 90.93%，独立 Semgrep 为 78.39%，提升约 12.54 个百分点。
- 误报从 Semgrep 的 560 个降至 QASecClaw 的 64 个，减少 88.6%，召回率下降 3.1%。
- 论文中的汇总指标显示，QASecClaw 的精确率为 0.951，召回率为 0.871，F1 为 0.909，误报率为 0.048，Youden’s J 为 0.823；Semgrep 的精确率为 0.695，召回率为 0.900，F1 为 0.784，误报率为 0.423，Youden’s J 为 0.477。
- 摘要中引用的按 CWE 分类结果包括 SQL Injection F1 = 94.05%、Cross-Site Scripting F1 = 89.58%、Weak Cryptography F1 = 99.61%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01885v1](https://arxiv.org/abs/2605.01885v1)
