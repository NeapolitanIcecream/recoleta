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
## 摘要
ATAAT 通过植入能在指令调优后保留下来的视觉后门，攻击 OpenVLA 风格的视觉-语言-动作机器人策略。论文的主要说法是，分离良性梯度和后门梯度后，在 5% 投毒率下，定向攻击成功率可超过 80%，同时保持较高的正常任务成功率。

## 问题
- VLA 机器人策略依赖视觉感知，因此供应链攻击者可以加入一个触发器，在部署期间改变机器人动作。
- 标准后门攻击在 VLA 上效果差，因为良性指令调优和恶意目标动作训练会把模型更新推向相互冲突的方向。
- 这一点很重要，因为持久后门可以在常规测试中保持隐藏，并由实体物体、空间状态或人类提示激活。

## 方法
- 论文用良性任务梯度和后门任务梯度之间的余弦相似度来定义梯度干扰。
- 在数据投毒中，ATAAT 构造带有可见触发器的投毒图像，并加入由代理特征提取器生成的小幅不可见扰动，使投毒样本把训练引向单独的特征方向。
- 在白盒微调中，ATAAT 使用干净数据上的激活统计来寻找休眠神经元，然后使用二值掩码，使只有这些参数学习后门。
- 触发器可以是简单的视觉物体，也可以是语义条件，例如打开的抽屉、交叉摆放的餐具，或戴手表的人。

## 结果
- 在使用 OpenVLA-7B 的 LIBERO-Spatial 数据投毒实验中，ATAAT 报告 88.8% 的良性 SR 和 83.5% 的 TASR；改造版 BadVLA 报告 17.5% 的 SR 和 13.1% 的 TASR，BadNet 报告 4.5% 的 SR 和 0.8% 的 TASR。
- 在 LIBERO-Object 数据投毒实验中，ATAAT 报告 90.1% 的 SR 和 85.9% 的 TASR；改造版 BadVLA 报告 16.1% 的 SR 和 12.8% 的 TASR。
- 在微调投毒中，ATAAT 在 LIBERO-Spatial 上报告 78.1% 的 SR 和 72.5% 的 TASR，而改造版 BadVLA 为 52.1% 的 SR 和 39.2% 的 TASR。
- 在 LIBERO-Object 的微调投毒中，ATAAT 报告 79.3% 的 SR 和 74.8% 的 TASR，而改造版 BadVLA 为 50.8% 的 SR 和 37.7% 的 TASR。
- 论文称该方法在 5% 投毒率下有效，并跟踪了梯度余弦相似度：BadVLA 在约 400 步后保持在 -0.4 附近，而 ATAAT 保持在 0 附近。
- 论文描述了针对固定物体、指向手势、物体状态和人类属性的真实机器人测试，但摘录没有提供真实场景成功率百分比。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.08612v1](https://arxiv.org/abs/2605.08612v1)
