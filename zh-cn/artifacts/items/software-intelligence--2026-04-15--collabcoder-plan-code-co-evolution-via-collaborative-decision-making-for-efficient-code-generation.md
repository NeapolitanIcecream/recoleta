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
CollabCoder 是一种多智能体代码生成方法。在调试过程中，它会根据情况更新计划或代码，而不是把初始计划固定不变。论文称，这种做法在标准基准和竞赛级基准上提高了 Pass@1，同时相比近期的智能体基线减少了 token 使用量和 API 调用次数。

## 问题
- 现有的智能体式代码生成系统常常把初始计划固定下来，即使测试失败已经表明计划本身有误或不完整。
- 许多系统以被动的试错循环来调试代码，错误归因能力较弱，也很少利用之前失败尝试中的信息。
- 这很重要，因为 LiveCodeBench 和 xCodeEval 这类基准中的复杂编程任务既需要正确的高层推理，也需要正确实现；无效的重复尝试会增加成本，而且仍然可能漏掉 bug。

## 方法
- CollabCoder 使用三个智能体：规划智能体、编码智能体和调试智能体。
- 调试智能体包含一个协同决策模块，每一轮会分析三个信号：计划质量、代码质量，以及计划与代码的一致性。
- 然后它为下一步选择一个动作：修改计划或修改代码。这个选择通过汇总置信度和一致性分数来完成，并使用固定信任权重：计划 0.4、代码 0.3、一致性 0.3。
- 推理轨迹模块会在多轮迭代中保存调试历史，并把过去的失败记录与当前测试反馈转成更新后的修复策略，因此系统不会重复效果差的修复方式。
- 这一过程会迭代执行，直到测试通过或达到迭代预算；论文对 CollabCoder 使用了 5 轮迭代。

## 结果
- 在基础代码生成基准上，使用 **Qwen2.5-Coder-32B** 时，CollabCoder 的 **平均 Pass@1 为 82.50**，高于 **CodeSIM 的 80.22**、**MapCoder 的 79.84** 和 **ThinkCoder 的 77.02**。它的 **token 输入/输出为 2468.22 / 1606.88**，**API 调用次数为 4.12**；相比之下，**CodeSIM 为 2191.03 / 2593.04** 和 **4.87 次调用**，**MapCoder 为 5848.39 / 3309.55** 和 **9.05 次调用**。
- 使用 **GPT-4o mini** 时，CollabCoder 的 **平均 Pass@1 达到 83.25**，高于 **CodeSIM 的 81.52** 和 **MapCoder 的 77.80**。它在各数据集上的分数分别为 **96.34 HE**、**84.76 HE-ET**、**91.69 MBPP**、**60.20 MBPP-ET**。
- 使用 **Seed-Coder-8B** 时，CollabCoder 的 **平均 Pass@1 为 76.26**，略高于 **CodeSIM 的 75.51**，也高于 **ThinkCoder 的 71.08** 和 **MapCoder 的 68.78**；它的 **API 调用次数为 5.06**，而 CodeSIM 为 **6.69**，MapCoder 为 **9.84**。
- 在使用 **GPT-4o mini** 的竞赛级基准上，CollabCoder 报告 **LiveCodeBench 上 Pass@1 为 41.96**，**xCodeEval 上为 47.16**，**平均为 44.56**。基线方法中，**CodeSIM 平均为 39.53**，**MapCoder 平均为 37.70**。
- 在这些竞赛基准上，CollabCoder 的 **API 调用次数为 12.27**，低于 CodeSIM 的 **17.16** 和 MapCoder 的 **22.41**；其 **token 输入/输出为 15155.93 / 4491.37**，而 **CodeSIM 为 20907.82 / 13151.10**，**MapCoder 为 28437.65 / 17692.18**。
- 摘要将更难基准上的提升概括为：在 **LiveCodeBench** 和 **xCodeEval** 上，相比强基线提高 **11-20%**，并且平均每次执行 **少 4-10 次 API 调用**。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.13946v2](http://arxiv.org/abs/2604.13946v2)
