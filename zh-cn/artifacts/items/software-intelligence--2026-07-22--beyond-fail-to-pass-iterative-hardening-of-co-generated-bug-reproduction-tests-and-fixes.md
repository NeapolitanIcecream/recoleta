---
source: arxiv
url: https://arxiv.org/abs/2607.19843v1
published_at: '2026-07-22T07:30:07'
authors:
- Yuhao Tan
- Zhibang Yang
- Fangkai Yang
- Yuan Yao
- Yu Kang
- Lu Wang
- Pu Zhao
- Xin Zhang
- Xiaoxing Ma
- Qingwei Lin
- Saravan Rajmohan
- Dongmei Zhang
topics:
- automated-program-repair
- code-intelligence
- bug-reproduction-tests
- mutation-testing
- multi-agent-software-engineering
- automated-software-production
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Fail-to-Pass: Iterative Hardening of Co-Generated Bug Reproduction Tests and Fixes

## Summary
## 摘要
CoHarden 通过针对可能的错误补丁迭代强化 bug reproduction tests，而不是仅依据 fail-to-pass 行为评判测试，从而改进自动化程序修复。在包含 433 个实例的 SWE-bench Verified ∩ SWT-bench Verified 设置中，该方法取得了 69.4% 的 Resolved 和 78.9% 的测试 F→P，相比使用相同骨干模型的协同生成基线，分别高出 8.0 和 6.2 个百分点。

## 问题
- Bug reproduction tests 通常只通过 fail-to-pass（F→P）进行评估：在有 bug 的代码上失败，在黄金修复上通过。即使某个宽松测试同时接受看似合理但实际错误的修复，这种标准也可能将其判定为成功。
- 宽松测试无法为后续修复提供帮助，而不匹配的测试可能误导修复代理。在联合生成测试和修复时，两类错误还可能相互强化。
- 这一问题之所以重要，是因为通过 reproduction test 并不一定能证明自动生成的补丁修复了报告中的行为或其根本原因。

## 方法
- Mutation Patch Evaluation（MPE）让生成的测试运行在黄金修复的语义变异版本上，并使用 2×2 测试结果矩阵将测试分类为 Rigorous、Lax 或 Misaligned。Laxity rate β/total 用于衡量生成测试接受但参考测试拒绝的变异补丁比例；主要阈值为 τ=0.202。
- 该研究将 BRT 质量与后续效用分开评估。在 1,104 对 F→P BRT/修复和 474 对非 F→P BRT/修复上，研究者测量了将测试注入 OpenHands + GPT-5-mini 修复代理后 Resolved 性能的配对变化。
- CoHarden 首先生成 reproduction test，而不修改源代码。随后，它最多执行五轮强化：对当前修复进行变异，依据当前测试和前一轮测试评估变异版本，并持续更新测试—修复对，直到时间性 Laxity rate 不超过 0.2。
- 该方法使用四种有针对性的变异算子，每个完整轮次生成 12 个候选变异版本。在部署时无法获得黄金制品，因此改用基于前一轮测试、无需参考信息的 Temporal Matrix。

## 结果
- 在注入的 F→P 测试中，Rigorous 测试将 Resolved 从 67.3% 提高到 75.8%（+8.5 个百分点）；Lax 测试没有带来变化（69.5% 到 69.5%，+0.0）。Misaligned 测试使 Resolved 下降 3.6 个百分点，从 44.5% 降至 40.9%。
- 在协同生成中，联合失败率为 19.9%，是独立假设下根据测试错误和修复错误预测的 10.6% 的 1.87 倍。在 166 个未解决实例中，有 80 个的测试通过了 F→P，但对应的修复是错误的。
- 在包含 433 个实例的 SWE-bench Verified ∩ SWT-bench Verified 评估中，CoHarden 达到 69.4% 的 Resolved 和 78.9% 的 F→P。OpenHands + Cogen 达到 61.4% 的 Resolved 和 72.7% 的 F→P；InfCode 分别达到 61.5% 和 69.6%。据报告，CoHarden 相比 OpenHands + Cogen 的提升分别为 +8.0 和 +6.2 个百分点。
- CoHarden 的单实例成本为 $0.84，InfCode 为 $0.77，Agent-CoEvo 为 $0.88；变异生成占最终运行成本的 9.5%。变异池只是对可能错误修复的近似，因此 Rigorous/Lax 评估取决于所使用的算子和采样方式。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19843v1](https://arxiv.org/abs/2607.19843v1)
