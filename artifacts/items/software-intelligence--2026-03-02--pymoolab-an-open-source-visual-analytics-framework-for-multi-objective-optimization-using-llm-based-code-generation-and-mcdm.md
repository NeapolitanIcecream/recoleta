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
- reproducible-workflows
relevance_score: 0.8
run_id: materialize-outputs
---

# PymooLab: An Open-Source Visual Analytics Framework for Multi-Objective Optimization using LLM-Based Code Generation and MCDM

## Summary
PymooLab 是一个建立在 pymoo 之上的开源可视化分析框架，试图把多目标优化中的建模、实验编排、结果分析和决策支持整合到同一条可复现工作流中。其核心卖点是用 LLM 生成兼容 pymoo 的代码，并在界面中直接提供实验管理与 MCDM 决策支持。

## Problem
- 现有多目标优化框架大多是**代码中心**的，用户需要手写问题定义、算法配置和后处理流程，这对缺乏软件工程背景的领域专家门槛很高。
- 实验可复现性常被破坏：超参数、评估预算、随机种子和运行元数据分散在脚本中，难以统一记录和审计。
- 即使优化算法能产出 Pareto 前沿，用户仍缺少易用的可视化与决策支持工具来理解权衡并选出折中解，这限制了实际部署价值。

## Approach
- 构建一个位于 **pymoo** 之上的 GUI + 后端桥接架构，将界面交互与优化执行解耦，同时保留与原生态 pymoo 生态的兼容性。
- 提供 **Test Module** 和 **Experiment Module**：前者用于单算法/单问题/单次运行的诊断验证，后者用于多算法、多问题、多次重复实验的统一编排、汇总和统计检验。
- 引入 **LLM Prompt Agent**，把自然语言问题描述自动转换为符合 pymoo 向量化接口的 Python 类，并通过语法检查、编译验证和热加载将其接入本地注册表。
- 内置 **MCDM** 决策支持，在分析界面中直接对最终 Pareto 近似集应用 TOPSIS 和加权和方法，输出折中点、得分与可追踪的 JSON 决策快照。
- 通过记录超参数、评估预算、随机种子、后端选择和结构化结果载荷来强化确定性执行与后续复用；对高计算量场景可走 pymoo 的 **JAX** 加速路径。

## Results
- 论文的主要贡献是**系统/框架设计与工作流演示**，摘录中**没有给出标准基准上的定量性能结果**，也没有报告如 HV、IGD、运行时间提升百分比、用户研究或消融实验数值。
- 明确宣称的能力包括：将原本需要脚本完成的多算法/多问题/多次运行实验改为 GUI 编排，并可导出 **CSV** 与 **LaTeX** 统计表。
- 在单次测试与大规模实验中，系统会自动记录 **hyperparameters、evaluation budgets、random seeds** 等元数据，以支持审计与复现实验；但未给出复现成功率或误差降低的量化指标。
- LLM 代理可把自然语言需求转成可执行 pymoo 兼容代码，文中给出的具体示例是“**实现任意目标数下使用 p-norm 的 IGD 指标**”；但未提供代码生成正确率、通过率或相对人工编码节省时间。
- MCDM 模块当前支持 **TOPSIS** 与**归一化加权和**两种方法，可在二维 Pareto 图中高亮选中的折中点，并把选择结果保存为 **JSON sidecar**；但没有给出决策质量或用户效率的定量比较。

## Link
- [http://arxiv.org/abs/2603.01345v1](http://arxiv.org/abs/2603.01345v1)
