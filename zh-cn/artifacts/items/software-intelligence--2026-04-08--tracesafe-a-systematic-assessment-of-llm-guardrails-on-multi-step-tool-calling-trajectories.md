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
## 总结
这篇论文研究 LLM 防护机制能否发现多步工具调用轨迹中的不安全行为，而不只是检查用户提示词或最终答案。论文提出了 TraceSafe-Bench，这是一个用于智能体工作流中逐步安全评估的静态基准，并发现现有防护机制会漏掉很多轨迹风险，而且很依赖结构化数据处理能力。

## 问题
- 现有安全基准大多只评估最终文本输出或端到端智能体，因此会错过中间步骤里已经发生的有害工具调用，比如数据泄露、跟随提示注入或误用 API。
- 独立防护机制被广泛用于 LLM 安全，但此前不清楚它们是否能读取并拦截嵌入多步执行轨迹中的风险，这些轨迹包含 JSON 参数、工具模式和先前观察结果。
- 对自治软件智能体来说，这一点很重要，因为一个无害的最终回答，无法抵消前面已经发生的错误动作，比如把秘密发送给工具，或执行了工具输出中的恶意指令。

## 方法
- 论文构建了 **TraceSafe-Bench**，这是一个用于中间轨迹防护评估的基准，覆盖 **12 个风险类别**，包括提示注入、隐私泄露、幻觉/环境落地问题和接口不一致。
- 数据集采用 **Benign-to-Harmful Editing** 流程：先从 Berkeley Function Calling Leaderboard 中正确的多步轨迹出发，再在特定步骤注入有针对性的危险变异，同时保持其余轨迹真实。
- 一个两阶段的 **Check** 和 **Mutate** 方法先筛选每一步哪些编辑是合理的，再应用代码控制的结构编辑，例如插入或替换 JSON 键、工具名称、参数值或工具描述。
- 这个基准总共包含 **1,000 多个执行实例**，最终评估集在 **每个风险类别抽取 90 条轨迹**。作者评估了 **13 个 LLM-as-a-guard 模型** 和 **7 个专门防护机制**。
- 研究还把防护机制表现与外部基准和轨迹位置进行比较，用来检验三个判断：结构是否比对齐更重要、架构是否比规模更重要，以及更长的轨迹会不会削弱或提升检测。

## 结果
- 主要基准结果是：当前防护机制在多步轨迹安全上表现较弱。摘要报告了对 **13 个 LLM 防护模型** 和 **7 个专门防护机制**、覆盖 **12 个风险类别**、共 **1,000+ 个实例** 的评估。
- 最强的相关性分析结果是 TraceSafe 表现与 **structured-to-text benchmarks** 之间的 **Spearman 相关系数 0.79**，而它与标准 **jailbreak robustness** 的相关性接近 0。论文认为，对这项任务来说，解析和推理结构比标准对齐分数更重要。
- 论文声称，**架构对轨迹风险检测的影响大于模型规模**，而且在这个基准上，**通用 LLM 的表现优于专门的安全防护机制**。
- 论文还声称 **更长的轨迹不会降低准确率**。准确率在更长的轨迹中保持稳定，而且后期步骤甚至可能提高检测效果，因为模型能利用执行行为，而不只是静态工具定义。
- 在可见表格里，不同模型的表现差异很大，也会随类别变化。例如，**gpt-oss-120b** 在所示设置下的 **平均分为 59.34**、**unsafe 为 53.52**、**benign 为 65.17**；而 **GPT-5 mini** 的 **平均分为 51.70**、**unsafe 为 86.36**、**benign 为 17.05**，说明对不安全行为的检测和对良性样本的误拒之间存在明显权衡。
- 摘录里没有给出全部 20 个被评估系统的完整总排名，所以这里看不到精确的最高总分和完整的基线对比。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07223v1](http://arxiv.org/abs/2604.07223v1)
