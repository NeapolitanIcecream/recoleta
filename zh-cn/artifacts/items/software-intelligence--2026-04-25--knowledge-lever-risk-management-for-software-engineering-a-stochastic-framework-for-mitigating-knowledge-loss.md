---
source: arxiv
url: http://arxiv.org/abs/2604.23257v1
published_at: '2026-04-25T11:49:06'
authors:
- Mark Chua
- Samuel Ajila
topics:
- knowledge-management
- software-engineering
- risk-management
- monte-carlo-simulation
- llm-assisted-development
relevance_score: 0.63
run_id: materialize-outputs
language_code: zh-CN
---

# Knowledge Lever Risk Management for Software Engineering: A Stochastic Framework for Mitigating Knowledge Loss

## Summary
## 摘要
本文提出 KLRM，一种面向软件工程知识流失的风险框架，并用随机仿真模型进行测试。核心观点是，把知识共享实践当作明确的风险控制手段，可以提高项目知识资本并降低失败风险。

## 问题
- 当关键开发者离开、文档滞后，或设计决策没有记录时，软件团队会失去关键的隐性知识。
- 常规软件风险管理关注进度、范围和预算，但知识流失仍会拖慢交付、增加返工并损害质量。
- 这很重要，因为软件项目依赖人的经验、设计理由和运维知识，而这些内容不会只靠源代码保留下来。

## 方法
- 论文定义了 **Knowledge Lever Risk Management（KLRM）**：一个四阶段流程，包含 **Audit、Alignment、Activation 和 Assurance**，用于识别并降低知识相关风险。
- 它把项目知识建模为 **人力资本、结构资本和关系资本** 的合成得分，示例权重为 **0.40 H + 0.35 S + 0.25 R**。
- 知识通过三种机制变化：稳定增长、稳定衰减，以及诸如人员流失或依赖失败之类的随机冲击事件。结构知识通过编码联系从人力知识中增长。
- 该框架把软件实践作为风险控制来激活，包括结对编程、导师制、ADR、事后复盘、CI/CD 检查、依赖监控、可观测性，以及带有人类审查和验证的 LLM 辅助开发。
- 评估使用 **5,000 次运行、10 年期的 Monte Carlo 仿真**，比较基线、单一杠杆和全部激活三种情景，指标包括期望知识资本、变异系数、Sharpe 比率和危机概率。

## 结果
- **Full KLRM** 的期望期末知识资本达到 **87.39**，而 **baseline** 为 **53.35**，提升 **63.8%**。
- **危机概率** 从基线的 **0.64%** 降到 **Full KLRM** 下的 **0.00%**。摘要把这描述为几乎消除了知识危机风险。
- **风险调整后的稳定性** 提升：**Full KLRM** 的 **Sharpe ratio** 为 **12.99**，基线为 **9.73**；**CV** 为 **7.7%**，基线为 **10.3%**。
- 在单一杠杆中，**Developer Expertise Only** 表现最好，期望知识资本为 **68.19**，**CV 8.6%**，**Sharpe 11.65**，**危机概率 0.00%**。
- 其他单杠杆结果更低：**Organizational Memory Only** 的期望资本为 **59.32**，危机概率 **0.02%**；**Process Only** 为 **58.30** 和 **0.10%**；**Ecosystem Relationships** 为 **58.15** 和 **0.06%**。
- 证据来自作者的随机模型仿真。摘要未报告在真实软件工程数据集或生产环境中的验证。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23257v1](http://arxiv.org/abs/2604.23257v1)
