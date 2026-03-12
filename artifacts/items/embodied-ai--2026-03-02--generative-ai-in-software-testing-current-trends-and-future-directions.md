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
- llm-for-testing
- prompt-engineering
- fine-tuning
relevance_score: 0.03
run_id: materialize-outputs
---

# Generative AI in Software Testing: Current Trends and Future Directions

## Summary
这是一篇关于生成式AI在软件测试中应用现状与未来方向的综述论文。文章系统梳理了生成式AI在测试用例生成、测试数据、测试预言机和测试优先级等任务中的潜力、方法与挑战。

## Problem
- 软件测试成本高、人工密集，文中指出其可占开发成本 **50%以上**，在持续集成/持续交付环境下更难扩展。
- 传统手工测试和脚本化自动化常面临 **覆盖率不足、测试数据缺乏、效率低** 等问题，难以跟上软件复杂度增长。
- 研究界虽已有AI用于测试的工作，但缺少一篇专门聚焦 **生成式AI为何适合软件测试、具体能做什么、还有哪些缺口** 的综合性梳理。

## Approach
- 论文采用 **文献综述/系统化调研** 方法，而不是提出新的测试算法；围绕4个研究问题分析AI类型、生成式AI有效性、应用潜力及优缺点。
- 作者从 **Google Scholar、ScienceDirect、arXiv、IEEE Xplore** 等来源检索文献，并用预设的纳入/排除标准筛选英文、与软件测试相关、时间范围 **2000–2024** 的材料。
- 最终纳入 **59篇** 论文，并按主题整理生成式AI在测试中的应用，包括 **test case generation、input generation、oracle generation、test data creation、test case prioritization** 等。
- 文章进一步总结两类核心机制：**fine-tuning**（用测试/代码数据把预训练LLM调成更适合测试任务）和 **prompt engineering**（通过更好的提示词让模型生成更可用的测试结果）。
- 核心思想可简单理解为：让大语言模型“读懂需求和代码”，再自动生成测试相关内容，并通过验证、修复和迭代提升可用性。

## Results
- 这是综述论文，**没有统一自建实验基准**；其主要结果来自所回顾文献中的代表性数字与趋势总结。
- 文献筛选后共纳入 **59篇** 相关论文；作者称在 **2019年后**，随着OpenAI相关模型兴起，相关研究发表数量显著增长。
- 在被引用的工作中，**A3Test** 经过微调后，相比其他预训练生成式Transformer，作者报告其结果 **正确性提升147%**、**速度提升97.2%**。
- 在被引用的工作中，**ChatUniTest** 采用提示工程与自动修复流程，报告 **代码覆盖率约59.6%**，而文中提到的其他微调LLM大约为 **38%–42%**。
- 文中还引用 Fan 等人的结论：通过提示工程，代码生成相关性能在 **CodeX、CodeGeeX、CodeGen** 上可提升 **50%–80%**，覆盖 **Python、Java、JavaScript** 等语言。
- 论文的最强结论是：生成式AI在提高测试覆盖率、效率和成本控制上具有明显潜力，但仍受 **提示质量、数据隐私、实现复杂度、偏差与数据需求** 等限制。

## Link
- [http://arxiv.org/abs/2603.02141v1](http://arxiv.org/abs/2603.02141v1)
