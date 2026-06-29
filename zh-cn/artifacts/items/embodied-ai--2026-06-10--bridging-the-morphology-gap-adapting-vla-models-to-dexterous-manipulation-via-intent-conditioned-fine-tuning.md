---
source: arxiv
url: https://arxiv.org/abs/2606.12109v1
published_at: '2026-06-10T14:03:52'
authors:
- Chuanke Pang
- Junyi Huang
- Zhijun Zhao
- Yaobing Wang
- Kun Xu
- Xilun Ding
topics:
- vision-language-action
- dexterous-manipulation
- robot-foundation-model
- policy-finetuning
- diffusion-policy
- cross-morphology-adaptation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Bridging the Morphology Gap: Adapting VLA Models to Dexterous Manipulation via Intent-Conditioned Fine-Tuning

## Summary
## 总结
InDex 通过保留 VLA 在机械臂层面的空间能力，并加入一个受意图条件约束的扩散头来控制手指，把预训练 VLA 策略适配到高自由度灵巧手。论文声称，在四个灵巧操作任务上，每个任务使用 100 条演示就能取得明显更高的仿真表现。

## 问题
- 大多数预训练 VLA 机器人策略面向 1 自由度并联夹爪，因此它们的动作头与多指机械手不匹配。
- 直接对灵巧动作做端到端微调，会抹去有用的 VLA 空间行为，而且在高自由度演示很少时容易塌缩。
- 这个问题很重要，因为堆叠、螺母装配这类接触丰富任务需要精确的手指运动，不只是把物体移动到位。

## 方法
- 该方法把灵巧手姿态转换为标量抓取意图 γ，取值范围为 [0,1]，其中 0 表示张开，1 表示闭合。计算方式是拇指指尖与其他指尖质心之间的距离。
- 第 1 阶段用 LoRA 微调 π0.5 动作专家，同时冻结 VLM 主干。它预测 6 自由度机械臂运动和粗粒度手部意图。
- 第 2 阶段冻结 VLA 主干，训练一个用于 12 维动作的去噪扩散动作头，条件包括 VLA 视觉嵌入、本体感觉和 γ。
- 扩散头负责生成手指级动作，VLA 保留更高层的到达和视觉-语言行为。

## 结果
- 在四个 robosuite 仿真任务上，π0.5+InDex 的平均任务成功率为 85.8%，对比 π0.5 为 50.3%，Diffusion Policy 为 42.8%，UniVLA 为 37.8%，OpenVLA 为 31.8%，ACT 为 34.5%。
- π0.5+InDex 的单任务成功率分别是：Lift 95%，Stack 83%，Pick & Place 89%，Nut Assembly 76%。
- π0.5+InDex 的分阶段平均成功率为：到达 92.8%，抓取 88.3%，完整任务 85.8%。在相同指标上，π0.5 基线分别为 76.0%、56.0% 和 50.3%。
- 在 Nut Assembly 上，π0.5 的到达成功率从 57% 降到任务成功率 25%，而 π0.5+InDex 报告的到达、抓取和任务成功率分别为 87%、79% 和 76%。
- 评估使用了每个任务 100 条成功演示和 100 次独立试验，并对物体姿态和光照做了领域随机化。
- 消融实验摘录显示，原生 π0.5 直接投影的平均成功率为 4.0%，不使用意图条件时为 17.0%。这支持 γ 意图信号的作用，不过所给文本中的完整消融表被截断了。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.12109v1](https://arxiv.org/abs/2606.12109v1)
