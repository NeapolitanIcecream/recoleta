---
source: arxiv
url: https://arxiv.org/abs/2605.01562v2
published_at: '2026-05-02T18:16:04'
authors:
- Ahmed F. Ibrahim
topics:
- requirements-engineering
- multi-agent-systems
- neuro-symbolic-ai
- software-reuse
- llm-validation
- model-driven-engineering
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Neuro-Symbolic Agents for Hallucination-Free Requirements Reuse

## Summary
## 摘要
本文将 OOMRAM 需求复用改造成一个受约束的多智能体工作流，由 LLM 提出需求选择，由确定性的验证器拦截无效组合。这样做很重要，因为需求工具需要接收自然语言输入，同时又不能放过缺失的必选需求、互斥选择或凭空生成的 ID。

## 问题
- OOMRAM 可以复用已验证的需求，但它原本的检索方法要求精确的需求标识符，这让自然语言形式的项目愿景很难直接使用。
- 直接用 LLM 生成需求时，模型可能编造需求 ID、遗漏必选节点、选择互斥选项，或生成孤立的子节点。
- 在受监管或安全关键的需求工作中，看起来有效但结构无效的规格会带来合规和设计风险。

## 方法
- 系统将每个产品家族模型存成一个正式的 OOMRAM 矩阵：需求节点、父子边、节点类型和布尔选择约束。
- LangGraph 工作流使用四个代理：Navigator 选择下一个决策点，Interpreter 将项目愿景映射到子需求 ID，Validator 检查拟议选择，Scribe 写出最终规格。
- Validator 只是普通 Python，不调用 LLM。它强制执行核心节点包含、单适配器的恰好一个选择、多适配器的至少一个选择，以及父子一致性。
- 如果 Interpreter 提出无效选择，Validator 会拒绝并把错误返回给前一步，修正后才继续遍历。
- 子图导航在每一步只向 Interpreter 展示局部子节点，使提示长度保持恒定，遍历时间与决策点数量呈线性关系。

## 结果
- 在 2 个应用家族的 10 个项目愿景上，eRecordKeeping 约有 60 个需求，SmartHome 约有 20 个需求，所有运行都成功完成。
- 论文报告生成的最终规格实现了 100% 的需求覆盖率和 100% 的结构有效性。
- 约束违反率为 0.2%：在一次中间的 er_small_biz 运行中出现 1 次违规，随后在 Validator 拒绝后被纠正，最终输出没有违规。
- 对于带完整金标准的 3 个愿景，F1 分数分别是 er_small_biz 的 0.471、er_gov_agency 的 0.576、sh_elderly 的 0.811；这 3 个愿景都没有完全匹配，因为存在多个同样有效的可选选择。
- 10 个愿景的平均延迟为 210 秒，每个愿景平均调用 78 次 LLM；eRecordKeeping 平均 263 秒、95 次调用，SmartHome 平均 160 秒、60 次调用。
- 论文只给出了无约束 LLM 运行的定性基线证据，称在加入 Validator 循环前，系统经常出现基数错误、遗漏必选需求和孤立子节点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01562v2](https://arxiv.org/abs/2605.01562v2)
