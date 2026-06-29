---
source: arxiv
url: https://arxiv.org/abs/2606.03556v1
published_at: '2026-06-02T12:19:28'
authors:
- Xiaofei Wang
- Mingliang Han
- Tianyu Hao
- Yi Yang
- Yun-Bo Zhao
- Keke Tang
topics:
- vision-language-action
- adversarial-patch
- robot-security
- partial-observability
- openvla
- libero
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# Partially Observable Adversarial Patch Attacks on Vision-Language-Action Models in Robotics

## Summary
## 摘要
这篇论文表明，即使攻击者只能看到一次 rollout 的前半段，静态对抗补丁也能干扰机器人的 vision-language-action 策略。该攻击同时针对目标对象的语义指向和动作平滑性，然后把同一个补丁带入任务中不可见的后续阶段。

## 问题
- 先前的 VLA 补丁攻击假设攻击者可以在完整的机器人轨迹上优化，这给了攻击者现实部署中通常看不到的信息。
- 论文研究了更严格的威胁模型：攻击者只观察前 K 帧，然后必须为剩余执行过程放置一个固定补丁。
- 这很重要，因为一个只基于短时间观测的实体补丁，可以在不改模型权重、不改指令、也不改控制器的情况下，让 VLA 控制的机器人在长时程内失败。

## 方法
- 攻击者以灰盒方式使用 VLA 模型，能查询模型并获取补丁优化所需的模型侧信号，但不能访问模型参数，也不能直接控制机器人。
- 补丁位置使用最后一帧前缀的跨模态注意力来确定。方法先找到与指令相关注意力最高的图像区域，然后把补丁限制在该区域内。
- 补丁内容通过两个损失进行优化：一个调整由注意力导出的任务名词语义指向，另一个把预测动作推向会增加末端执行器轨迹曲率的方向。
- 补丁只在长度为 K 的已观测前缀上学习，然后在后续帧上保持不变地使用。
- 默认设置包括 K=40、3x3 token 补丁，对应 42x42 像素、50 次 SGD 迭代、100 个采样目标方向，以及损失权重 lambda_sem=1.0 和 lambda_traj=12.0。

## 结果
- 在 LIBERO 上、以 OpenVLA 为受害模型时，与 UADA、UPA 和 TMA 相比，该方法在 Spatial、Object、Goal 和 Long 四个套件中几乎所有列出的设置里都报告了最佳 ASR。
- 在 K=30 时，ASR 在 Spatial 上为 73.8%，在 Object 上为 90.7%，在 Goal 上为 72.8%，在 Long 上为 86.6%。同列中最好的基线 ASR 分别是 59.1%、63.8%、59.5% 和 57.2%。
- 在 K=40 时，ASR 在 Spatial 上为 72.4%，在 Object 上为 89.7%，在 Goal 上为 71.7%，在 Long 上为 89.1%。最好的基线 ASR 分别是 52.6%、61.9%、59.4% 和 59.1%。
- 对于 K=30 的 nASR，该方法在 Spatial 上得分 87.5%，在 Object 上得分 96.0%，在 Goal 上得分 79.6%，在 Long 上得分 93.9%。最好的基线 nASR 分别是 77.7%、82.3%、74.4% 和 84.9%。
- 注意力定位有帮助：在四个 LIBERO 套件上取平均时，最后一帧定位在 K=30 时得到 81.0% 的 ASR 和 89.3% 的 nASR，而前缀均值定位分别是 77.7% 和 86.6%。
- 摘要说该攻击在仿真和真实机器人上都做了测试，但所示文本里只有 LIBERO 结果的定量表格。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.03556v1](https://arxiv.org/abs/2606.03556v1)
