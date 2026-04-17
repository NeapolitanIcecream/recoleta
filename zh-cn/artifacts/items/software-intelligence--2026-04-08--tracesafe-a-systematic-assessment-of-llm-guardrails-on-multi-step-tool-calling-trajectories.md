---
source: arxiv
url: http://arxiv.org/abs/2604.07223v1
published_at: '2026-04-08T15:46:14'
authors:
- Yen-Shan Chen
- Sian-Yao Huang
- Cheng-Lin Yang
- Yun-Nung Chen
topics:
- llm-safety
- agentic-workflows
- tool-calling
- guardrails
- benchmarking
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# TraceSafe: A Systematic Assessment of LLM Guardrails on Multi-Step Tool-Calling Trajectories

## Summary
## 概要
本文研究 LLM 护栏能否在多步工具调用轨迹内部识别不安全行为，而不是只筛查用户提示或最终答案。论文提出了 TraceSafe-Bench，这是一个用于评估代理工作流中步骤级安全性的静态基准，并发现现有护栏会漏掉许多轨迹风险，而且很依赖结构化数据处理能力。

## 问题
- 现有安全基准大多评估最终文本输出或端到端代理，因此会漏掉有害的中间工具调用，而这些调用已经可能导致数据泄露、遵循提示注入，或误用 API。
- 独立护栏已被广泛用于 LLM 安全，但此前并不清楚它们是否能读取并拦截嵌入在多步执行轨迹中的风险，这些轨迹包含 JSON 参数、工具 schema 和先前观察结果。
- 这对自主软件代理很重要，因为即使最终答案看起来无害，也无法抵消更早一步的错误行为，例如把机密发送给工具，或遵循来自工具输出的恶意指令。

## 方法
- 论文构建了 **TraceSafe-Bench**，这是一个用于评估轨迹中途护栏能力的基准，覆盖 **12 个风险类别**，包括提示注入、隐私泄露、幻觉/环境锚定错误，以及接口不一致。
- 数据集使用 **Benign-to-Harmful Editing** 流程：从 Berkeley Function Calling Leaderboard 中正确的多步轨迹开始，然后在特定步骤注入定向的不安全变异，同时保持轨迹其余部分仍然逼真。
- 一个两阶段的 **Check** 和 **Mutate** 方法先筛选每一步中哪些编辑是合理的，然后再应用由代码控制的结构性编辑，例如插入或替换 JSON 键、工具名称、参数值或工具描述。
- 该基准总计包含 **1,000 多个执行实例**，最终评估集为每个风险类别抽样 **90 条轨迹**。作者评估了 **13 个 LLM-as-a-guard 模型** 和 **7 个专用护栏**。
- 研究还将护栏表现与外部基准以及轨迹位置进行比较，以检验三个判断：结构是否比对齐更重要，架构是否比规模更重要，以及更长的轨迹会降低还是提升检测效果。

## 结果
- 主要基准结果是：现有护栏在多步轨迹安全上表现较弱。摘要报告称，评估覆盖 **12 个风险类别**、**1,000+ 个实例**，测试了 **13 个 LLM 护栏模型** 和 **7 个专用护栏**。
- 文中最强的分析结果是：TraceSafe 表现与 **structured-to-text benchmarks** 的 **Spearman 相关系数为 0.79**，而与标准 **jailbreak robustness** 的相关性接近于零。论文据此认为，在这项任务中，解析结构并基于结构推理，比标准对齐分数更重要。
- 论文称，在轨迹风险检测中，**架构比模型规模更重要**，而且 **通用 LLM 的表现优于专用安全护栏**。
- 论文称，**更长的轨迹不会降低准确率**。在更长的轨迹上，准确率保持稳定，后期步骤甚至可能提升检测效果，因为模型可以利用执行行为，而不只依赖静态工具定义。
- 从可见表格来看，模型表现不均衡，并且对类别很敏感。例如，在所示设置下，**gpt-oss-120b** 的 **平均值为 59.34**、**unsafe 为 53.52**、**benign 为 65.17**；而 **GPT-5 mini** 的 **平均值为 51.70**、**unsafe 为 86.36**、**benign 为 17.05**，这说明不安全检测与良性拒绝之间存在明显权衡。
- 这段摘录没有给出全部 20 个评估系统的完整汇总排名，因此这里无法确定整体最佳分数，也无法看到完整的基线比较。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07223v1](http://arxiv.org/abs/2604.07223v1)
