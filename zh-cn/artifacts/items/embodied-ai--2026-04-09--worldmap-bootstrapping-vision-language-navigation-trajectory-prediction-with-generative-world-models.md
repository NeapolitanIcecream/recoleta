---
source: arxiv
url: http://arxiv.org/abs/2604.07957v1
published_at: '2026-04-09T08:21:58'
authors:
- Hongjin Chen
- Shangyun Jiang
- Tonghua Su
- Chen Gao
- Xinlei Chen
- Yong Li
- Zhibo Chen
topics:
- vision-language-navigation
- world-models
- trajectory-prediction
- teacher-student-learning
- embodied-ai
relevance_score: 0.79
run_id: materialize-outputs
language_code: zh-CN
---

# WorldMAP: Bootstrapping Vision-Language Navigation Trajectory Prediction with Generative World Models

## Summary
## 概要
WorldMAP 通过把世界模型生成的未来视图转换为带伪标签的路径，来训练导航轨迹预测器。论文认为，在单图像视觉语言导航中，世界模型更适合用作监督信号生成器，而不是测试时规划器。

## 问题
- 任务是在未见过的环境中，根据一张第一人称图像和一条语言指令，预测一条有地面约束、可通行的导航轨迹。
- 直接使用视觉语言模型时，输出的路径往往不稳定，容易忽略几何结构、障碍物或正确的停止位置。
- 世界模型可以生成看似合理的未来视图，但这些视图不能直接提供训练可靠预测器所需的结构化目标、障碍物和路径监督信号。

## 方法
- WorldMAP 采用教师-学生架构。教师模型利用生成的未来视频构建语义-空间记忆，以及一个共享的鸟瞰视角规划空间。
- 教师模型用 CLIP 检索与指令相关的视图，使用 VLM 和 UniPixel 分割目标区域与障碍物，将其投影到 BEV 中，并构建代价地图。
- 然后，它在该代价地图上运行 Fast Marching Method 规划，生成轨迹伪标签。
- 轻量级学生 VLM 接收原始图像和指令，直接预测航路点，并使用多假设轨迹头和最佳匹配训练损失。
- 在推理时，只有学生模型运行，因此高成本的世界模型和规划流程只在训练阶段使用。

## 结果
- 在 Target-Bench 上，WorldMAP 在对比方法中取得了最好的 ADE 和 FDE：**ADE 42.06**、**FDE 38.87**、**DTW 31.95**。
- 与表现最好的对比基线 **Gemini-3-Pro** 相比，WorldMAP 将 **ADE 从 51.27 降到 42.06**，提升 **18.0%**；将 **FDE 从 67.19 降到 38.87**，提升 **42.1%**；DTW 结果接近（**31.95 vs. 31.63**）。
- WorldMAP 使用 **Qwen3-VL-8B** 作为学生模型，并且明显优于开源 VLM 的直接预测结果。例如，直接使用 **Qwen3-VL-8B** 的成绩是 **ADE 183.93、FDE 339.58、DTW 177.33**。
- 它也优于结合世界模型的基线 **MindJourney**，后者的结果是 **ADE 152.41、FDE 250.17、DTW 84.84**。
- 论文的主要具体结论是，生成的未来视图更适合作为有地面约束规划的训练监督，而不是作为测试时直接推理的额外证据。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07957v1](http://arxiv.org/abs/2604.07957v1)
