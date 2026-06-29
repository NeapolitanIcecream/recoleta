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
QASecClaw 先用 Semgrep 找出候选安全问题，再用一个专注代码的 LLM 代理读取代码上下文，筛掉更可能的误报。在 OWASP Benchmark v1.2 上，它的精确率和 F1 都明显高于单独使用 Semgrep，但召回率小幅下降。

## 问题
- 当 SAST 工具匹配到危险模式，却忽略了附近的上下文，比如净化、编码、校验或参数化 API 时，它们常会把安全代码标成有漏洞。
- 误报会浪费开发和安全审查时间，降低对扫描结果的信任，还可能让真实漏洞被忽略。
- 这篇论文要减少误报，同时保留 SAST 作为高召回候选发现来源的角色。

## 方法
- QASecClaw 先运行 Semgrep，把它的告警当作候选漏洞，而不是让 LLM 在整个代码库里搜索。
- SAST Filter Agent 会把每个发现、CWE 类型、文件位置和源代码上下文发给 Qwen 3.5 Plus，并要求判断是真阳性还是误报。
- Mission Orchestrator 负责协调测试规划、基于 Semgrep 的验证、证据关联、LLM 筛选和报告生成。
- 系统按每批 15 个文件处理发现，并将 LLM 响应校验为结构化 JSON。
- 如果 LLM 失败、超时或返回的 JSON 格式错误，QASecClaw 会保留原始的 Semgrep 结果，避免遮住可能真实的问题。

## 结果
- 评估使用完整的 OWASP Benchmark v1.2：共 2,740 个 Java 测试用例，覆盖 11 个 CWE 类别，其中 1,415 个为有漏洞案例，1,325 个为安全案例。
- QASecClaw 的 F1 为 90.93%，单独使用 Semgrep 为 78.39%，提升约 12.54 个百分点。
- 误报从 Semgrep 的 560 个降到 QASecClaw 的 64 个，减少 88.6%；召回率下降 3.1%。
- 论文中的总体指标显示，QASecClaw 的精确率为 0.951、召回率为 0.871、F1 为 0.909、误报率为 0.048、Youden’s J 为 0.823；Semgrep 的精确率为 0.695、召回率为 0.900、F1 为 0.784、误报率为 0.423、Youden’s J 为 0.477。
- 摘要中引用的按 CWE 分项结果包括：SQL 注入 F1 = 94.05%，跨站脚本 F1 = 89.58%，弱加密 F1 = 99.61%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01885v1](https://arxiv.org/abs/2605.01885v1)
