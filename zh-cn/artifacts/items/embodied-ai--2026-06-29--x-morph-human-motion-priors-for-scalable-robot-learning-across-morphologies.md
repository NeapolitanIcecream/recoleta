---
source: arxiv
url: https://arxiv.org/abs/2606.30290v1
published_at: '2026-06-29T13:31:27'
authors:
- Ritwik Sharma
- Shivam Sood
- Arhaan Jain
- Shyam Charan Kesavamoorthi
- Chengyang He
- Guillaume Sartoretti
topics:
- cross-morphology-retargeting
- robot-motion-priors
- legged-robot-learning
- human-motion-data
- sim2sim-tracking
- video-teleoperation
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# X-Morph: Human Motion Priors for Scalable Robot Learning Across Morphologies

## Summary
## 概要
X-Morph 将人类动作转换为可执行的腿式机器人行为，适用于四足机器人、六足机器人和带机械臂的四足机器人系统。在机器人专用动作数据集稀缺时，它把人类动作作为可复用的训练数据。

## 问题
- 非人形腿式机器人缺少大规模动作数据集，因此每种新形态通常需要机器人专用示范、手工设计的奖励，或小规模技能库。
- 直接进行人到机器人的动作重定向，视觉上可能合理，但会产生足端打滑、地面穿透、悬空接触、关节限位问题，或机器人无法跟踪的参考动作。
- 这个问题的关键在于，可扩展的机器人学习需要能跨不同身体复用的行为数据，而这些身体并不共享人类骨架。

## 方法
- X-Morph 首先使用感知形态差异的身体部位对应关系，将人类或 G1 人形机器人的动作映射到目标机器人参考动作，例如把人类腿部对应到四足机器人腿部，或把人类手臂对应到前腿。
- 一个物理感知的时间校正器会编辑重定向后的片段，以减少足端滑动、穿透、脚部悬空、根节点漂移和末端执行器误差。
- 一个特权强化学习教师策略使用全状态信息和跟踪奖励来跟踪校正后的参考动作。
- 一个因果学生策略从教师策略蒸馏而来，并使用可部署的本体感知输入，以及紧凑的当前和下一步参考流运行。
- 在交互式使用中，因果重定向模型会把最近的 G1 动作映射为清理后的机器人参考动作，用于视频遥操作；文本提示也可以生成或检索人类动作，再对其进行重定向和跟踪。

## 结果
- 系统在 3 种目标形态上评估：Go2 四足机器人、Yuna 六足机器人，以及带机械臂的 B2-Z1 四足机器人。
- 在使用 33 个匹配行走片段的 Go2 消融实验中，物理校正器将足端打滑从 58.76 cm/s 降至 42.76 cm/s，下降 27.2%。
- 同一 Go2 消融实验将穿透 p95 从 11.34 cm 降至 6.02 cm，下降 46.9%；接触高度误差从 6.45 cm 降至 3.60 cm，下降 44.2%。
- 对于实时视频参考流下的 Yuna 六足机器人 sim2sim 跟踪，校正后的参考动作将关节 MAE 从 6.57 度降至 5.45 度，提升 17.4%。
- Yuna 跟踪测试还将根节点速度 RMSE 从 0.479 m/s 降至 0.413 m/s，将偏航角速度 RMSE 从 0.896 rad/s 降至 0.651 rad/s，并将平均足端打滑从 29.29 cm/s 降至 24.30 cm/s。
- 实时视频流水线可从 30 Hz 摄像头流中以最高 28.9 Hz 发布重定向后的机器人参考动作；论文还展示了文本条件执行和六足机器人开门先验作为定性演示，但没有提供受控的样本效率对比。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.30290v1](https://arxiv.org/abs/2606.30290v1)
