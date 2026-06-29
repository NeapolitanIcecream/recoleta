---
source: arxiv
url: http://arxiv.org/abs/2604.16790v1
published_at: '2026-04-18T02:35:05'
authors:
- Zixiao Zhao
- Amirreza Esmaeili
- Fatemeh Fard
topics:
- llm-as-a-judge
- code-intelligence
- software-engineering
- evaluation-bias
- agentic-workflows
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Bias in the Loop: Auditing LLM-as-a-Judge for Software Engineering

## Summary
## 摘要
本文审计了用于代码评估的 LLM 裁判，发现当提示词加入表面线索时，它们的判决会大幅变化。作者认为，只看裁判准确率还不够；研究还应报告偏置敏感性和重复性。

## 问题
- 在人工审查或可执行测试有限时，LLM 裁判会被用来给代码候选项排序，尤其是在基于代理的软件工程工作流中。
- 同一裁判在重复运行中，或者在提示词做了很小改动后，可能会翻转决定，即使代码本身没有变化。
- 这很重要，因为提示词带来的伪影会改变基准结论、模型排名和补丁选择决策。

## 方法
- 论文研究了三个任务上的成对代码评判：代码生成、代码修复和单元测试生成。
- 研究采用以测量为先的设置：固定候选代码，只改裁判提示词，一次只注入一种偏置。
- 偏置集合包含 12 种提示级干预，例如位置/顺序、冗长度、权威性/来源、干扰、思维链、自我增强，以及“改进版”线索。
- 作者评估了两个性质：每种偏置条件下的微观准确率，以及在同一提示词下同一案例被评判两次时的重测一致率。
- 他们测试了开源的 Qwen 系裁判，也报告了闭源 GPT 系裁判的相似模式。

## 结果
- 主要结论：即使底层代码片段不变，裁判决定也对提示词偏置非常敏感。
- 论文指出，当提示偏置支持标准答案时，一些偏置会提高准确率；当它们支持错误答案时，准确率会大幅下降。某些设置下，这些变化足以改变任务层面的结论和模型相对排名。
- 闭源 GPT 系裁判报告的最大具体波动出现在 TestGen 上：干扰使准确率从 77.46% 降到 62.51%。
- 响应可靠性也会随裁判模型而变：Qwen2.5-Coder-3B 在约 99% 的输入上返回所需的 A/B 判决，而通用 Qwen 配置只有约 44%，而且经常一直输出自由形式文本直到上下文长度上限。
- 摘要和摘录都说代码修复任务的裁判准确率通常较高，但这里没有给出完整的按任务划分准确率表。
- 论文建议加入明确控制，例如 A/B 顺序交换和受控提示扰动，并要求在报告准确率的同时报告偏置敏感性。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.16790v1](http://arxiv.org/abs/2604.16790v1)
