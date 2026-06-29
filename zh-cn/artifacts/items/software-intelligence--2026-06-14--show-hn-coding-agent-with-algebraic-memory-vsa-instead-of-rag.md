---
source: hn
url: https://github.com/vitaliyfedotovpro-art/raidho
published_at: '2026-06-14T23:44:56'
authors:
- astrumverum
topics:
- coding-agent
- memory
- vsa
- multi-model
- cost-benchmark
relevance_score: 0.98
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Coding agent with algebraic memory (VSA) instead of RAG

## Summary
## 总结
Raidho 是一个编码代理，把推理、执行和记忆拆到不同组件里。它的重要性在于，它声称相比单模型工具循环，成本更低，而且能保留项目级的持久记忆。

## 问题
- 大多数编码代理用一个模型同时做规划和工具调用，这让每次迭代都要为昂贵的推理付费。
- 纯聊天历史不能在多次运行之间很好地保留可复用事实，所以代理会重复工作。
- 这份材料面向本地编码工作流，在这些场景里，提供方选择、成本和持久性都很重要。

## 方法
- 它用一个模型在文本模式下负责推理，再用第二个模型在工具循环中执行代码。
- 它加入了持久记忆，把 subject-relation-object 事实按项目写到磁盘上，并在下一次运行时重新加载。
- 这套记忆用的是 Vector Symbolic Architecture（VSA），不是 RAG；它把事实做代数组合，并用 bit-packed 相似度排序。
- 它还提供 council mode，让两个提供方围绕一个问题辩论，再由一个中立步骤提炼一致点、分歧和建议。
- 一个可选的自动提炼模式会把重复出现的、成功的只读任务循环转成确定性流程，供后续复用。

## 结果
- 摘录里给出了一条明确的基准：在同一个任务、同一个模型下，一个确定性流程的成本是 $0.05，context-first hybrid 的成本是 $0.116，纯工具循环的成本是 $0.301。
- 在这条基准上，hybrid 的报告质量和工具循环相同，成本低 2.6 倍。
- 在一个针对小型数据的重复多步任务中，自动提炼让 5 次运行的成本降低了 9.6 倍，也就是下降了 70%。
- 对于一个数据量很大的审计，自动提炼几乎没有省钱，因为成本来自文件内容，而不是循环开销。
- 摘录说这个系统通过官方 SDK 在 DeepSeek 和 Claude 上做了端到端测试，但这段文字没有给出更完整的基准表。

## Problem

## Approach

## Results

## Link
- [https://github.com/vitaliyfedotovpro-art/raidho](https://github.com/vitaliyfedotovpro-art/raidho)
