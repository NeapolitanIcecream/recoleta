---
source: arxiv
url: https://arxiv.org/abs/2606.06155v1
published_at: '2026-06-04T13:28:51'
authors:
- Qize Yu
- Jiadi You
- Yuran Wang
- Jiaqi Liang
- Bowen Ping
- Yang Tian
- Yue Chen
- Minghong Cai
- Zeying Gong
- Ruihai Wu
- Yinchuan Li
- Junwei Liang
- Yingcong Chen
topics:
- vision-language-action
- robot-foundation-model
- affordance-learning
- generalist-robot-policy
- dexterous-manipulation
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# AffordanceVLA: A Vision-Language-Action Model Empowering Action Generation through Affordance-Aware Understanding

## Summary
## 摘要
AffordanceVLA 在视觉-语言-行动机器人策略中加入了可供性预测，让模型预测该用哪个物体、在哪里接触，以及 3D 形状该如何引导动作。

## 问题
- 直接的 VLA 策略把图像和语言映射到机器人动作，但 VLM 特征偏语义，而机器人动作需要 3D 空间控制。
- 密集视频预测会引入多余像素并拖慢推理，而粗粒度的理由常常漏掉接触位置和几何信息。
- 这个问题很重要，因为当策略关注了错误的物体、错误的接触区域或错误的空间布局时，操作就会失败。

## 方法
- 模型使用三个 Transformer 专家：理解专家用于图像-语言特征，可供性生成专家用于任务相关的物理线索，动作专家用于动作片段。
- Which2Act 预测目标物体裁剪的潜变量，促使模型关注指令中提到的物体。
- Where2Act 预测 2D 可供性图，为策略提供明确的交互区域。
- How2Act 预测 3D 形状和一个 10-DoF 布局向量，用于旋转、缩放和位移。
- 训练分为 3 个阶段：可供性接地预训练、加入可供性的机器人联合训练，以及面向 LIBERO、CALVIN 和真实环境部署的目标任务后训练。

## 结果
- 给出的摘录没有包含 LIBERO 或 CALVIN 的成功率表，因此这里看不到基准百分比和与基线的差距。
- 论文声称在 LIBERO 和 CALVIN 的仿真任务上表现强，在真实世界任务上也有提升，但摘录里只给了定性描述。
- 数据流水线通过关键帧提取、Claude Opus 4.5、Qwen3-VL、RexOmni、SAM 和 SAM-3D 生成了超过 100,000 条可供性标注。
- 第 I 阶段的可供性损失权重中，Which2Act、Where2Act 和 shape 都是 0.1，layout 是 0.04。
- 第 II 阶段的动作损失权重是 1.0，可供性损失权重是 0.5；第 III 阶段将可供性权重降到 0.15，用于任务适配。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.06155v1](https://arxiv.org/abs/2606.06155v1)
