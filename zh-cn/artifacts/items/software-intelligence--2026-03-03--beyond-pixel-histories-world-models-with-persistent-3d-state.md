---
source: arxiv
url: http://arxiv.org/abs/2603.03482v1
published_at: '2026-03-03T19:58:31'
authors:
- Samuel Garcin
- Thomas Walker
- Steven McDonagh
- Tim Pearce
- Hakan Bilen
- Tianyu He
- Kaixin Wang
- Jiang Bian
topics:
- world-models
- 3d-scene-representation
- interactive-video-generation
- neural-rendering
- diffusion-models
relevance_score: 0.34
run_id: materialize-outputs
language_code: zh-CN
---

# Beyond Pixel Histories: World Models with Persistent 3D State

## Summary
PERSIST提出一种带有持久3D状态的交互式世界模型，不再只依赖过去像素帧，而是显式维护一个会随时间演化的潜在3D场景。这样可以在长时序生成中获得更好的空间记忆、几何一致性和稳定性。

## Problem
- 现有自回归视频/世界模型通常只看有限长度的像素历史，导致一旦超出上下文窗口，就容易遗忘先前见过的区域。
- 仅从像素中隐式学习3D结构很困难，尤其在视角变化、遮挡、离屏动态和长时回访场景下，会出现几何不一致和时序漂移。
- 这很重要，因为交互式生成不仅要单帧看起来真实，还要在长回合中维持可持续、可回访、可供智能体训练的稳定世界。

## Approach
- 核心思想：把“记忆”从像素历史改成一个持续更新的潜在3D世界状态。模型维护三部分：3D world-frame、相机状态、以及从3D到像素的渲染模块。
- world-frame模型用3D潜变量预测场景如何随动作演化；相机模型预测玩家视角；随后通过几何投影把3D体素特征映射到屏幕，再由像素生成器生成当前帧。
- 像素生成器相当于“学习版延迟着色器”：它以投影后的3D特征为主要条件，再补充纹理、光照、粒子和屏幕特效等3D表示未直接覆盖的信息。
- 为缓解自回归推理中的曝光偏差，作者对扩散/flow模型使用diffusion forcing，并在训练不同组件时加入噪声增强，使各模块可分开训练、推理时直接组合。
- 训练时依赖环境提供的3D voxel world-frame与相机参数监督；推理时可仅用单张RGB初始帧启动，也支持给定初始3D world-frame以进一步提升效果。

## Results
- 在Luanti/Craftium上，作者收集约4000万次环境交互、约10万条轨迹、共460小时24Hz游戏数据；3D观测为以玩家为中心的48^3体素网格。
- 与Oasis相比，PERSIST-S的FVD从706降到209，PERSIST-XL降到181；相对WorldMem的596也显著更低，说明视频分布质量和长程稳定性更好。
- 用户研究中，PERSIST-S在单帧视觉质量/3D一致性/时序一致性/总体评分上达到2.8/2.7/2.5/2.6；而Oasis为2.1/1.9/1.8/1.9，WorldMem为1.7/1.7/1.5/1.5（评分范围1-5）。
- 最强配置PERSIST-XL+w0在FVD上达到116，并在用户评分上达到3.2（视觉质量）、2.8（3D一致性）、2.8（时序一致性）、3.0（总体），优于所有基线和其他PERSIST配置。
- 论文还声称模型可从单张图像合成多样3D环境、支持600步自回归rollout，并支持在3D空间中直接编辑地形/生物群系/树木等对象，实现几何感知控制；这些能力主要以定性结果展示。

## Link
- [http://arxiv.org/abs/2603.03482v1](http://arxiv.org/abs/2603.03482v1)
