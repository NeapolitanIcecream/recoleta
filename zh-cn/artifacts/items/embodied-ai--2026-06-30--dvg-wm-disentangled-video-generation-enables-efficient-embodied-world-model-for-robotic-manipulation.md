---
source: arxiv
url: https://arxiv.org/abs/2606.32028v1
published_at: '2026-06-30T17:54:32'
authors:
- Ziyu Shan
- Zhenyu Wu
- Xiaofeng Wang
- Zheng Zhu
- Ziwei Wang
topics:
- embodied-world-model
- robotic-manipulation
- video-generation
- language-conditioned-planning
- imitation-learning
- contact-rich-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# DVG-WM: Disentangled Video Generation Enables Efficient Embodied World Model for Robotic Manipulation

## Summary
## 摘要
DVG-WM 是一个用于机器人操作的两阶段视频世界模型，将低分辨率动态预测与高分辨率视频细化分离。它声称在 LIBERO 上，相比多个视频规划基线，视频保真度更高、物体定位更好、推理更快。

## 问题
- 机器人视频世界模型需要预测接触、遮挡和物体运动，同时生成清晰的高分辨率帧。
- 单阶段视频生成器在高分辨率合成上花费许多去噪步骤，这会拖慢重复规划调用。
- 粗糙或缓慢的预测会损害操作性能，因为很小的接触误差也可能改变动作计划。

## 方法
- 模型接收初始观测和语言指令，然后预测一段 49 帧的未来视频。
- 低分辨率预览阶段使用带 LoRA 的 CogVideoX-5B，在 256×384 分辨率下生成粗略的潜在动态。
- 高分辨率细化阶段使用较小的 CogVideoX-2B 模型，生成 480×720 视频潜变量。
- 流匹配将上采样后的低分辨率潜变量序列直接映射到高分辨率潜变量，在推理时使用 4 个细化步骤。
- 潜变量退化训练方法会扰动预览潜变量，使细化模型学习重新生成夹爪与物体的接触细节，而不只是放大像素。

## 结果
- 在 LIBERO 视频预测上，DVG-WM 报告的 PSNR 为 20.019；相比之下，CogVideoX-5B 为 19.286，Wan2.1-14B 为 18.964，LongScape 为 19.977，LVP-14B 为 19.582。
- DVG-WM 报告的 LPIPS 为 0.120，FVD 为 152.36；相比之下，LongScape 的 LPIPS 为 0.123、FVD 为 153.72，CogVideoX-5B 的 LPIPS 为 0.138、FVD 为 171.24。
- 物体级准确率达到 89%；相比之下，LVP-14B 为 80%，CogVideoX-5B 为 76%，Wan2.1-14B 为 68%。
- SSIM 为 0.783，低于 LongScape 的 0.788，但高于 CogVideoX-5B 的 0.761、Wan2.1-14B 的 0.732 和 LVP-14B 的 0.765。
- 推理时间为 88.7 秒；相比之下，CogVideoX-5B 为 236.8 秒，Wan2.1-14B 为 312.0 秒，LVP-14B 为 354.2 秒，最高加速 3.97×。
- 论文还报告了在一个包含 7K 条轨迹的真实世界数据集上结合动作专家进行的测试，但所给摘录没有包含真实世界成功率的数值。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.32028v1](https://arxiv.org/abs/2606.32028v1)
