---
source: arxiv
url: https://arxiv.org/abs/2605.26820v1
published_at: '2026-05-26T10:39:02'
authors:
- Jiarun Zhu
- Yijun Hong
- Xiaoquan Sun
- Zetian Xu
- Mingqi Yuan
- Zhiyong Wang
- Wenjun Zeng
- Jiayu Chen
topics:
- vision-language-action
- continual-learning
- catastrophic-forgetting
- experience-replay
- real-world-robotics
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Can VLA Models Learn from Real-World Data Continually without Forgetting?

## Summary
## 摘要
本文测试 VLA 机器人策略能否在学习新的真实世界任务时保住旧的操作技能。结果显示，直接按顺序微调会造成严重遗忘；在合理设置回放比例和动作归一化后，经验回放可以起作用。

## 问题
- 真实机器人会随着时间接收新的任务数据，但把所有历史数据都拿来重训的成本很高。
- VLA 策略在后续任务上微调时，可能丢掉早先学到的技能，这会限制机器人长期部署。
- 以往关于持续学习的 VLA 研究多在范围很窄的仿真环境中进行，可能没有覆盖真实物体、相机、动作分布和任务切换带来的问题。

## 方法
- 作者收集了一个真实世界持续学习数据集，包含 4 个顺序进行的操作任务，每个任务 500 条轨迹：Stack Bowl、Hang Cup、Press Button 和 Fold Towel。
- 他们对一个 \(\pi_{0.5}\) VLA 策略在每个任务上微调 4,000 步，并在每一阶段后评估所有已见任务。
- 他们用归一化到 0-100 的任务分数，衡量平均分、负向后向迁移（NBT）和前向迁移（FT）。
- 他们测试了经验回放，缓冲区比例为 \(B \in \{0.002, 0.02, 0.2\}\)，回放频率为 \(f_r \in \{0.05, 0.1, 0.2, 0.5\}\)。
- 他们比较了两种动作归一化方式：固定使用第一个任务的统计量，以及按任务分别统计。

## 结果
- 直接按顺序微调后，Stack Bowl 从 100.0 降到 15.0，Hang Cup 从 97.5 降到 25.0，Press Button 从 100.0 降到 13.3。最终平均分是 37.3，NBT 为 +80.0，FT 为 -50.0。
- 默认回放在 \(B=0.2\)、\(f_r=0.2\) 时，Stack Bowl 得分 96.3，Hang Cup 97.5，Press Button 90.0，Fold Towel 90.0。平均分是 93.5，NBT 为 +5.0，FT 为 +11.8。
- 默认回放的平均分高于联合训练：93.5 对 70.3。联合训练在 Press Button 上只剩 13.3，而默认回放达到 90.0。
- 更小的回放缓冲区会削弱部分任务的保留效果：当 \(B=0.002\) 时，Hang Cup 为 60.0，平均分为 85.5；当 \(B=0.02\) 时，平均分为 86.3。
- 回放频率改变了稳定性和学习效果之间的权衡：\(f_r=0.05\) 时平均分 85.3，\(f_r=0.1\) 时 83.3，\(f_r=0.2\) 时 93.5，\(f_r=0.5\) 时 88.0。
- 固定动作归一化的平均分为 93.5；按任务归一化后，平均分降到 23.7，Hang Cup、Press Button 和 Fold Towel 都是 0.0。测试时改用 Stack Bowl 的统计量后，这个设置的平均分升到 58.0，说明学到的动作尺度不对，而不是完全缺少任务语义。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26820v1](https://arxiv.org/abs/2605.26820v1)
