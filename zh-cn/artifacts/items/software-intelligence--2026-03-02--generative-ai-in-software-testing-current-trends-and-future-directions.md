---
source: arxiv
url: http://arxiv.org/abs/2603.02141v1
published_at: '2026-03-02T18:01:43'
authors:
- Tanish Singla
- Qusay H. Mahmoud
topics:
- generative-ai
- software-testing
- llm-for-code
- prompt-engineering
- fine-tuning
- literature-review
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Generative AI in Software Testing: Current Trends and Future Directions

## Summary
本文是一篇关于生成式AI在软件测试中的综述，系统梳理了其在测试用例生成、测试预言机、测试数据与优先级排序等任务中的应用、优势与局限。论文重点强调通过微调与提示工程提升大模型测试能力，并指出该方向在近年快速升温。

## Problem
- 软件测试约占开发成本的 **50% 以上**，人工测试在系统复杂度提升和 CI/CD 场景下变得低效且昂贵。
- 传统测试常面临 **覆盖率不足**、测试数据匮乏、依赖人工经验猜测用户行为等问题，影响缺陷发现与交付质量。
- 研究上缺少专门聚焦“生成式AI如何系统性改进软件测试全流程”的综合视角，因此需要总结现状、机会与挑战。

## Approach
- 论文采用 **文献综述** 方法，围绕 4 个研究问题：软件测试中的AI类型、生成式AI的有效性、应用潜力，以及优缺点。
- 检索来源包括 **Google Scholar、SpringerLink、ScienceDirect、ResearchGate、arXiv、IEEE Xplore**，并设置纳入/排除标准；时间范围为 **2000–2024**。
- 最终筛选并分析 **59 篇**相关文献，将内容组织为生成式AI在测试中的核心任务：测试用例生成、输入/输出与oracle生成、数据生成、测试优先级排序等。
- 论文认为提升生成式AI测试能力的核心机制主要有两类：**微调（fine-tuning）** 让模型更贴近测试任务，**提示工程（prompt engineering）** 让模型在给定上下文下产出更可用的测试结果。
- 同时讨论了其适用边界与风险，如数据隐私、偏置、实现复杂度、对高质量数据与正确提示的依赖。

## Results
- 综述流程最终纳入 **59 篇**论文；作者指出相关研究在 **2019 年 OpenAI 出现后显著增长**，说明生成式AI测试成为快速升温的研究方向。
- 文中引用 **A3Test**：经微调后，相比其他预训练生成式Transformer，结果 **正确性提升 147%**、**速度提升 97.2%**。
- 文中引用 **ChatUniTest**：仅基于提示工程的方法可实现约 **59.6% 代码覆盖率**，而文中对比的其他微调LLM约为 **38%–42%**。
- 文中引用 Fan 等工作：通过提示工程，CodeX、CodeGeeX、CodeGen 在 Python、Java、JavaScript 等代码生成任务上，性能提升约 **50%–80%**。
- 论文的最强总体结论是：生成式AI可提升 **测试覆盖率、效率并降低成本**，尤其适合测试用例生成、验证与 IoT 测试；但这是一篇综述，绝大多数数字来自被综述工作，而非本文自有实验。

## Link
- [http://arxiv.org/abs/2603.02141v1](http://arxiv.org/abs/2603.02141v1)
