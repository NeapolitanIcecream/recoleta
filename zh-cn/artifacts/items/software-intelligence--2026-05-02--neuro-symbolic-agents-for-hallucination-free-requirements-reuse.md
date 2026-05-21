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
本文把 OOMRAM 需求复用改为受约束的多智能体工作流：LLM 提出需求选择，确定性验证器阻止无效组合。这一点有意义，因为需求工具需要支持自然语言输入，同时不能漏掉强制需求、选择互斥项或编造 ID。

## 问题
- OOMRAM 可以复用已验证的需求，但其原始检索方法需要精确的需求标识符，因此很难处理自然语言形式的项目愿景。
- 直接用 LLM 生成需求时，模型可能编造需求 ID、遗漏强制节点、选择互斥选项，或生成没有父节点的子节点。
- 在受监管或安全敏感的需求工作中，看似有效但结构无效的规格说明会带来合规和设计风险。

## 方法
- 系统把每个产品族模型存为形式化的 OOMRAM 格：需求节点、父子边、节点类型和布尔选择约束。
- LangGraph 工作流使用四个智能体：Navigator 选择下一个决策点，Interpreter 将项目愿景映射到子需求 ID，Validator 检查拟议选择，Scribe 编写最终规格说明。
- Validator 是普通 Python 代码，不调用 LLM。它强制执行核心节点包含、单适配器恰选一个、多适配器至少选一个，以及父子一致性。
- 如果 Interpreter 提出无效选择，Validator 会拒绝该选择，并把错误发回以便修正，然后遍历继续。
- 子图导航在每一步只向 Interpreter 展示局部子节点，使提示大小保持不变，并使遍历时间随决策点数量线性增长。

## 结果
- 在 2 个应用族的 10 个项目愿景上，所有运行都成功完成：eRecordKeeping 约有 60 个需求，SmartHome 约有 20 个需求。
- 论文报告称，生成的最终规格说明达到 100% 需求覆盖率和 100% 结构有效性。
- 约束违规率为 0.2%：在一次 er_small_biz 中间运行中出现 1 次违规，经 Validator 拒绝后得到修正，因此最终输出没有违规。
- 在 3 个有完整金标准的愿景中，F1 分数分别为 er_small_biz 0.471、er_gov_agency 0.576、sh_elderly 0.811；3 个愿景的精确匹配均为 false，因为存在多个有效的可选选择。
- 10 个愿景的平均延迟为 210 秒，每个愿景平均 78 次 LLM 调用；eRecordKeeping 平均 263 秒、95 次调用，SmartHome 平均 160 秒、60 次调用。
- 对于无约束 LLM 运行，论文只给出定性基线证据，称在加入 Validator 循环前，经常出现基数错误、遗漏强制需求和没有父节点的子节点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.01562v2](https://arxiv.org/abs/2605.01562v2)
