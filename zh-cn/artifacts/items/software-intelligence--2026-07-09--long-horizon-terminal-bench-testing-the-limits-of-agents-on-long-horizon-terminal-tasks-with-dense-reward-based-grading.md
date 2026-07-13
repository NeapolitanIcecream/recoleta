---
source: arxiv
url: https://arxiv.org/abs/2607.08964v1
published_at: '2026-07-09T21:56:37'
authors:
- Zongxia Li
- Zhongzhi Li
- Yucheng Shi
- Ruhan Wang
- Junyao Yang
- Zhichao Liu
- Xiyang Wu
- Anhao Li
- Yue Yu
- Ninghao Liu
- Lichao Sun
- Haotao Mi
- LeoweiLiang
topics:
- terminal-agents
- long-horizon-planning
- code-intelligence
- software-engineering-agents
- agent-evaluation
- dense-reward-grading
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# Long-Horizon-Terminal-Bench: Testing the Limits of Agents on Long-Horizon Terminal Tasks with Dense Reward-Based Grading

## Summary
## 摘要
Long-Horizon-Terminal-Bench 评估 AI 智能体能否在持续数十分钟到数小时的终端工作流中持续推进。密集的子任务评分揭示了部分进展和失败模式，而二元通过/失败基准无法呈现这些信息。

## 问题
- 现有终端基准主要关注短任务和最终状态评分，难以呈现中间进展，也会把接近完成的运行结果与完全失败的运行结果归为一类。
- 软件修复、实验复现、数据审计和科学计算等真实工作流需要执行数百个操作，管理长上下文、调试，并在时间预算内完成任务。

## 方法
- 该基准提供了 46 个容器化终端任务，覆盖九个广泛领域，包括软件工程、实验复现、互动游戏、多模态分析和科学计算。
- 每个任务都被划分为有实际意义的子任务，并使用二元、连续、阈值式或按回合聚合的检查方式。总奖励是各子任务得分的加权平均值。
- 隐藏压力测试用于评估模型能否泛化到公开示例之外的情况，包括字段重命名、缺失值、含噪输入、图像几何结构变化，以及不同的坐标或时间约定。
- 作者通过共享的终端智能体测试框架评估了 15 个前沿模型，并报告通过率、平均奖励、token 使用量、回合数、执行时间和估算成本。

## 结果
- 智能体每个任务平均使用 990 万个 token，执行约 231 个回合，耗时 85.3 分钟，因此该基准的要求明显高于以往的终端基准。
- 在测试模型中，GPT-5.5 表现最强。在奖励阈值为 0.95 时，它完成了 46 个任务中的 7 个，比例为 15.2%；在满奖励阈值 1.0 下，通过率为 10.9%。
- 所有模型在 0.95 阈值下的平均通过率为 4.3%，在 1.0 阈值下为 1.7%。15 个模型中有 10 个在严格阈值下一个任务也没有完成。
- 密集评分显示，690 次运行中有 433 次获得了部分奖励，其中 180 次的奖励至少为 0.5；另有 227 次得分低于 0.05。二元评分会把这些结果都归为失败。
- 接近完成的运行次数超过完整通过次数的两倍。得分在 0.75 到 0.95 之间的运行有 73 次，而得分达到或超过 0.95 的通过运行有 30 次。
- 超时导致了 79% 的未完成运行，说明在 90 分钟预算内持续规划、验证和完成任务仍是主要弱点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.08964v1](https://arxiv.org/abs/2607.08964v1)
