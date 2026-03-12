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
- multi-agent-systems
- retrieval-augmented-generation
- test-automation
- agile-regression-testing
- human-ai-collaboration
relevance_score: 0.86
run_id: fc07db68-6925-476b-aaeb-9e389eb4df94
---

# Human-AI Collaboration for Scaling Agile Regression Testing: An Agentic-AI Teammate from Manual to Automated Testing

## Summary
### TL;DR: 该论文提出并在西门子旗下Hacon落地验证了一种“检索增强+多智能体”的代理式AI队友，将已验证的手工测试规格自动生成为可执行系统级回归测试脚本，以提升自动化产能并缩小敏捷回归测试的手工-自动化鸿沟。

### Problem:
- 敏捷迭代中**测试规格产出速度超过自动化脚本实现速度**，导致回归覆盖不足、手工测试负担上升与发布反馈变慢。
- 在大型工业系统里，测试脚本不仅要“能跑”，还必须满足**可维护性、断言/语义准确性、团队约定与治理可追踪**等要求，现有学术/工具指导不足。
- 人类测试工程师依赖大量**隐性领域知识与非正式约定**解读规格，但AI往往难以从规格中获得同等信息量，产生误解风险。

### Approach:
- 构建“Hacon Test Automation Copilot”作为**异步批处理的AI静默队友**：每个Sprint开始前，从Jira导出并已人工审核的规格（JSON/Xray）进入输入目录，触发自动生成。
- 采用**RAG（检索增强生成）**：从历史“规格-脚本”对中检索相似示例，辅助LLM生成候选系统测试脚本。
- 采用**有界多智能体工作流**：
  - Generator 生成脚本；
  - Jenkins 环境执行；
  - Evaluator 基于执行日志按矩阵评估（语法正确、可执行、步骤覆盖、语义正确、改进空间）；
  - Reporter 输出面向经理/工程师的结构化Markdown报告，并将追踪信息记录到MLflow。
- **治理与协作机制**：AI不得直接合入回归套件；所有产物（脚本、日志、报告、trace）可追踪；最终接受/重构/重写由人类负责，强调“AI跟随、人类主导”。

### Results:
- 工业现状量化：自动化覆盖每月发布仅提升约**1–2%**；手工测试仍占总量**82–87%**，且手工测试绝对数量每次发布增长约**10–20%**（2025月度发布数据）。
- 评估规模：共**61**条测试规格（6个功能域，平均约**6**步/用例，范围**2–18**步；工作量估算**3–8** story points；输入清晰度分级A–D）。
- 人工评审数据：**5**名测试工程师对**46**个AI生成脚本进行审阅与重构，并完成Likert量表+开放反馈。
- 生产力信号（语义审查/观察）：每个脚本中约**30–50%**的AI生成代码在工程师重构时**保持不变**，表明其可作为“初稿”显著减少从零编写工作量。
- 质量/协作发现（定性为主，未给出更细量化指标）：即使规格被评为A–B（较清晰），AI仍会因隐性领域知识与团队约定缺失而**过于字面执行/误解语义**；并出现**不符合团队clean code与领域API约定**（如臆造方法名、结构不符合规范、报告不够可操作）的问题，强调**人类复核不可替代**与“人机共适应”对持续收益的重要性。

## Links
- Canonical: http://arxiv.org/abs/2603.08190v1
