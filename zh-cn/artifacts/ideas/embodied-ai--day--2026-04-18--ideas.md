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

# 机器人部署复盘诊断

## Summary
真实世界的长时程机器人评估已经具体到会改变日常工作流程。最直接的近期动作是按阶段的内部评测、回放后的结构化失败复盘，以及发布门槛里的动态抓取压力测试。证据里的共同点很明确：更大的机器人数据和部署循环，需要更好的方式去看清执行在时间上的断裂点，而不只是看一次运行有没有成功结束。

## 用于内部模型测试的按阶段长时程机器人评估
机器人团队现在已经有足够证据，把单一成功率换成按阶段计分的长时程评估，用在每周模型测试里。LongBench 说明了这样做的必要性：长任务会通过不同机制失败，包括执行漂移、阶段切换错误、错过时间窗口，以及需要依赖早先上下文的歧义状态。一个简单的通过/失败数字会把这些差异掩盖掉。

可落地的做法是做一个内部评测工具，按完成的子步骤给每个任务计分，并按失败机制打标签。做桌面操作策略的团队可以先从很窄的一组任务开始：一个时间窗口任务、一个误差累积任务、一个上下文相关任务。重点是看模型是否每次都卡在同一阶段、是否在回合后段退化，或者是否把外观相近的状态混淆了。这样比汇总成功率更能给模型和数据团队明确目标。

LongBench 也直接指出了当前策略的薄弱点。在完全可观测任务上，pi_0 的平均阶段分数是 86.3，Diffusion Policy 是 51.2，OpenVLA-OFT 是 32.7。动态抓取是最严苛的压力测试：pi_0 达到 73.3，而其余列出的系统都在 0.0 到 13.3 之间。一个成本不高的验证步骤，是把现有的一项内部任务重新跑一遍，加入阶段标注，再把排序和当前的通过/失败榜单对比。如果排序或失败原因发生变化，旧评测就在藏信号。

### Evidence
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): LongBench summary states the benchmark separates execution and context difficulty, uses stage-wise scoring, and reports policy gaps on long-horizon tasks.
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): The abstract describes mechanism-aware evaluation for execution robustness, temporal consistency, and context-dependent reasoning in real-world manipulation.
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): The introduction explains that aggregate success fails to distinguish execution instability, dynamic response limits, and contextual ambiguity.

## 真实机器人回放复盘的失败模式标注流程
现在，比再做一轮汇总式基准测试，更容易说服团队去做机器人回放失败分析工具。LongBench 按机制组织长时程操作，包括阶段依赖、迭代推进、误差累积、时间窗口、完成歧义、计数歧义、子任务分支歧义和跨回合歧义。这套分类已经足够支撑真实部署中的复盘流程。

这里真正有用的产品，是一个回放后调试器，把视频、动作块和任务阶段对齐，然后让复盘者从一个固定的小集合里标注失败模式。做 VLA 或 VA 策略的团队可以在每批真实世界试验后使用它。几周下来，他们会拿到按任务和按策略版本统计的失败原因分布，这比单一成功分数更可操作，也比给每条轨迹完整重标注便宜。

这也符合更广泛的机器人学习报道里描述的部署节奏。这个领域已经在更大的真实世界数据集上训练，并用已部署机器人的反馈改进模型。Google 为 RT-1 花了 17 个月，收集了 700 个任务的数据，并报告在见过的任务上成功率为 97%，在未见过的指令上为 76%。一旦团队把采集循环做到这个规模，瓶颈就会转向判断哪些失败值得补新数据、改控制器，还是重做任务。一个轻量的失败标注工具正好补上这层分流。

### Evidence
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): LongBench defines concrete mechanism categories for long-horizon failures and motivates evaluation beyond aggregate success.
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): The paper abstract frames the benchmark around execution robustness, temporal consistency, and context-dependent reasoning.
- [Robots learn: A brief, contemporary history](../Inbox/2026-04-18--robots-learn-a-brief-contemporary-history.md): The article reports RT-1 data collection over 17 months and 700 tasks, supporting the claim that larger deployment and data loops raise pressure for better failure triage.

## 机器人发布门槛中的动态抓取验收测试
在长时程操作策略进入真实工作流之前，动态抓取应该先进入验收测试。LongBench 显示，这个时间窗口任务把当前系统区分得比更容易的完全可观测任务更明显。pi_0 的分数是 73.3，而 OpenVLA-OFT 是 0.0，SmolVLA 是 10.0，Diffusion Policy 是 13.3，MemoryVLA 是 10.0，CronusVLA 是 13.3。这个差距已经足够当作门槛。

对评估仓储拣选、料箱转运或移动物体交接策略的团队来说，流程改动很简单：每个候选版本都加一个简短的动态抓取测试，并在现场试运行前要求达到最低阶段分数。这个测试成本低，因为它只覆盖一个窄能力，但会带来明确的运营后果。如果策略在受控基准上连时间窗口都抓不住，那么在输送带、人机交接或物体运动引入噪声后，可靠性大概率会下降。

更大的市场背景也支持更严格的门槛。商用部署压力在上升，《Technology Review》提到 2025 年人形机器人投资达到 61 亿美元，而且已部署系统越来越多地用于数据采集和改进。把时间窗口压力测试放进发布流程，是在操作员承担故障成本之前抓住已知薄弱点的一种直接方法。

### Evidence
- [LongBench: Evaluating Robotic Manipulation Policies on Real-World Long-Horizon Tasks](../Inbox/2026-04-18--longbench-evaluating-robotic-manipulation-policies-on-real-world-long-horizon-tasks.md): LongBench reports dynamic grasping as the hardest fully observable task and gives the stage-wise scores across six policies.
- [Robots learn: A brief, contemporary history](../Inbox/2026-04-18--robots-learn-a-brief-contemporary-history.md): The article notes rising commercial deployment and investment, which increases the need for concrete pre-deployment acceptance tests.
