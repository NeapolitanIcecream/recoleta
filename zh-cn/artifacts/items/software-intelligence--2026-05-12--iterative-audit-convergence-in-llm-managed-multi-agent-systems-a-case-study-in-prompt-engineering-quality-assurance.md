---
source: arxiv
url: https://arxiv.org/abs/2605.12280v1
published_at: '2026-05-12T15:39:04'
authors:
- Elias Calboreanu
topics:
- multi-agent-systems
- prompt-quality-assurance
- llm-auditing
- cross-document-validation
- agentic-software-engineering
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Iterative Audit Convergence in LLM-Managed Multi-Agent Systems: A Case Study in Prompt Engineering Quality Assurance

## Summary
## 摘要
论文报告了一个生产系统的个案研究：Claude 子代理审计了 AEGIS 的 8 个提示规范文件。AEGIS 是一条 7 通道 LLM 编排流水线。9 轮审计发现 51 个提示规范一致性缺陷，最后一次全范围检查没有发现问题。

## 问题
- 多代理 LLM 系统常把行为规则、数据契约、工具权限和集成逻辑放在提示文件中。字段名错误、过期的 Jira 规则或缺少通道引用，可能破坏代理交接或污染下游工作。
- 非正式提示审查可能漏掉跨文件缺陷，因为每个文件单独看可能有效，但与另一个文件不一致。
- 研究关注哪些缺陷类别只在后续扩大范围的审计轮次中出现，以及约 7150 行提示规范上的收敛情况。

## 方法
- 审计覆盖 8 个文件：7 个通道级 `PROMPT.md` 文件，共 6907 行，以及一个共享的 245 行 `TICKET_CONTRACT.md`。
- Claude 子代理使用一份检查清单，改编自 Weinberg 和 Freedman 式走查。清单覆盖版本一致性、跨通道 schema、Jira 权限、标签、通道数量引用、节奏和内部矛盾。
- 早期轮次一次审查一个文件。后续轮次把生产者和消费者文件一起加载，然后加载全部 8 个文件，使代理能够跨文档比较 schema 和契约。
- 发现项包含精确行号引用。每轮之间会应用修复，并在可行时用定向 grep 检查。
- 研究在第 9 轮停止，当时针对全部 8 个文件和全部 7 个检查清单维度的全范围审计返回 0 个发现项。

## 结果
- 审计在约 7150 行提示规范中发现 51 个缺陷，约为每千行规范 7.1 个缺陷。
- 各轮缺陷数为 15、8、12、2、8、1、4、1 和 0。审计范围扩大后，曲线在第 3 轮和第 5 轮再次上升。
- 缺陷分类为：过期 Jira 引用 12 个（23.5%）、版本漂移 9 个（17.6%）、语义误导文本 8 个（15.7%）、缺少 Lane 7 覆盖 7 个（13.7%）、标签或契约缺口 6 个（11.8%）、跨通道 schema 不匹配 5 个（9.8%），以及公式或时序漂移 4 个（7.8%）。
- 严重性编码发现 5 个高严重性缺陷（9.8%）、32 个中严重性缺陷（62.7%）和 14 个低严重性缺陷（27.5%）。所有高严重性缺陷都是跨通道 schema 不匹配。
- 跨通道 schema 不匹配只在多文件比较成为标准做法后的第 4 到第 8 轮出现。最明显的例子是 Lane 3 和 Lane 4 之间的 `priority_score` 与 `fix_priority` 字段名不匹配，这可能导致静默运行时失败。
- 研究没有运行单次全范围对照，编写和审计使用的是同一 LLM 系列，缺陷编码由一名作者完成。因此，结果支持的是有边界的个案研究结论，而不是通用性能估计。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12280v1](https://arxiv.org/abs/2605.12280v1)
