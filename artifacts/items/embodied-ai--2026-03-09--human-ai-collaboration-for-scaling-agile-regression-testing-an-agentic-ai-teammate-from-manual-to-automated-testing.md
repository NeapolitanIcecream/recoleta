---
source: arxiv
url: http://arxiv.org/abs/2603.08190v1
published_at: '2026-03-09T10:19:13'
authors:
- Moustapha El Outmani
- Manthan Venkataramana Shenoy
- Ahmad Hatahet
- Andreas Rausch
- Tim Niklas Kniep
- Thomas Raddatz
- Benjamin King
topics:
- agentic-ai
- regression-testing
- test-automation
- rag
- human-ai-collaboration
relevance_score: 0.04
run_id: materialize-outputs
---

# Human-AI Collaboration for Scaling Agile Regression Testing: An Agentic-AI Teammate from Manual to Automated Testing

## Summary
本文研究在工业敏捷开发中，如何把大量人工测试规格更快转成可执行回归测试脚本。作者提出一个带检索增强与多代理流程的“AI队友”，用于先生成可审查的脚本草稿，再由人工把关。

## Problem
- 要解决的问题是：人工测试规格的产出速度快于自动化脚本编写速度，导致回归自动化覆盖跟不上发布节奏，增加人工测试负担并拖慢反馈循环。
- 这很重要，因为在该工业场景中，自动化覆盖每次发布仅增长 **1–2%**，但手工测试仍占总量的 **82–87%**，且手工测试绝对数量每次发布还增长 **10–20%**。
- 现有LLM/测试生成方法通常忽视真实团队中的可维护性、断言质量、项目约定，以及人机协作与治理要求。

## Approach
- 核心方法是一个**检索增强生成（RAG）+ 有界多代理工作流**的测试自动化Copilot：从已验证的测试规格直接生成系统级测试脚本初稿。
- 最简单地说，它会先从历史“规格-脚本”样例中找相似案例，再让生成代理写脚本，把脚本放到 Jenkins 里执行，然后由评估代理根据日志判断是否可用，最后由报告代理整理给测试经理和测试工程师审阅。
- 工作流是异步批处理的：团队在冲刺开始时把 Jira/Xray 规格导出成 JSON，AI 预先生成脚本、执行日志、Markdown 报告和 MLflow 追踪记录，人工再决定接受、修改或重写。
- 该机制强调**人类最终审批**：AI 不能直接把产物并入回归测试套件，所有产物都有可追踪记录，以满足治理和审计需求。

## Results
- 评估基于 **61** 个测试规格，覆盖 **6** 个功能域，平均每个用例约 **6** 个步骤（范围 **2–18**），故事点约 **3–8**；其中 **46** 个AI生成脚本被 **5** 名测试工程师审查与重构，另对其中 **10** 个脚本做了语义级人工复审。
- 作者声称的主要突破是生产率提升：人工语义审查显示，每个脚本中约 **30–50%** 的AI生成代码最终**无需修改**，说明AI显著减少了初始编写工作量。
- 论文没有给出更标准化的定量指标，如节省的精确工时、通过率、缺陷率、与人工基线的统计显著性比较；最明确的量化证据主要是 **30–50% 未改动代码占比**。
- 质性结果表明，即使输入规格被预先评为较高质量（**A–B**），AI 仍会因隐性领域知识与团队约定而产生“过于字面化”的误解，并出现幻觉方法名/API名、不符合团队 clean code 规范等问题。
- 作者将AI输出定位为接近“**初级测试工程师的第一稿**”：功能上经常可用，但通常**不能直接上线**，仍需人工在语义正确性、代码风格、复用片段和报告可操作性上进行审查与修正。

## Link
- [http://arxiv.org/abs/2603.08190v1](http://arxiv.org/abs/2603.08190v1)
