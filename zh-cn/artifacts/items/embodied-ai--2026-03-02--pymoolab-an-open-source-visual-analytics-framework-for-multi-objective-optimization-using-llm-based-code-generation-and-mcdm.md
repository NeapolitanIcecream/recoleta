---
source: arxiv
url: http://arxiv.org/abs/2603.01345v1
published_at: '2026-03-02T00:56:32'
authors:
- Thiago Santos
- Sebastiao Xavier
- Luiz Gustavo de Oliveira Carneiro
- Gustavo de Souza
topics:
- multi-objective-optimization
- visual-analytics
- llm-code-generation
- mcdm
- pymoo
- reproducibility
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# PymooLab: An Open-Source Visual Analytics Framework for Multi-Objective Optimization using LLM-Based Code Generation and MCDM

## Summary
PymooLab 是一个建立在 pymoo 之上的开源可视化分析框架，旨在降低多目标优化的编程门槛，并把实验配置、执行监控、结果分析和决策支持整合到同一工作流中。其核心特色是 LLM 辅助代码生成、可审计的可复现实验记录，以及内嵌的 MCDM 决策工具。

## Problem
- 现有多目标优化框架大多以代码为中心，用户需要手写问题定义、算法配置和分析脚本，对非程序员门槛较高。
- 这种分散式流程会削弱可复现性：超参数、评估预算、随机种子和实验元数据容易遗漏或管理不一致。
- 即使得到 Pareto 前沿，用户仍缺少统一的可视化与多准则决策支持界面，难以从候选解中做出实际选择。

## Approach
- 在 pymoo 之上构建一个 GUI + 后端桥接架构，把测试、批量实验、LLM 建模、扩展和 MCDM 分析整合为统一平台。
- 用 LLM Prompt Agent 将自然语言需求转成兼容 pymoo 的向量化 Python 代码，并通过语法检查、编译验证和热重载接入本地注册表。
- 通过 Test Module 支持单算法-单问题-单次运行的异步诊断，实时展示收敛曲线、Pareto 前沿和日志，以便在大规模实验前先排查配置问题。
- 通过 Experiment Module 管理多算法、多问题、多次重复实验，统一设置 FE 预算、种子策略和并行执行，并导出 CSV/LaTeX 统计表及 Wilcoxon/Friedman 分析。
- 在分析界面直接嵌入 MCDM（如 TOPSIS、加权和），对最终 Pareto 解集做折中解选择，并将决策快照以 JSON 保存以便审计追踪。

## Results
- 论文的主要贡献是**系统与工作流层面**，而非提出新的优化算法；给出的证据主要是架构说明、界面演示和功能对比，**未在摘录中提供标准基准上的定量性能提升数字**。
- 明确宣称支持对实验元数据的完整记录，包括**hyperparameters、evaluation budgets、random seeds**，用于强化可复现性，但未报告例如“复现率提升 X%”之类量化结果。
- 明确宣称支持通过 pymoo 原生 **JAX** 加速路径提升高维评估可扩展性，但摘录中**没有提供运行时间、吞吐量或加速倍数**。
- 在功能覆盖上，作者将自身定位为相比 pymoo 原生代码流更完整的端到端平台：集成**可视化实验、LLM 建模、统计汇总、MCDM 决策**，并公开源码地址，但没有给出与 PlatEMO、DESDEO、pagmo 等框架的量化对比实验。
- 演示性结果包括：系统能把多次实验结果自动汇总成**mean ± standard deviation**表格，支持导出**CSV**和**LaTeX**；支持非参数检验如**Wilcoxon**和**Friedman**；支持 MCDM 方法如**TOPSIS** 和**normalized weighted-sum**。这些是明确功能声明，但不是性能指标。

## Link
- [http://arxiv.org/abs/2603.01345v1](http://arxiv.org/abs/2603.01345v1)
