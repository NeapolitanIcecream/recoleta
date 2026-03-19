---
source: arxiv
url: http://arxiv.org/abs/2603.01409v1
published_at: '2026-03-02T03:22:44'
authors:
- Sicheng Zhu
- Jiajun Wang
- Jiawei Ai
- Xin Li
topics:
- reinforcement-learning
- unit-test-generation
- mutation-testing
- code-verification
- llm-for-code
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# MIST-RL: Mutation-based Incremental Suite Testing via Reinforcement Learning

## Summary
本文提出 MIST-RL，用强化学习按“新增效用”而不是“测试数量”来逐步生成单元测试，从而减少冗余并提升代码验证质量。其核心价值是在更短测试套件下获得更强的故障发现能力，并改进下游代码重排序。

## Problem
- 现有 LLM 单元测试生成大多依赖“多生成一些测试”，但更多测试很快出现收益递减，后期样本大量语义重复。
- 冗余测试会造成 **test bloat**：增加推理与执行成本，却不能有效发现新的 bug，也削弱测试作为代码 verifier 的区分能力。
- 这很重要，因为 LLM 生成代码常常首轮不正确；若 verifier 不够“激进”，就难以筛掉看似合理但实际有细微逻辑错误的候选程序。

## Approach
- 将测试套件生成建模为**序列决策过程**：模型每一步生成一个新测试，并利用此前测试已杀死的 mutants 作为历史状态。
- 用**增量变异奖励**驱动学习：只有当新测试杀死了此前未杀死的 mutant 时才获得奖励；重复覆盖旧 mutant 的测试基本没有收益。
- 加入**动态冗余惩罚**：若测试可运行但没有带来新的 fault detection，则按序列位置施加随时间增长的惩罚，迫使模型尽早生成高价值测试。
- 奖励函数还区分三种情况：测试编译/执行失败给重罚；无新增贡献给惩罚；有新增贡献时按“断言质量 + 新杀死 mutant 的加权数量”给正奖励。
- 采用 **GRPO** 进行策略优化，并构建基于 Python AST 的轻量 mutation engine 来高效生成/评估 mutants。

## Results
- 在 **HumanEval+** 上，MIST-RL 的 **Mutant Kill Rate = 74.03%**，相比 **CodeRM-8B 的 45.53%** 提升 **+28.5 个百分点**，也高于 **Qwen3-14B 的 58.69%**；平均测试套件长度 **6.14 vs. 7.61**，较 CodeRM-8B 缩短 **19.3%**。
- 在 **MBPP+** 上，MIST-RL 的 **Mutant Kill Rate = 70.27%**，高于 **CodeRM-8B 的 61.08%** 和 **Qwen3-14B 的 66.50%**；平均长度 **5.17 vs. 6.55**，较 CodeRM-8B 缩短 **21.1%**。
- 在 **DS-1000** 上，MIST-RL 达到 **57.90%** mutant kill，优于 **CodeRM-8B 的 49.08%** 和 **Qwen3-14B 的 53.20%**；平均长度 **5.78**，也短于 CodeRM-8B 的 **7.37**。
- 作为下游 verifier，在 **HumanEval+ 代码重排序** 中，候选数 **N=10** 时 **Pass@1 = 48.78%**，优于 **CodeRM-8B 的 45.73%** 和 **Qwen3-14B 的 44.51%**，比 SOTA 基线提升 **3.05 个百分点**。
- 在 **N=20** 的重排序设置下，MIST-RL 仍领先：**62.80%**，对比 **CodeRM-8B 的 61.59%** 与 **Qwen3-14B 的 55.49%**。
- 消融实验表明：去掉增量奖励后，HumanEval+ 的 mutation score 从 **74.03% 降到 65.1%**；去掉动态惩罚后，平均套件长度从 **6.14 暴涨到 14.20**，说明两者分别对效果和去冗余都关键。

## Link
- [http://arxiv.org/abs/2603.01409v1](http://arxiv.org/abs/2603.01409v1)
