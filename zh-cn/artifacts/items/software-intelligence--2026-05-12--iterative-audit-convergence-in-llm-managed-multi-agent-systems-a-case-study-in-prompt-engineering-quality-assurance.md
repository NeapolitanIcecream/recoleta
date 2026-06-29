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
## 总结
论文报告了一个生产环境单案例研究：Claude 子代理对 AEGIS 这条 7 车道的 LLM 编排流水线做了提示规范审计。九轮审计发现了 51 个提示规范一致性缺陷，最后一次全范围审计没有发现问题。

## 问题
- 多代理 LLM 系统通常把行为规则、数据契约、工具权限和集成逻辑放在提示文件里。字段名写错、Jira 规则过期，或者缺少车道引用，都可能破坏代理交接或污染下游工作。
- 只做非正式的提示审查，容易漏掉跨文件缺陷，因为单独看每个文件都可能合理，但彼此之间却不一致。
- 这项研究想回答：哪些缺陷类别只在后面的扩展范围轮次里出现，以及大约 7150 行提示规范在收敛时表现如何。

## 方法
- 审计覆盖 8 个文件：7 个车道级 `PROMPT.md` 文件，共 6907 行，以及一个 245 行的共享 `TICKET_CONTRACT.md`。
- Claude 子代理使用了改写自 Weinberg 和 Freedman 式 walkthrough 的检查清单。清单覆盖版本一致性、跨车道模式、Jira 权限、标签、车道数量引用、节奏和内部矛盾。
- 早期轮次一次只看一个文件。后面的轮次把生产者和消费者文件一起加载，随后加载全部 8 个文件，这样代理可以跨文档比较模式和契约。
- 发现都附带了准确的行号引用。修复在轮次之间完成，并在可行时用定向 grep 复查。
- 研究在第 9 轮结束，因为对全部 8 个文件和 7 个检查维度做完整范围审计后没有发现问题。

## 结果
- 审计在大约 7150 行中发现了 51 个提示规范缺陷，约为每千行规范 7.1 个缺陷。
- 各轮发现数分别是 15、8、12、2、8、1、4、1 和 0。随着审计范围扩大，第 3 轮和第 5 轮的曲线又上升了。
- 缺陷分类如下：过期 Jira 引用 12 个（23.5%）、版本漂移 9 个（17.6%）、语义误导文本 8 个（15.7%）、缺少 Lane 7 覆盖 7 个（13.7%）、标签或契约缺口 6 个（11.8%）、跨车道模式不匹配 5 个（9.8%）、公式或时间节奏漂移 4 个（7.8%）。
- 严重性编码显示 5 个高严重性缺陷（9.8%）、32 个中严重性缺陷（62.7%）和 14 个低严重性缺陷（27.5%）。所有高严重性缺陷都是跨车道模式不匹配。
- 跨车道模式不匹配只在第 4 至第 8 轮出现，因为那时多文件比较已经变成常规流程。最典型的例子是 Lane 3 和 Lane 4 之间 `priority_score` 与 `fix_priority` 字段名不一致，这本来可能导致运行时静默失败。
- 这项研究没有做单次全范围对照实验，写作和审计用了同一类 LLM，也只有一位作者做缺陷编码，所以结果支持的是一个有边界的案例研究结论，而不是一般性的性能估计。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.12280v1](https://arxiv.org/abs/2605.12280v1)
