---
kind: trend
trend_doc_id: 151
granularity: day
period_start: '2026-04-18T00:00:00'
period_end: '2026-04-19T00:00:00'
topics:
- robotics
- long-horizon manipulation
- benchmarks
- vision-language-action
- robot learning
run_id: materialize-outputs
aliases:
- recoleta-trend-151
tags:
- recoleta/trend
- topic/robotics
- topic/long-horizon-manipulation
- topic/benchmarks
- topic/vision-language-action
- topic/robot-learning
language_code: zh-CN
---

# 机器人研究聚焦真实世界长时程评测

## Overview
这一时期的信号不多，但很一致：最强的信号是机器人研究开始更具体地处理真实世界长时程评测。LongBench为操作任务加入了机制层面的基准，而同期一篇关于机器人学习的历史文章则把这种需求与更大的数据采集和部署周期联系起来。由此，研究重点更清楚地转向在真实环境中衡量执行漂移、时序失败和上下文使用。

## Clusters

### 面向机制的长时程评测
LongBench为这一时期提供了一个具体锚点：长时程机器人评测开始更明确地说明策略为何会失败。该基准覆盖10个真实世界任务和1,000多个episode。它将完全可观测的执行问题与依赖上下文的歧义分开，再按阶段给进展打分，而不是只用一个通过/失败结果。这很重要，因为当前策略失效的原因并不相同。在上下文无关任务上，pi_0以86.3的平均阶段得分领先，Diffusion Policy为51.2，OpenVLA-OFT为32.7。动态抓取是最清晰的压力测试案例。pi_0得分73.3，而这里列出的其他系统都在0.0到13.3之间。

#### Evidence
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): 包含基准设计、任务划分、规模和主要结果的摘要

### 规模和部署提高了评测门槛
第二个信号不止来自一篇论文。这里看到的机器人技术栈与数据规模、真实部署和多模态动作预测直接相关。Technology Review的历史文章不是基准测试论文，但它为“为什么长时程评测现在很重要”提供了有用背景。文中提到，Google RT-1训练持续17个月，覆盖700个任务，在已见任务上的成功率为97%，在未见指令上为76%。文章也提到商业压力在上升：2025年人形机器人投资达到61亿美元。把它与LongBench放在一起看，近期重点很明确。更好的机器人模型需要更好的真实世界测试，因为更大的策略和更大的数据采集闭环已经进入部署讨论。

#### Evidence
- [Robots learn: A brief, contemporary history](../Inbox/2026-04-18--robots-learn-a-brief-contemporary-history.md): 包含RT-1、投资和部署背景的摘要
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): 提供这一趋势中真实世界评测部分的基准论文
