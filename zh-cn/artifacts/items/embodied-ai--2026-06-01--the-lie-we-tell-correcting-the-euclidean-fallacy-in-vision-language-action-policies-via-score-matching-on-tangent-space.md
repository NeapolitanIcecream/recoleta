---
source: arxiv
url: https://arxiv.org/abs/2606.01847v1
published_at: '2026-06-01T07:59:29'
authors:
- Bing-Cheng Chuang
- I-Hsuan Chu
- Bor-Jiun Lin
- YuanFu Yang
- Min Sun
- Chun-Yi Lee
topics:
- vision-language-action
- diffusion-policy
- lie-groups
- se3-robotics
- robot-manipulation
- equivariant-policy
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# The Lie We Tell: Correcting the Euclidean Fallacy in Vision Language Action Policies via Score Matching on Tangent Space

## Summary
## 摘要
Lie Diffuser Actor 让基于扩散的机器人位姿生成保持在 SE(3) 上，而不是把位姿展平成欧几里得向量。论文称，这样可以减少无效旋转，保持坐标系等变性，并在基准测试中优于 3D Diffuser Actor 和 OpenVLA-OFT 变体。

## 问题
- 许多基于扩散的 VLA 策略把机器人工具端位姿编码成 12 维欧几里得向量，用展平的旋转矩阵加平移表示。
- 给旋转矩阵加入高斯噪声会产生非正交旋转、对坐标系敏感的 score，以及效率较低的位姿路径。
- 这会影响操作任务，因为无效或不稳定的位姿轨迹会抬高控制成本，并削弱在不同相机或工作空间坐标系下的迁移。

## 方法
- 该方法 Lie Diffuser Actor 在切空间 se(3) 中加入噪声，把位姿表示为 6 维 twist，包含角速度和线速度分量。
- 它用指数映射把每个带噪 twist 映射回 SE(3)，所以每一步去噪都保持为有效的刚体变换。
- 反向扩散模型在 se(3) 中预测 score 向量，再通过群乘法更新位姿，而不是做向量相加。
- 该架构在 3D Diffuser Actor 的基础上加入了 RGB-D 点云编码、CLIP 文本特征、Transformer 去噪器和切空间预测头。
- 论文给出了关于流形封闭性、左不变等变性，以及类似测地线的螺旋运动轨迹的理论论断。

## 结果
- 在 CALVIN ABC→D 上，Lie Diffuser Actor 的平均任务长度达到 3.512，3D Diffuser Actor 为 3.27，论文报告提升 7.3%。
- 在 CALVIN ABC→D 上，Lie Diffuser Actor 的逐步成功率为 SR1 93.7、SR2 83.4、SR3 70.3、SR4 57.6、SR5 46.2。
- 在 CALVIN ABCD→D 上，Lie Diffuser Actor 的平均任务长度达到 3.584，3D Diffuser Actor 为 3.288；SR5 从 41.6 提升到 53.7。
- 在 OpenVLA-OFT 跨架构验证中，SE(3) score matching 将 LIBERO Long 成功率从 92.20% 提升到 94.13%。
- 在旋转约束分析中，该方法报告的正交性违反低于 3D Diffuser Actor：中位数低 5.7%，P90 低 11.8%，P95 低 5.4%，P99 低 2.6%。
- 真实机器人实验据称在大多数任务上优于基线，但摘要没有给出任务级数量或成功率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.01847v1](https://arxiv.org/abs/2606.01847v1)
