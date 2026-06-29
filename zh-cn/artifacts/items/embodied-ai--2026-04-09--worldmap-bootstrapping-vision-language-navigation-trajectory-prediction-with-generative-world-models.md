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
## 摘要
WorldMAP 通过把世界模型生成的未来视图转成带伪标签的路径，来训练导航轨迹预测器。论文认为，在单图视觉语言导航中，世界模型作为监督生成器的作用，比作为测试时规划器更大。

## 问题
- 任务是：在未见环境中，根据一张自我视角图像和一条语言指令，预测一条有依据、可通行的导航轨迹。
- 直接的视觉语言模型常会输出不稳定的路径，漏掉几何关系、障碍物或正确的停止点。
- 世界模型可以生成看起来合理的未来视图，但这些视图不能直接提供训练可靠预测器所需的结构化目标、障碍物和路径监督。

## 方法
- WorldMAP 使用教师-学生框架。教师利用生成的未来视频构建语义-空间记忆和共享的鸟瞰图规划空间。
- 教师用 CLIP 检索与指令相关的视图，再用 VLM 和 UniPixel 分割目标区域和障碍物，把它们投影到 BEV 中，并构建代价地图。
- 然后在这张代价地图上运行快速行进法规划，生成轨迹伪标签。
- 一个轻量的学生 VLM 接收原始图像和指令，直接预测路径点，并使用多假设轨迹头和最佳匹配训练损失。
- 推理时只运行学生，因此昂贵的世界模型和规划流程只用于训练。

## 结果
- 在 Target-Bench 上，WorldMAP 在对比方法中取得最好的 ADE 和 FDE：**ADE 42.06**，**FDE 38.87**，**DTW 31.95**。
- 相比最强竞争基线 **Gemini-3-Pro**，WorldMAP 将 **ADE 从 51.27 降到 42.06**，提升 **18.0%**；将 **FDE 从 67.19 降到 38.87**，提升 **42.1%**；DTW 也接近（**31.95 对 31.63**）。
- WorldMAP 使用 **Qwen3-VL-8B** 作为学生模型，明显优于直接的开源 VLM 预测。例如，直接使用 **Qwen3-VL-8B** 时，得分为 **ADE 183.93，FDE 339.58，DTW 177.33**。
- 它也超过了加入世界模型的基线 **MindJourney**，其结果为 **ADE 152.41，FDE 250.17，DTW 84.84**。
- 论文的核心具体结论是：生成的未来视图更适合作为具身规划的训练监督，而不是作为直接推理的额外测试时证据。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07957v1](http://arxiv.org/abs/2604.07957v1)
