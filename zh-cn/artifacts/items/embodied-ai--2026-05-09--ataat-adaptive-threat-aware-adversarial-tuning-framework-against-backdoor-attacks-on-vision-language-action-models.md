---
source: arxiv
url: https://arxiv.org/abs/2605.08612v1
published_at: '2026-05-09T02:15:10'
authors:
- Kewei Chen
- Yayu Long
- Shuai Li
- Mingsheng Shang
topics:
- vision-language-action
- robot-security
- backdoor-attacks
- openvla
- adversarial-tuning
- robot-manipulation
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# ATAAT: Adaptive Threat-Aware Adversarial Tuning Framework against Backdoor Attacks on Vision-Language-Action Models

## Summary
## 总结
ATAAT 通过在 OpenVLA 风格的视觉-语言-动作机器人策略中植入视觉后门来攻击它们，这些后门可以在指令微调后继续存在。它的核心主张是，把正常梯度和后门梯度分开后，在 5% 投毒率下，定向攻击成功率可以超过 80%，同时正常任务成功率仍然保持较高水平。

## 问题
- VLA 机器人策略依赖视觉感知，因此供应链攻击者可以加入一个触发器，在部署时改变机器人的动作。
- 传统后门攻击在 VLA 上效果差，因为正常的指令微调和恶意的目标动作训练会让模型更新朝着相反方向走。
- 这很重要，因为持续存在的后门可以在常规测试中保持隐藏，并在物理物体、空间状态或人类线索上被激活。

## 方法
- 论文用良性任务梯度和后门任务梯度之间的余弦相似度来定义梯度干扰。
- 在数据投毒场景中，ATAAT 构造带有可见触发器和小幅不可见扰动的投毒图像，不可见扰动由代理特征提取器生成，使投毒样本把训练引向单独的特征方向。
- 在白盒微调场景中，ATAAT 先用干净数据上的激活统计找到沉睡神经元，然后用二值掩码让只有这些参数学习后门。
- 触发器可以是简单的视觉物体，也可以是语义条件，例如打开的抽屉、交叉摆放的餐具，或者戴着手表的人。

## 结果
- 在 LIBERO-Spatial 数据投毒、OpenVLA-7B 上，ATAAT 报告良性 SR 为 88.8%，TASR 为 83.5%；改造后的 BadVLA 报告 SR 为 17.5%，TASR 为 13.1%；BadNet 报告 SR 为 4.5%，TASR 为 0.8%。
- 在 LIBERO-Object 数据投毒上，ATAAT 报告 SR 为 90.1%，TASR 为 85.9%；改造后的 BadVLA 报告 SR 为 16.1%，TASR 为 12.8%。
- 在微调投毒中，ATAAT 在 LIBERO-Spatial 上报告 SR 为 78.1%，TASR 为 72.5%；改造后的 BadVLA 分别为 52.1% 和 39.2%。
- 在 LIBERO-Object 的微调投毒中，ATAAT 报告 SR 为 79.3%，TASR 为 74.8%；改造后的 BadVLA 分别为 50.8% 和 37.7%。
- 论文说该方法在 5% 投毒率下有效，并跟踪了梯度余弦相似度：BadVLA 在约 400 步后维持在 -0.4 附近，而 ATAAT 维持在 0 附近。
- 文中描述了针对固定物体、指向的手、物体状态和人类属性的真实机器人测试，但摘录没有给出真实世界的成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08612v1](https://arxiv.org/abs/2605.08612v1)
