---
source: hn
url: https://sherwood.news/tech/figures-robots-just-sorted-packages-for-200-hours-straight/
published_at: '2026-05-26T22:52:27'
authors:
- hochmartinez
topics:
- humanoid-robots
- package-sorting
- robot-autonomy
- multi-robot-operation
- logistics-automation
relevance_score: 0.55
run_id: materialize-outputs
language_code: zh-CN
---

# Figure's robots sorted packages for 200 hours straight

## Summary
Figure 报告称，一组 Figure 03 人形机器人连续运行了 200 小时，完成了一个自动化包裹分拣演示，共分拣 249,560 个包裹。这里最强的主张是它在物流任务中的续航能力，不是提出了新的研究方法，也不是一个经过基准测试的机器人策略。

## Problem
- 这个任务面向仓库包裹分拣，机器人需要识别条形码，并把包裹正面朝下放到传送带上。
- 这很重要，因为真正有用的人形机器人需要长时间完成有偿工业工作，而不只是短时间演示。
- 文章没有描述科学问题陈述、正式基准或失败模型。

## Approach
- Figure 在一条包裹分拣线上使用了 Figure 03 人形机器人。
- 每个机器人都会找到小包裹上的条形码，并把包裹正面朝下放到传送带上。
- 多台机器人协同工作：当一台机器人的电池在大约 3 到 4 小时后电量下降时，它会离开充电，另一台机器人接替。
- Brett Adcock 说，这次运行是自主完成的，过程中没有人介入。
- 这条帖子提到了 Helix 模型，但摘录没有给出模型架构、训练数据、控制策略、传感器栈或评估设置的细节。

## Results
- 这个演示运行了 200 小时，相当于 8 天 8 小时，或 25 个 8 小时的人类班次。
- 直播计数显示，在这 200 小时内共分拣了 249,560 个包裹。
- 在之前 10 小时的人机对抗挑战中，人类实习生分拣了 12,924 个包裹，Figure 03 机器人分拣了 12,735 个。
- 报告的速度分别是：人类每个包裹 2.79 秒，机器人每个包裹 2.83 秒。
- 文章称这 200 小时运行没有故障，也没有人介入，但没有给出独立审计、错误率、正常运行时间拆分，或与现有仓库自动化基线的对比。

## Link
- [https://sherwood.news/tech/figures-robots-just-sorted-packages-for-200-hours-straight/](https://sherwood.news/tech/figures-robots-just-sorted-packages-for-200-hours-straight/)
