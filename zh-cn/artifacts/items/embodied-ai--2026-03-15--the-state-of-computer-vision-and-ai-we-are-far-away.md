---
source: hn
url: http://karpathy.github.io/2012/10/22/state-of-computer-vision/
published_at: '2026-03-15T23:41:14'
authors:
- stickynotememo
topics:
- computer-vision
- scene-understanding
- common-sense-reasoning
- embodiment
- ai-critique
relevance_score: 0.63
run_id: materialize-outputs
language_code: zh-CN
---

# The state of Computer Vision and AI: we are far away

## Summary
这是一篇观点性文章，论证当时的计算机视觉与AI距离“像人一样理解图像”还非常遥远。作者用一张搞笑照片说明，真正的视觉理解需要远超分类与检测的常识、物理、社会认知与心智推理。

## Problem
- 文章讨论的问题是：**如何让机器像人一样从一张图像中理解场景、物体交互、物理因果、人物身份、意图与心理状态**，而不仅是做标签分类或框选目标。
- 这很重要，因为人类对图像的自然理解依赖大量隐含知识；如果缺少这些能力，现有CV系统即使在基准上表现不错，也离真正智能相差甚远。
- 作者指出核心难点不只是推理算法，还包括**如何获取能支撑这些推理的训练数据与经验**，例如物体如何工作、人与环境如何交互等。

## Approach
- 这不是一篇提出新算法的论文，而是一篇**概念性/批判性分析**：通过一个“奥巴马偷偷踩体重秤”的照片案例，逐层拆解人类理解笑点所需的知识链条。
- 作者认为核心机制应包含多层推理：**3D场景理解、镜像辨识、身份识别、人体姿态与物体可供性、物理因果、可见性/注意力、未来事件预测、他人心理状态建模**。
- 文中批评当时主流CV任务（如ImageNet分类、Pascal VOC检测）过于狭窄、割裂，无法逼近完整场景理解。
- 作者进一步提出一种方向性判断：仅靠更多静态图像/视频/文本和训练技巧可能不够，**还可能需要embodiment（具身经验）**，让系统通过长期、结构化、时间连贯的交互经验学习世界。

## Results
- **没有提供实验、数据集或定量指标**；这是一篇立场/评论文章，不报告可复现实验结果。
- 最强的具体主张是：当时SOTA主要评测在**ImageNet的1-of-k图像分类**和**Pascal VOC目标检测/边界框**等任务上，但这些任务与人类式场景理解之间存在巨大鸿沟。
- 作者的关键结论是：仅从一张RGB图像中恢复背后的“巨大知识冰山”极其困难，当前CV/AI“非常、非常遥远”。
- 另一个重要前瞻性观点是：要达到更接近人类的视觉理解，系统可能需要**多年、结构化、时间连贯的经验以及主动交互能力**，即某种具身学习框架。

## Link
- [http://karpathy.github.io/2012/10/22/state-of-computer-vision/](http://karpathy.github.io/2012/10/22/state-of-computer-vision/)
