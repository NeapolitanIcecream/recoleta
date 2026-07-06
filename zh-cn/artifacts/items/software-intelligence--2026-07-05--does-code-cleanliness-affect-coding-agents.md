---
source: hn
url: https://arxiv.org/abs/2605.20049
published_at: '2026-07-05T23:03:55'
authors:
- softwaredoug
topics:
- coding-agents
- code-cleanliness
- software-engineering
- code-intelligence
- agent-evaluation
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Does Code Cleanliness Affect Coding Agents?

## Summary
## 摘要
本文测试更干净的代码是否会改变 Claude Code 在软件任务中的表现。在 660 次受控试验中，代码整洁度没有改变通过率，但减少了 token 使用量和文件重复访问次数。

## 问题
- 编码代理评估通常固定目标代码库，因此无法说明代码质量是否会改变代理行为。
- 论文研究结构和风格上的整洁度是否会影响代理浏览和修改代码的能力。
- 这一点会影响代理成本和速度，因为即使最终任务成功率不变，成本和速度也取决于 token 使用量和代码导航。

## 方法
- 研究构建了最小配对代码库：每一对保持架构、依赖和公开行为相同，只改变整洁度。
- 整洁度通过静态分析规则违规和认知复杂度来改变。
- 作者从两个方向创建配对：一条流水线把干净代码库变得混乱，另一条流水线清理混乱代码库。
- 他们在 6 组代码库配对上编写了 33 个任务，并通过应用程序公开接口处的隐藏测试评估输出。
- 他们使用 Claude Code 运行了 660 次试验。

## 结果
- 与配对的较混乱代码库相比，更干净的代码没有改变 Claude Code 的通过率。摘录没有给出通过率百分比。
- 与匹配的较混乱变体相比，更干净的代码减少了 7% 到 8% 的 token 使用量。
- 更干净的代码将文件重复访问次数减少了 34%。
- 论文主张的主要收益是更低的运行成本和更好的导航能力，这些结果是在外部行为相同的匹配代码库上测得的。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.20049](https://arxiv.org/abs/2605.20049)
