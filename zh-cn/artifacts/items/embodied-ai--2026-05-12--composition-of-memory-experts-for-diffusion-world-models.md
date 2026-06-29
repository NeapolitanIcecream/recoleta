---
source: arxiv
url: https://arxiv.org/abs/2605.18813v1
published_at: '2026-05-12T09:43:10'
authors:
- Sebastian Stapf
- Pablo Acuaviva Huertos
- Aram Davtyan
- Paolo Favaro
topics:
- diffusion-world-models
- long-term-memory
- product-of-experts
- video-prediction
- navigation-planning
relevance_score: 0.58
run_id: materialize-outputs
language_code: zh-CN
---

# Composition of Memory Experts for Diffusion World Models

## Summary
## 摘要
CoME 是一种扩散世界模型方法，它把短期记忆、长期记忆和空间记忆专家组合起来，让生成的未来与过去观测保持一致。

## 问题
- 世界模型需要很长的历史信息来做规划和导航，因为智能体可能会回到某个地点，并且应当预测出它之前看到的相同物体和布局。
- Transformer 的上下文代价很高，因为注意力的计算量会随长度平方增长，而循环模型和状态空间模型会更高效地压缩历史，但会丢失细节。
- 长上下文视频预测还需要空间一致性，因为外观相近的位置可能导致错误的记忆回忆。

## 方法
- 该方法在采样时用 Product of Contrastive Experts 规则组合多个扩散专家。
- 短期记忆专家关注最近的上下文，文中描述为大约 10 到 100 张图像，以保持局部运动和视觉细节稳定。
- 长期记忆专家通过测试时微调把情节历史存到 LoRA 适配器权重中，使用大约 100 到 1000 张图像。
- 空间长期记忆专家把位姿、地图或其他空间信号作为生成条件，让预测在位置和外观上都匹配。
- 对比规则把每个条件专家和它的无条件版本进行比较，在 KDE 分析中减少伪模式，同时不收缩每个局部模式。

## 结果
- 在 Memory Maze 上，Base 模型的 LPIPS 为 0.209，SSIM 为 0.771，PSNR 为 19.16。
- 加入 STM 后，Memory Maze 的结果变为 LPIPS 0.156、SSIM 0.820、PSNR 21.29。
- 可见的表格显示，STM 在 Memory Maze 上相对 Base 让 LPIPS 提升 0.053、SSIM 提升 0.049、PSNR 提升 2.13。
- 摘要说 LTM、SLTM，尤其是 STM+LTM 进一步提升了时间一致性，并且超过了列出的基线，但这些行的具体数值被截断了。
- 实验使用了 Memory Maze，其中有 3 万条、每条 1000 帧的轨迹；RECON，其中有超过 5000 条真实户外轨迹；以及带相机位姿的 RE10K 室内场景。
- 基线训练了 15 万步；DiT 基线用 3 帧上下文预测 17 帧，而 STM 专家用 33 帧条件帧预测 17 帧。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18813v1](https://arxiv.org/abs/2605.18813v1)
