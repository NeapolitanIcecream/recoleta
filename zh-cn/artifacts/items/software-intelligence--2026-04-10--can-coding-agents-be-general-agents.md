---
source: arxiv
url: http://arxiv.org/abs/2604.13107v1
published_at: '2026-04-10T22:39:51'
authors:
- Maksim Ivanov
- Abhijay Rana
- Gokul Prabhakaran
topics:
- coding-agents
- business-process-automation
- enterprise-resource-planning
- agent-evaluation
- code-execution
- human-ai-interaction
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Can Coding Agents Be General Agents?

## Summary
## 总结
本文测试编码代理是否能处理通用业务工作流，而不只是软件任务。在一个 Odoo ERP 案例研究中，这些代理能稳定完成简单任务，但在更难的工作流上就会出问题，尤其是在业务规则必须和代码执行保持一致时。

## 问题
- 现有基准把问题拆成两半：像 SWE-Bench 和 Terminal-Bench 这样的软件基准测试代码和系统能力，而像 BFCL 和 $\tau$-bench 这样的工具使用与策略基准会简化执行层。
- 真实的业务自动化需要两边同时成立：理解业务请求和政策，检查实时系统状态，决定应该发生什么，然后正确修改软件状态。
- 论文要回答编码代理是否能在真实 ERP 里端到端完成这件事，因为用户已经把它们用在软件工程之外的业务工作上。

## 方法
- 作者把编码代理的泛化定义为业务层和代码层之间的双向转换：读取业务目标，用代码检查系统，规划业务动作，再把改动写回系统。
- 他们在 **Odoo 19.0 Community Edition** 中搭建了一个案例研究环境，里面填入了销售、库存、制造、采购和人力资源的真实公司数据。
- 任务是带有明确约束和政策规则的自然语言业务工作流。每个场景至少需要 **2 个相互依赖的决策** 和至少 **2 个相互作用的约束**；更难的场景需要 **5 个以上决策** 和 **5 个以上约束**。
- 代理只能使用 **bash 工具**、数据库凭据、一个工作区，以及五个 Odoo 数据模型的示例。它必须自己映射 ERP 并编写脚本。他们在最高推理设置下测试了 **GPT-5** 和 **Claude Sonnet 4.5**。
- 评估把最终 PostgreSQL 状态和真实标准进行对比，标准包括 **约束处理、资源优化、可追溯性和政策遵循**。

## 结果
- 在 **10 个简单场景** 的第一次试验中，Claude Sonnet 4.5 编码代理在验证器上的得分 **超过 80%**，并且能稳定完成创建销售订单、选择最便宜的供应商和生成发票等任务。
- 这项研究评估了 **20 个场景**，难度范围从 **Easy 到 Hardest**。随着约束数量增加，表现会下降。
- 论文报告了一个定性上的模型分化：**GPT-5** 经常给出与 Claude Sonnet 4.5 相当或更好的业务计划，但它的错误 API 调用更多，拉低了总分。
- 在更复杂的场景中，代理会从可行但次优的计划退化到在约束满足上直接失败，可追溯性也会随着工作流变复杂而变差。
- 论文归纳出四种反复出现的失败模式：用于政策实现的 **lazy code heuristics**、**business-layer hallucinations**、**ignored policy constraints**，以及把代码执行成功误当成业务结果正确的 **overconfidence**。
- 摘要没有给出按模型和难度划分的完整数值表，因此最强的量化结论是 **10 个简单场景上超过 80%**，以及一组 **20 个场景**，并且在更难任务上有明显退化。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13107v1](http://arxiv.org/abs/2604.13107v1)
