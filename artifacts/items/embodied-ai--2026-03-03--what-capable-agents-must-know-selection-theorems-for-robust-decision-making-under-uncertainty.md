---
source: arxiv
url: http://arxiv.org/abs/2603.02491v1
published_at: '2026-03-03T00:47:58'
authors:
- Aran Nayebi
topics:
- decision-theory
- pomdp
- world-models
- regret-analysis
- predictive-state-representations
relevance_score: 0.34
run_id: materialize-outputs
---

# What Capable Agents Must Know: Selection Theorems for Robust Decision-Making under Uncertainty

## Summary
本文证明：如果一个智能体在一类带不确定性的预测/决策任务上平均遗憾足够低，那么它**必须**在内部实现某种可预测的结构化状态，而不只是“可以”用世界模型来实现。核心贡献是把这个必要性从经典的“可构造性”推进到“被任务选择出来的表示约束”。

## Problem
- 经典 POMDP / 控制理论表明：最优控制**可以**用 belief state 或 world model 实现，但并未说明这些表示在什么条件下是**必要的**。
- 如果只看外部表现，一个架构也许能在若干任务上表现很好，却未必真的学到了可预测的内部状态；这使“能力是否迫使模型化世界”成为开放问题。
- 该问题重要，因为它关系到：高能力 agent 的内部表征是否会被鲁棒决策需求所约束，尤其在随机策略、部分可观测和任务分布评测下是否仍成立。

## Approach
- 作者提出**selection theorems**：在一族结构化、动作条件化的预测任务上，若 agent 的**平均 normalized regret** 很低，则其内部记忆/状态必须区分出足以支持预测的关键情形。
- 技术核心是把预测问题化简为二元“**betting**”决策：agent 先在两个互斥分支之间下注，再通过后续轨迹验证哪一边正确。
- 他们证明了一个遗憾分解：当测试具有足够大的 margin 时，低 regret 会直接限制 agent 在错误下注上的概率质量；因此 agent 不能把可预测上显著不同的情形混在同一内部状态里。
- 在**完全可观测**环境中，这一论证给出对干预式转移核的近似恢复；在**部分可观测**环境中，则推出 belief-like memory / predictive state 的必要性，并给出 no-aliasing 类型结论。
- 论文还讨论了结构化任务分布的额外选择效应，例如 block-structured tests 导致信息模块化、regime mixtures 导致对环境机制变化敏感的内部状态。

## Results
- **完全可观测主定理（Theorem 1）**：若对诊断目标族的平均 regret 满足 
  \(\mathbb{E}[\delta] \le \bar{\delta}\)，则由策略构造的转移估计器 \(\widehat P\) 满足平均绝对误差界：
  \(\mathbb{E}[|\widehat P_{ss'}(a)-P_{ss'}(a)|] \le 2 t_\gamma \mathbb{E}[\sqrt{P_{ss'}(a)(1-P_{ss'}(a))/n}] + \bar\delta / c(\gamma) + O(1/n)\)。
- 文中给出更粗但更直接的数值形式：
  \(\mathbb{E}[|\widehat P_{ss'}(a)-P_{ss'}(a)|] \le t_\gamma / \sqrt n + \bar\delta / c(\gamma) + O(1/n)\)。这表明误差随测试深度 **n** 增大而按 **1/\sqrt n** 缩小，并随平均遗憾 **\bar\delta** 线性变差。
- **错误下注质量控制（Lemma 1）**：在 betting 设定中，normalized regret 与错误动作概率质量 \(w\) 满足 \(\delta = w \cdot 4m/(1+2m)\)；当 margin \(m \ge \gamma\) 时，\(w \le \delta / c(\gamma)\)。这是“低 regret 强迫内部预测区分”的关键定量桥梁。
- **因果层级结果（Corollary 1）**：若环境近似满足 causal Markov process，且 \(|P - P^{do}| \le \varepsilon_{\mathrm{cMP}}\)，则 
  \(\mathbb{E}[|\widehat P_{ss'}(a)-P^{do}_{ss'}(a)|]\) 具有与上式相同的误差界，只额外加上 **\(\varepsilon_{\mathrm{cMP}}\)**；即低平均遗憾足以选择出对 **Pearl Level 2 interventions** 的近似表示。
- **负结果（Corollary 2）**：即使精确恢复了 interventional kernel，也**不能一般性恢复 Level 3 counterfactuals**；作者给出两个共享同一干预核但反事实耦合不同的结构因果模型作为反例。
- 论文没有实验数据集、benchmark 分数或经验 SOTA 对比；其“突破性结果”主要是**新的理论必要性结论**，覆盖了**随机策略、平均情形 regret、部分可观测**这几个先前结果较弱或未覆盖的设置。

## Link
- [http://arxiv.org/abs/2603.02491v1](http://arxiv.org/abs/2603.02491v1)
