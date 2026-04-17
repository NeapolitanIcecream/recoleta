---
source: arxiv
url: http://arxiv.org/abs/2604.05399v2
published_at: '2026-04-07T03:49:12'
authors:
- Youngjoo Ahn
- Sangyeop Yeo
- Gijung Im
- Jongmin Lee
- Jinyoung Yeo
- Jieung Kim
topics:
- formal-verification
- automated-theorem-proving
- proof-search
- llm-for-code
- interactive-theorem-proving
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# PROMISE: Proof Automation as Structural Imitation of Human Reasoning

## Summary
## 摘要
PROMISE 面向大型形式化验证项目中的自动证明生成，这类项目里的证明很长、依赖关系复杂，当前基于 LLM 的方法在这类任务上准确率会下降。它通过寻找在结构上相似的证明状态转移来引导证明搜索，而不是依赖与已有引理或证明脚本的表面文本匹配。

## 问题
- 形式化验证可以为安全关键软件提供机器检查的正确性保证，但证明构造仍然成本很高，并且需要专家级的交互式定理证明。
- 现有基于 LLM 的证明系统通常把证明看作单次生成、下一步 tactic 预测，或基于文本的引理和证明检索；当证明在模块和文件之间存在很深的依赖关系时，这些方法会遇到困难。
- 在 seL4 或 FSCQ 这类系统级基准上，论文称以往方法对中层引理的证明覆盖率往往低于 30%，这限制了它们在已验证系统软件中的实际用途。

## 方法
- PROMISE 将证明建模为一系列证明状态以及由 tactic 触发的状态转移，然后搜索那些与当前证明状态演化方式相似的历史转移。
- 它基于证明状态的演化模式检索结构兼容的证明片段，而不只是比较定理陈述或证明文本的词面相似度。
- 它把这种结构化检索与当前活跃证明环境中的上下文感知引理检索结合起来，使用那些作用适合当前目标状态的可用引理。
- 该系统以迭代、带状态的证明搜索循环运行：提出简短的 tactic 延续，用证明助手检查，再利用检索到的状态转移轨迹扩展搜索。
- 该方法与模型无关，直接使用现成的 LLM，无需额外训练；论文使用 GPT-3.5-Turbo、Qwen2.5-Coder-7B-Instruct 进行评估，也讨论了 GPT-4.1 的设置。

## 结果
- 在 seL4 微内核验证基准上，PROMISE 报告最多提升 **26 个百分点**，论文将其描述为相比此前基于 LLM 的证明自动化方法取得 **186% 的相对增益**。
- 论文将其与 **Selene** 和 **Rango** 对比，并称在相同查询预算下，PROMISE 在**大多数设置**中优于已有方法。
- 在摘录中提到的唯一例外 **GPT-4.1/P2** 设置下，PROMISE 与最强基线结果接近，而不是领先。
- PROMISE 在不同模型规模和能力下都保持了较强表现；摘录称，在 PROMISE 内部，**Qwen2.5-Coder-7B-Instruct** 与 **GPT-3.5-Turbo** 的差距很小，而其他方法对模型更敏感。
- 摘录没有给出完整结果表、各模型的精确成功率数值，也没有给出除 **26 个百分点 / 186%** 提升这一主结论之外的逐基准细分结果。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05399v2](http://arxiv.org/abs/2604.05399v2)
