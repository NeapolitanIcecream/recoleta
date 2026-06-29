---
source: arxiv
url: http://arxiv.org/abs/2604.13946v2
published_at: '2026-04-15T14:58:26'
authors:
- Duy Tung Doan
- Quang Huy Phung
- Dzung Nguyen
- Khac-Hoai Nam Bui
topics:
- multi-agent-code-generation
- code-intelligence
- plan-code-coevolution
- automated-debugging
- llm-agents
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# CollabCoder: Plan-Code Co-Evolution via Collaborative Decision-Making for Efficient Code Generation

## Summary
## 摘要
CollabCoder 是一种多智能体代码生成方法。在调试过程中，它会更新计划或代码，而不是把最初的计划固定不变。论文称，这种方法在标准和竞赛级基准上提高了 Pass@1，同时比近期智能体基线减少了 token 使用量和 API 调用次数。

## 问题
- 现有的智能体代码生成器常常把初始计划固定下来，即使测试失败表明计划本身有误或不完整。
- 许多系统用反应式的试错循环来调试代码，错误归因弱，也很少利用之前失败的尝试。
- 这在 LiveCodeBench 和 xCodeEval 这类基准上的复杂编程任务里很重要，因为这类任务既需要正确的高层推理，也需要正确实现；重复试错会增加成本，还是会漏掉缺陷。

## 方法
- CollabCoder 使用三个智能体：规划智能体、编码智能体和调试智能体。
- 调试智能体包含一个协作决策模块。它在每次迭代中分析三个信号：计划质量、代码质量和计划与代码的一致性。
- 然后它为下一步选择一个动作：修改计划或修改代码。这个选择通过聚合置信度和一致性分数，并使用固定信任权重完成：计划 0.4，代码 0.3，一致性 0.3。
- 一个 Reasoning Trajectory 模块会在迭代之间保存调试历史，把过去的失败和当前测试反馈转成更新后的修复策略，这样系统就不会重复无效修复。
- 这个过程会迭代进行，直到测试通过或达到迭代预算；论文对 CollabCoder 使用 5 次迭代。

## 结果
- 在使用 **Qwen2.5-Coder-32B** 的基础代码生成基准上，CollabCoder 的 **平均 Pass@1 为 82.50**，高于 **CodeSIM 的 80.22**、**MapCoder 的 79.84** 和 **ThinkCoder 的 77.02**。它的 **token I/O 为 2468.22 / 1606.88**，**API 调用为 4.12 次**；相比之下，**CodeSIM 为 2191.03 / 2593.04** 和 **4.87 次**，**MapCoder 为 5848.39 / 3309.55** 和 **9.05 次**。
- 使用 **GPT-4o mini** 时，CollabCoder 的 **平均 Pass@1 达到 83.25**，高于 **CodeSIM 的 81.52** 和 **MapCoder 的 77.80**。它在各数据集上的分数是 **96.34 HE**、**84.76 HE-ET**、**91.69 MBPP**、**60.20 MBPP-ET**。
- 使用 **Seed-Coder-8B** 时，CollabCoder 的 **平均 Pass@1 为 76.26**，略高于 **CodeSIM 的 75.51**，也高于 **ThinkCoder 的 71.08** 和 **MapCoder 的 68.78**；它使用 **5.06 次 API 调用**，而 CodeSIM 为 **6.69 次**，MapCoder 为 **9.84 次**。
- 在使用 **GPT-4o mini** 的竞赛级基准上，CollabCoder 在 **LiveCodeBench 上的 Pass@1 为 41.96**，在 **xCodeEval 上为 47.16**，**平均为 44.56**。基线是 **CodeSIM 平均 39.53**，**MapCoder 平均 37.70**。
- 在这些竞赛基准上，CollabCoder 使用 **12.27 次 API 调用**，低于 **CodeSIM 的 17.16 次** 和 **MapCoder 的 22.41 次**；它的 token I/O 为 **15155.93 / 4491.37**，而 CodeSIM 为 **20907.82 / 13151.10**，MapCoder 为 **28437.65 / 17692.18**。
- 摘要把在 **LiveCodeBench** 和 **xCodeEval** 上相对强基线的提升概括为 **11-20%**，并且平均每次执行减少 **4-10 次 API 调用**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13946v2](http://arxiv.org/abs/2604.13946v2)
