---
source: arxiv
url: https://arxiv.org/abs/2606.18976v1
published_at: '2026-06-17T12:00:21'
authors:
- Marco Becattini
- "Niccol\xF2 Caselli"
- Matteo Minin
- Roberto Verdecchia
- Enrico Vicario
topics:
- multi-agent-llm
- software-architecture
- automated-feedback
- software-engineering-education
- evidence-grounding
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# CAPRA: Scaling Feedback on Software Architecture Deliverables with a Multi-Agent LLM System

## Summary
## 摘要
CAPRA 是一个多智能体 LLM 工具，用于审查学生的软件架构报告，并生成经过证据检查的 LaTeX 反馈。它面向架构文档，因为人工审查耗时，常规自动评分对这类材料支持较弱。

## 问题
- 软件架构交付物混合了需求、UML 图、测试、设计理由和可追溯性，教师需要花大量时间审查。
- 现有自动评估更适合代码，因为代码有测试和静态检查；架构报告是开放式且多模态的。
- 如果 LLM 编造问题，或给出没有来源证据的泛泛评论，学生可能会被误导。

## 方法
- CAPRA 使用 PyMuPDF 解析学生 PDF 中的文本，并使用 gpt-4o vision 解析 UML 和其他图，然后把图的描述插入文档文本。
- 专门的智能体检查同一份增强后的文档，关注需求、用例、架构、测试、课程要求的功能以及可追溯性链接。
- 每个问题都必须包含引用、严重程度和置信度分数。
- 确定性的证据锚定步骤会根据归一化 Levenshtein 距离进行模糊匹配，用源文本检查每条引用；匹配分数低于 0.45 的会被丢弃，置信度低于 0.65 的发现会被过滤掉。
- ConsistencyManager 智能体合并重复发现，固定的 LaTeX 模板生成最终的 PDF 反馈报告。

## 结果
- 在 10 份评估报告上，CAPRA 在严格聚合规则下通过了八项二元标准中的 88.8%；严格聚合要求两名评分者都将某项标准标为通过。
- 在宽松聚合规则下，同样的 8 项标准和 10 份报告的通过率为 91.9%。
- 两名人工评分者在 80 个判断中有 75 个一致，原始一致率为 93.75%，Cohen's kappa 为 0.582。
- CAPRA 处理每份报告略多于 4 分钟，成本约为每份 $0.44。
- 论文将其与一份架构报告的完整人工审查估计耗时 30 到 45 分钟进行了比较。
- 研究使用 10 份高分报告构建功能知识库，并使用另一组 10 份报告进行评估，因此证据仍属初步。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.18976v1](https://arxiv.org/abs/2606.18976v1)
