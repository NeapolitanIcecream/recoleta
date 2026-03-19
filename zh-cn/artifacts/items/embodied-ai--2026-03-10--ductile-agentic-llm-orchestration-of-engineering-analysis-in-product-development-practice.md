---
source: arxiv
url: http://arxiv.org/abs/2603.10249v1
published_at: '2026-03-10T22:00:47'
authors:
- Alejandro Pradas-Gomez
- Arindam Brahma
- Ola Isaksson
topics:
- llm-agents
- engineering-automation
- workflow-orchestration
- aerospace-analysis
- human-in-the-loop
relevance_score: 0.09
run_id: materialize-outputs
language_code: zh-CN
---

# DUCTILE: Agentic LLM Orchestration of Engineering Analysis in Product Development Practice

## Summary
本文提出 DUCTILE，一种用于产品开发中工程分析自动化的 LLM 代理编排方法，将“可适应的流程协调”和“已验证工具的确定性执行”分离。其目标是在输入格式、单位、命名和方法发生常见变化时，仍能保持工程分析流程可用、可审计且由工程师监督。

## Problem
- 传统工程分析自动化依赖预先定义的刚性接口、脚本和工作流；当工具、数据格式、单位、命名或流程稍有变化时，自动化就容易失效。
- 在航空等安全关键行业，这种脆弱性会把工程师时间消耗在数据清洗、工具衔接和脚本修补上，而不是关键工程判断上。
- 仅靠增加更多规则会让系统更复杂、更难维护；仅靠专家人工适配又慢且依赖个体经验，难以规模化。

## Approach
- DUCTILE 的核心机制是：让 LLM 代理负责“读文档、看输入、决定接下来该走哪条处理路径”，但真正的工程计算仍由经过验证的确定性工具执行。
- 代理根据记录在上下文中的设计实践、工具文档和输入数据，自适应地生成/调用处理代码与工具链，而不是把所有可能情况事先硬编码成固定流程。
- 系统强调人类监督：工程师审查计划、监督执行并对输出做最终判断，满足可追踪、可审计和责任归属要求。
- 论文还给出一套工程级要求与评估原则，包括 inspectability、reproducibility、deterministic execution boundary、traceability、human oversight、robustness to variability 等。

## Results
- 在一家航空制造商的工业结构分析任务中，DUCTILE 处理了 **4 类** 会让传统脚本流水线失效的输入偏差：**格式、单位、命名规范和方法差异**。
- 论文声明该方法在 **10 次独立运行** 中接受评估，并由 **2 名** 监督风格不同的工程师参与部署/使用。
- 结果依据专家定义的验收标准进行评估；作者声称系统能够在重复独立运行中产出**正确且方法学合规**的结果。
- 文本未提供更细的定量指标，如准确率、通过率、时间节省百分比、与具体基线的数值差距，因此无法报告更详细的 benchmark 数字。
- 论文的最强具体主张是：相较会因常规输入变化而中断的传统脚本式自动化，DUCTILE 能在不修改已验证工程工具的前提下吸收这些变化，并保持透明与可审计。

## Link
- [http://arxiv.org/abs/2603.10249v1](http://arxiv.org/abs/2603.10249v1)
