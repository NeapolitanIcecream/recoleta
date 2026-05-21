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
CoME 是一种扩散世界模型方法，它结合短期、长期和空间记忆专家，使生成的未来与过去观察保持一致。

## 问题
- 世界模型在规划和导航中需要长历史记录，因为智能体可能会重访某个地点，并且应当预测出它之前看到的相同物体和布局。
- Transformer 上下文成本高，因为注意力计算按平方增长；循环模型和状态空间模型会压缩历史并丢失细节。
- 长上下文视频预测还需要空间一致性，因为外观相似的位置可能导致错误回忆。

## 方法
- 该方法在采样时用 Product of Contrastive Experts 规则组合多个扩散专家。
- 短期记忆专家关注近期上下文，论文描述为约 10-100 张图像，用于保持局部运动和视觉细节稳定。
- 长期记忆专家通过在约 100-1000 张图像上进行测试时微调，将情节历史存入 LoRA 适配器权重。
- 空间长期记忆专家以位姿、地图或其他空间信号为条件生成，使预测既匹配位置，也匹配外观。
- 对比规则将每个条件专家与其无条件版本进行比较，以减少虚假模式，同时在 KDE 分析中不收窄每个局部模式。

## 结果
- 在 Memory Maze 上，Base 模型报告 LPIPS 0.209、SSIM 0.771、PSNR 19.16。
- 加入 STM 后，Memory Maze 结果提升到 LPIPS 0.156、SSIM 0.820、PSNR 21.29。
- 可见表格显示，在 Memory Maze 上，相比 Base，STM 使 LPIPS 提升 0.053、SSIM 提升 0.049、PSNR 提升 2.13。
- 摘录称 LTM、SLTM，尤其是 STM+LTM 进一步提升了时间一致性，并超过列出的基线，但包含其确切数值的行被截断。
- 实验使用 Memory Maze，其中包含 30k 条、每条 1k 帧的轨迹；RECON，其中包含超过 5k 条真实户外轨迹；以及带有相机位姿的 RE10K 室内场景。
- 基线训练 150k 步；DiT 基线使用 3 个上下文帧预测 17 帧，而 STM 专家使用 33 个条件帧预测 17 帧。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.18813v1](https://arxiv.org/abs/2605.18813v1)
