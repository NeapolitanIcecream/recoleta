---
source: hn
url: https://news.ycombinator.com/item?id=47317429
published_at: '2026-03-09T23:53:01'
authors:
- maille
topics:
- email-triage
- knowledge-extraction
- read-only-ai
- privacy-first
- human-ai-interaction
relevance_score: 0.57
run_id: materialize-outputs
---

# Ask HN: Read‑only LLM tool for email triage and knowledge extraction?

## Summary
这不是一篇研究论文，而是一则产品需求帖，描述了一个**只读**的 LLM 邮件分拣与知识提取工具设想。核心诉求是在不赋予模型任何写入或发送权限的前提下，实现邮件分类、问答检索和跟进提醒。

## Problem
- 现有邮件过滤规则过于粗糙，难以处理“介于重要与不重要之间”的邮件。
- 许多 AI 邮件产品要求完整邮箱控制权限，甚至主动代发、归档或修改内容，这与用户对安全边界的要求冲突。
- 用户希望从分散的邮件线程中提取决策、任务、截止日期与停滞事项，但传统邮箱搜索难以支持自然语言层面的知识检索。

## Approach
- 提出一个**严格只读**的 LLM 邮件助手：只能读取和分析邮件，不能发送、移动、删除、归档或修改任何内容。
- 用 LLM 对来信进行细粒度分拣，如“important”“maybe useful”“likely promo”，覆盖规则过滤器难以处理的灰色地带。
- 将分散邮件线程整理为可搜索知识库，支持类似“过去 3 个月 Project X 的所有决策是什么？”的自然语言查询。
- 从长邮件链中抽取显式任务、截止日期，并识别“已停滞、需要跟进”的线程。
- 可选强调隐私优先，例如本地运行或允许用户自带 API key，以减少数据外泄风险。

## Results
- 文本**没有提供任何实验、数据集、基线或定量指标**，因此没有可报告的准确率、召回率或效率提升数字。
- 最强的具体主张是产品边界：实现“zero write permissions”，即**零写权限**，不发送、不移动、不删除、不自动归档。
- 给出的目标能力包括 3 类：邮件分拣、知识检索、跟进/行动项检测，但都属于需求描述，**未展示已实现效果或对比结果**。
- 隐私方面的具体要求是“本地运行”或“自带 API keys”，但同样没有性能或安全评测结果。

## Link
- [https://news.ycombinator.com/item?id=47317429](https://news.ycombinator.com/item?id=47317429)
