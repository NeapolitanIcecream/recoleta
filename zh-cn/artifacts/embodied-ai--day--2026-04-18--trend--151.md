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

# 机器人工作聚焦于真实世界长时程评测

## 概览
这个时期规模不大，但方向一致：最强的信号是机器人研究在真实世界长时程评测上变得更具体。LongBench 为操作任务加入了机制层面的基准，而一篇同期的机器人学习历史回顾把这个需求和更大的数据采集、部署周期联系起来。结果是，大家更明确地关注在真实场景里测量执行漂移、时序失败和上下文使用。

## 研究发现

### 面向机制的长时程评测
LongBench 为这一时期提供了一个具体锚点：长时程机器人评测开始更明确地解释策略为什么会失败。这个基准覆盖 10 个真实世界任务和 1,000 多个 episode。它把完全可观测的执行问题和依赖上下文的歧义分开，再按阶段给进展评分，而不是只给一个通过或失败的数字。这很重要，因为当前策略的失效原因各不相同。在上下文无关任务上，pi_0 以 86.3 的平均阶段评分领先，Diffusion Policy 为 51.2，OpenVLA-OFT 为 32.7。动态抓取是最清楚的压力测试。pi_0 得到 73.3，其他列出的系统都在 0.0 到 13.3 之间。

#### 资料来源
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): Summary with benchmark design, task split, scale, and headline results

### 规模和部署抬高了评测门槛
第二个信号不只来自一篇论文。这里看到的机器人技术栈和数据规模、真实部署、以及多模态动作预测有关。Technology Review 的历史文章不是基准论文，但它补充了为什么现在需要长时程评测。文章提到 Google 为 RT-1 训练了 17 个月，覆盖 700 个任务，在见过的任务上成功率为 97%，在未见过的指令上为 76%。它也提到商业压力在上升：2025 年人形机器人投资达到 61 亿美元。把这篇文章和 LongBench 放在一起看，近期重点就很清楚了。更好的机器人模型需要更好的真实世界测试，因为更大的策略和更大的数据采集循环已经进入部署讨论。

#### 资料来源
- [Robots learn: A brief, contemporary history](../Inbox/2026-04-18--robots-learn-a-brief-contemporary-history.md): Summary with RT-1, investment, and deployment context
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): Benchmark paper that supplies the real-world evaluation side of the trend
