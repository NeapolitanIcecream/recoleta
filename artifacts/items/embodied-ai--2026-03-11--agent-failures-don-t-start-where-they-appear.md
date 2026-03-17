---
source: hn
url: https://www.vichoiglesias.com/writing/agent-failures-dont-start-where-they-appear
published_at: '2026-03-11T23:39:33'
authors:
- vichoiglesias
topics:
- agent-debugging
- failure-analysis
- execution-traces
- state-tracking
- long-horizon-agents
relevance_score: 0.18
run_id: materialize-outputs
---

# Agent Failures Don't Start Where They Appear

## Summary
这篇文章指出，长时运行的智能体失败通常不是在“看起来出错”的那一步开始，而是更早进入了一个不可恢复的状态。作者主张把调试重点从阅读末端日志转向定位“失败开始变得不可避免”的状态转折点。

## Problem
- 传统 agent 调试通常从最终错误处往回翻 trace，但长轨迹中可见错误往往只是更早问题的下游结果。
- 仅有 prompts、tool calls、model outputs 等可观测日志，只能重建过程，无法直接标出“何时首次进入不可恢复失败状态”。
- 对长时间运行系统而言，找不到这个因果边界会让排障缓慢、主观且容易误判，这对生产级 agent 很重要。

## Approach
- 核心思想是把失败视为**沿时间传播的轨迹问题**，而不是某个单点事件；真正该问的是：**系统在哪一步首次进入了失败已不可避免的状态？**
- 为此，执行历史需要记录**状态随时间的演化**，不仅是外部事件，还包括每一步 agent 当时“知道什么”与关键内部状态如何变化。
- 一旦能比较跨时间步的状态，就可以检查某个违反条件/失败条件在何时首次为真，从而定位“未来在此处断裂”的边界。
- 作者进一步声称，若按这种方式记录运行历史，就可以对失败起点进行搜索，并在**对数时间**内找到该步，而不是人工逐行阅读长 trace。

## Results
- 文中没有提供实验数据、基准数据集或定量评测结果。
- 最强的具体主张是：通过记录状态演化而非仅记录事件，可以定位“失败首次不可恢复”的步骤，而不是只看到最终显性错误。
- 作者给出的效率主张是可在**logarithmic time（对数时间）**内搜索到失败起点，但未给出算法细节、复杂度证明或实验验证。
- 文章以事务制裁审查为例说明：例如在**step 47** 才出现错误批准，但真正导致失败的状态变化可能发生在更早的如 **step 12** 或其他中间步骤；这些数字是说明性示例，不是实验结果。

## Link
- [https://www.vichoiglesias.com/writing/agent-failures-dont-start-where-they-appear](https://www.vichoiglesias.com/writing/agent-failures-dont-start-where-they-appear)
