---
source: arxiv
url: https://arxiv.org/abs/2606.09803v1
published_at: '2026-06-08T17:54:10'
authors:
- Wayne King
- Zeyue Xue
- Yuxuan Bian
- Jie Huang
- Haoran Li
- Yaowei Li
- Yaofeng Su
- Yuming Li
- Haoyu Wang
- Shiyi Zhang
- Songchun Zhang
- Yuwei Niu
- Sihan Xu
- Junhao Zhuang
- Haoyang Huang
- Nan Duan
topics:
- action-world-models
- memory-mechanisms
- video-diffusion
- state-space-models
- revisit-consistency
- evaluation-protocol
relevance_score: 0.64
run_id: materialize-outputs
language_code: zh-CN
---

# Echo-Memory: A Controlled Study of Memory in Action World Models

## Summary
## 摘要
Echo-Memory 是一项关于动作条件视频世界模型中记忆机制的对照研究。它发现，重放质量和回访记忆会把方法排出不同顺序，而按块的状态空间递归在开放域回访上得分最高。

## 问题
- 当摄像机离开后又返回时，动作世界模型可能会让场景变化，或替换掉一个显著物体，即使局部视频看起来合理。
- 以往的记忆比较会混在一起考虑骨干网络、训练、检索、采样和指标的变化，因此很难单独看出记忆机制的作用。
- 这很重要，因为跟随摄像机的视频不足以构成世界模型；模型必须在生成的多个片段之间保留物体身份和场景状态。

## 方法
- 这项研究固定了视频扩散变换器骨干、优化器、摄像机-动作表示、采样器、训练方案和评估流程。
- 只改变记忆形式：原始上下文、基于压缩的记忆、带不同读出路径的空间摘要，以及状态空间递归。
- 共享输入接口使用首帧、文本提示、历史上下文和逐帧的 12D 相对 RT 摄像机-动作序列。
- 训练使用 81 帧片段、352×640 分辨率、AdamW、8 张 A100-80G GPU、5000 步、只监督目标帧，以及 10% 的重叠丢弃策略。
- 评估分三条分支：重放的 PSNR/SSIM/LPIPS，域内循环返回的 PSNR/SSIM/LPIPS，以及由 Qwen3-VL-30B-A3B 按 0-100 的 VLM 量表打分的开放域回访。

## 结果
- 原始上下文是一个强基线：开放域 VLM 从仅锚点 I2V 的 12.25 升到 K=5 时的 50.75，K=20 时的 58.63。
- 按块的 State-Space 在主表中拿到最高的开放域回访分数：69.00 O-V，高于 Context K=20 的 58.63，也高于旧版混合 State-Space 的 34.75。
- 重放指标不能预测回访记忆：Spatial Memory 的重放 PSNR 很高，达到 13.60，但开放域 VLM 只有 6.00。
- Context K=20 在主表重放指标里拿到最好的 SSIM 和 LPIPS：SSIM 为 0.449，LPIPS 为 0.496，而它的开放域 VLM 为 58.63。
- 域内回访也会把方法排出不同顺序：State-Space 旧版混合的 ID-PSNR 为 12.23，而 Context K=20 的 ID-PSNR 为 11.07，但开放域 VLM 更好。
- VLM 裁判的校验结果显示，它与 Claude Opus 4.6、GPT-5.5 和人工锚点的相关性都高于 0.90；相对于 Qwen3-VL，Pearson 相关系数分别为 0.93、0.94 和 0.96。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09803v1](https://arxiv.org/abs/2606.09803v1)
