---
source: arxiv
url: https://arxiv.org/abs/2606.10862v1
published_at: '2026-06-09T13:39:49'
authors:
- Taishan Li
- Jiwen Zhang
- Siyuan Wang
- Xuanjing Huang
- Zhongyu Wei
topics:
- vision-language-action
- robot-manipulation
- occlusion-robustness
- viewpoint-imagination
- robot-benchmarks
- world-models
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# LIBERO-Occ: Evaluating and Improving Vision-Language-Action Models under Scene-Induced Occlusion via Viewpoint Imagination

## Summary
## 摘要
LIBERO-Occ 测试 VLA 机器人策略在任务物体或目标区域被真实场景几何遮挡时的表现。VIM 通过从可见相机图像生成一个可能的腕部/夹爪视角，并把这个生成视角用于动作预测，来改进遮挡下的操作表现。

## 问题
- 标准的 LIBERO 风格 VLA 评估通常假设任务相关物体可见，但真实操作场景里，物体、容器，或两者都可能被遮挡。
- 遮挡把动作预测变成部分可观测问题：策略可能需要物体位置、形状或目标区域信息，而相机看不到这些内容。
- 这篇论文对可部署的机器人策略有意义，因为增加摄像头或主动相机硬件会带来标定、安装和维护成本。

## 方法
- 作者在保留任务语义并通过演示回放检查可执行性的前提下，给 LIBERO 任务加入物理遮挡物，构建了 LIBERO-Occ。
- LIBERO-Occ 包含 2,000 个受遮挡任务，覆盖被操作物体遮挡、容器遮挡和双重遮挡，并按基于分割的可见性损失分成轻度、中度和重度三档。
- VIM 先根据被遮挡的主视角和语言指令，预测一个互补视角的视觉 token，例如腕部/夹爪视角。
- 策略再在主视角、指令和想象出的互补视角条件下预测动作 token。
- 训练分两阶段：先做视角生成，再做联合动作预测与视角生成损失训练，权重 λ = 0.5。

## 结果
- 在没有真实互补视角的 LIBERO-Occ 上，VIM 的平均成功率达到 65.05%，比最强基线 UniVLA 的 57.10% 高 7.95 个百分点。
- OpenVLA-OFT 在原始 LIBERO 上的平均成绩最好，为 95.75%，但在 LIBERO-Occ 上降到 47.95%；VIM 在原始 LIBERO 上得分 90.75%，在 LIBERO-Occ 上得分 65.05%。
- 在列出的无互补视角方法里，VIM 从原始 LIBERO 到遮挡版本的平均下降最小，为 25.70 分；对比 UniVLA 的 31.15、OpenVLA 的 52.00、OpenVLA-OFT 的 47.80、π-0 的 39.95 和 π-0.5 的 49.45。
- 给 VIM 模型提供真实的互补视角后，LIBERO-Occ 的平均成功率从 65.05% 提升到 74.00%，这给缺失视觉证据提供了上限参考。
- 在原始 LIBERO 上，互补视角带来的性能差距为 2.2 到 8.3 分；在 LIBERO-Occ 上，这个差距扩大到 22.1 到 45.5 分，说明遮挡会增加对隐藏视觉证据的依赖。
- 按遮挡目标类型划分，VIM 在被操作物体遮挡上得分 54.67%，在容器遮挡上得分 91.33%，在双重遮挡上得分 35.43%，在每一组里都领先列出的基线。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.10862v1](https://arxiv.org/abs/2606.10862v1)
