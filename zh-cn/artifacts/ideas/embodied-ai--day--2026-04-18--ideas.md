---
kind: ideas
granularity: day
period_start: '2026-04-18T00:00:00'
period_end: '2026-04-19T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- robotics
- long-horizon manipulation
- benchmarks
- vision-language-action
- robot learning
tags:
- recoleta/ideas
- topic/robotics
- topic/long-horizon-manipulation
- topic/benchmarks
- topic/vision-language-action
- topic/robot-learning
language_code: zh-CN
---

# 机器人 rollout 诊断

## Summary
真实世界长时程机器人评估已经具体到足以改变日常工作流。近期最明确的动作是：做分阶段内部评测、在 rollout 之后做结构化失败复盘，以及把动态抓取压力测试加入发布门禁。现有证据的共同点很直接：随着机器人数据和部署循环变大，团队需要更好的方法看清执行是如何随着时间推移出错的，而不只是看一次运行最后有没有成功。

## 用于内部模型测试的分阶段长时程机器人评估
机器人团队现在已经有足够证据，在每周模型测试中用分阶段的长时程评估取代单一成功率。LongBench 说明了原因：长任务会通过不同机制失败，包括执行漂移、阶段切换错误、错过时间窗口，以及需要依赖更早上下文记忆的歧义状态。单一的通过/失败数字会盖住这些差异。

实际可做的是一个小型内部评测工具：按已完成的子步骤给每个任务打分，并按机制标记失败。交付桌面操作策略的团队可以先从一个窄范围开始：一个时间窗口任务、一个误差累积任务和一个上下文依赖任务。重点是看模型是否每次都卡在同一阶段、是否在 rollout 后段性能下降，或者是否会混淆视觉上相似的状态。这样给模型团队和数据团队的目标，比总体成功率更清楚。

LongBench 也明确提示了当前策略会在哪些地方失效。在完全可观测任务上，pi_0 的平均分阶段得分是 86.3，Diffusion Policy 是 51.2，OpenVLA-OFT 是 32.7。动态抓取是区分度最强的压力测试：pi_0 达到 73.3，其他列出的系统都在 0.0 到 13.3 之间。一个低成本的验证步骤，是给现有的一项内部任务补上阶段标注，再把排序和当前的通过/失败排行榜对比。如果排序或失败模式说明发生变化，旧评测就盖住了有用信号。

### Evidence
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): LongBench 摘要说明，该基准将执行难度与上下文难度分开，使用分阶段评分，并报告了长时程任务上的策略差距。
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): 摘要描述了面向真实世界操作的机制感知评估，覆盖执行稳健性、时间一致性和依赖上下文的推理。
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): 引言解释了，总体成功率无法区分执行不稳定、动态响应限制和上下文歧义。

## 面向真实机器人 rollout 复盘的失败模式标注流程
与其再做一轮总体基准测试，现在更容易为机器人 rollout 的失败复盘工具找到理由。LongBench 按机制组织长时程操作问题，包括阶段依赖、迭代进展、误差累积、时间窗口、完成歧义、计数歧义、子任务分支歧义和跨 episode 歧义。这个分类已经足够用来搭建真实部署的复盘流程。

这里合适的产品是一个运行后调试器，把视频、动作块和任务阶段对齐，然后让审阅者从一个简短固定集合里标注失败模式。做 VLA 或 VA 策略的团队可以在每一批真实世界试验后使用它。几周之后，他们就能按任务和策略版本得到失败原因分布。这比单一成功率更能指导行动，也比给每条轨迹重新完整标注更便宜。

这也符合更广泛机器人学习报道里描述的当前部署周期。这个领域已经在用更大的真实世界数据集训练，并通过已部署机器人的反馈改进模型。Google 为 RT-1 用了 17 个月，在 700 个任务上收集数据，并报告已见任务成功率 97%、未见指令成功率 76%。当团队把数据收集循环做到这个规模后，瓶颈就变成哪些失败值得补新数据、改控制器，或重设计任务。一个轻量的失败标注工具可以提供这层分流。

### Evidence
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): LongBench 定义了长时程失败的具体机制类别，并说明评估不能只看总体成功率。
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): 论文摘要把基准聚焦在执行稳健性、时间一致性和依赖上下文的推理上。
- [Robots learn: A brief, contemporary history](../Inbox/2026-04-18--robots-learn-a-brief-contemporary-history.md): 文章报告 RT-1 在 17 个月内覆盖 700 个任务的数据收集，这支持了一个判断：更大的部署和数据循环会提高对更好失败分流的需求。

## 将动态抓取验收测试加入机器人发布门禁
在长时程操作策略进入真实工作流之前，动态抓取应当进入验收测试。LongBench 表明，这个时间窗口任务比更容易的完全可观测任务更能拉开当前系统之间的差距。pi_0 得分 73.3，OpenVLA-OFT 得分 0.0，SmolVLA 10.0，Diffusion Policy 13.3，MemoryVLA 10.0，CronusVLA 13.3。这个差距已经足够拿来做门槛。

对于评估仓储拣选、料箱转移或运动物体交接策略的团队，流程改动很简单：给每个发布候选版本加一个短动态抓取测试，并在现场试验前要求达到最低分阶段得分。这个测试成本低，因为它只盯住一个能力点，而且操作后果很明确。如果策略在受控基准上都会错过时间窗口，那么当传送带、人工交接或物体运动带来噪声时，它的可靠性很可能会进一步下降。

更大的市场背景也支持更严格的门槛。商业部署压力在上升，Technology Review 的文章提到，2025 年人形机器人投资达到 61 亿美元，而且已部署系统越来越多地被用于数据收集和模型改进。把时间窗口压力测试放进发布流程，是在运营方承担失败成本之前抓住一个已知弱点的直接办法。

### Evidence
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): LongBench 报告动态抓取是最难的完全可观测任务，并给出了六种策略的分阶段得分。
- [Robots learn: A brief, contemporary history](../Inbox/2026-04-18--robots-learn-a-brief-contemporary-history.md): 文章提到商业部署和投资都在上升，这提高了对具体部署前验收测试的需求。
