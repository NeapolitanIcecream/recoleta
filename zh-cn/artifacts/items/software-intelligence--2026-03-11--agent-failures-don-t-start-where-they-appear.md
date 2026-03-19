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
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Agent Failures Don't Start Where They Appear

## Summary
本文指出，长时间运行的智能体失败通常不是在表面出错的那一步开始，而是在更早某个状态转折点就已注定。作者主张把调试目标从“哪里出错了”改为“系统何时首次进入不可恢复失败状态”。

## Problem
- 长链路智能体执行中的可见失败，往往只是更早错误状态传播后的结果，因此从尾部倒查日志常常低效且误导。
- 现有 agent observability 工具主要记录事件、提示词、工具调用和延迟，但不能直接定位“从可恢复变为不可恢复”的因果边界。
- 这很重要，因为运行可能持续数十分钟到数小时；若无法找到最早失效点，工程师就只能手工重建故事，调试成本高且不稳定。

## Approach
- 核心思想是把失败看成**跨时间传播的状态轨迹问题**，而不是某个单点动作或单次函数调用的问题。
- 需要记录的不只是事件日志，还包括每一步的系统状态：当时 agent 知道什么、内部变量如何变化、哪些风险条件是否已成立。
- 有了按时间演化的状态历史后，就可以判断“哪一步首次使失败条件为真”，也就是未来开始断裂的那一刻。
- 作者进一步提出，可把这种定位过程变成对执行历史的搜索问题，并声称能够以**对数时间**找到失败起点。

## Results
- 文中没有提供正式实验、数据集或基线比较，也没有报告准确率、召回率或耗时数字。
- 最强的具体主张是：如果执行历史记录了状态演化，就可以搜索出“失败首次开始的确切步骤”。
- 文章明确宣称该搜索可在**logarithmic time（对数时间）**完成，但未给出算法细节、复杂度证明或实现结果。
- 文章通过示例说明：例如在第 **47** 步出现违规批准时，真正导致失败的状态变化可能发生在更早的第 **12** 步或中间某一步，但这只是概念性说明，不是实验结果。"

## Link
- [https://www.vichoiglesias.com/writing/agent-failures-dont-start-where-they-appear](https://www.vichoiglesias.com/writing/agent-failures-dont-start-where-they-appear)
