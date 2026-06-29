---
source: arxiv
url: https://arxiv.org/abs/2606.16999v1
published_at: '2026-06-15T17:36:23'
authors:
- Mehmet Iscan
topics:
- code-generation
- code-intelligence
- post-hoc-selection
- software-evaluation
- frozen-code-models
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Selection Without Signal, Recovery Through Expression: A Measurement Study of Post-Hoc Falsification Operators for Frozen Small Code Models

## Summary
## 摘要
本文发现，在相同计算量下，语义后处理算子不能让冻结的小型代码模型超过 Best-of-N，而评测与提取流程的修复可以找回被漏掉的正确代码。最有用的结果是 M1：一个提取和签名对齐步骤，它在不增加生成次数的情况下提高准确率。

## 问题
- 约 0.5B 到 1.5B 参数的冻结本地代码模型经常生成看似合理的代码，这些代码能通过可见测试，但会在隐藏测试上失败，限制了它们在离线和隐私受限编码工具中的使用。
- 许多后处理方法试图在不训练的情况下选择、验证、修复或反驳生成候选，但还不清楚它们是否比多采样候选提供更多信号。
- 实际风险是把工程精力浪费在语义重排序上，而候选池中可能没有正确程序，或者通过可见测试的候选在没有隐藏测试泄漏的情况下无法区分。

## 方法
- 研究冻结模型，采样一个共享候选池，只向每个算子提供提示、公开测试和候选，并用隐藏测试将返回程序与 Best-of-N 比较。
- Best-of-N 返回第一个通过公开测试的候选。每个被测试算子获得相同的生成器计算量，因此收益不能来自额外样本。
- 研究评估了 26 个语义输出空间算子，覆盖选择、验证、修复、反例搜索、淘汰、可靠否决、组合、生成条件控制和计算分配。
- 研究单独测试了 M1。M1 找回标准提取器漏掉的代码，并把单个已定义函数名对齐到公开测试签名。
- 研究还测试了 ACE，这是一种自适应共识提前停止规则，在足够多候选达成一致时节省采样工作。

## 结果
- 在测试的模型单元和基准上，26 个语义后处理算子在相同计算量下都没有让留出集准确率超过 Best-of-N。
- 困难任务上出现覆盖墙：k=16 时，30 个任务中仍有 16 个任务的采样池里没有隐藏测试正确的候选。
- 基于共识的选择几乎没有改进空间：在两个可使用可靠否决的陷阱基准上，模型在 0/10 和 2/16 个任务中触发了相应 bug，且从未成为共识多数；约 83% 的真实 bug 对可靠变形关系不可见。
- 论文证明了无害声明的有限样本下限：在观察到零伤害时，要以 delta = 0.10 认证总体伤害率 <= 0.05，需要 n >= 45。
- M1 是唯一已部署的准确率收益。在 DeepSeek-Coder-1.3B 上，它将 HumanEval+ 从 29 个任务提高到 41 个任务，增益为 +12，p = 2.4e-4，b10 = 0；在 MBPP+ 上，它将 128 个任务提高到 161 个任务，增益为 +33，p = 1.2e-10，b10 = 0。
- ACE 在零伤害运行点节省约 19% 的样本；更激进的设置节省约 64%，但出现可测量回退，b10 = 2。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.16999v1](https://arxiv.org/abs/2606.16999v1)
