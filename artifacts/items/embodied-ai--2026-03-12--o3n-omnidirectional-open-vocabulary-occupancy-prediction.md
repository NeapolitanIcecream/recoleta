---
source: arxiv
url: http://arxiv.org/abs/2603.12144v1
published_at: '2026-03-12T16:45:42'
authors:
- Mengfei Duan
- Hao Shi
- Fei Teng
- Guoqiang Zhao
- Yuheng Zhang
- Zhiyong Li
- Kailun Yang
topics:
- open-vocabulary-occupancy
- omnidirectional-perception
- 3d-scene-understanding
- mamba
- embodied-perception
relevance_score: 0.72
run_id: materialize-outputs
---

# O3N: Omnidirectional Open-Vocabulary Occupancy Prediction

## Summary
O3N提出了首个**纯视觉、端到端**的全景开放词汇3D占据预测框架，目标是在单张360°图像下同时重建几何与可扩展语义。它重点解决全景畸变、长程上下文建模和未见类别语义对齐问题，并在QuadOcc与Human360Occ上达到SOTA。

## Problem
- 现有3D占据预测通常依赖有限视角输入和封闭类别集合，难以满足具身智能体在开放世界中的**360°安全感知**需求。
- 全景ERP图像存在**几何畸变与非均匀采样**，会破坏空间连续性，增加远处区域语义稀疏和训练过拟合风险。
- 开放词汇设置下，**pixel-voxel-text**三模态对齐容易因训练只见过base classes而失配，导致对novel classes泛化差。

## Approach
- 提出**O3N**：输入单张全景RGB图像和类别文本，直接预测开放词汇3D occupancy，是论文声称的首个该任务的纯视觉端到端框架。
- 用**Polar-spiral Mamba (PsM)**在极坐标/柱坐标体素上做螺旋扫描与双分支建模，简单说就是按更符合360°几何的顺序聚合近到远的信息，并与笛卡尔体素融合，提升长程上下文和空间连续性建模。
- 用**Occupancy Cost Aggregation (OCA)**先计算“体素特征和文本特征有多匹配”的代价体，再做空间聚合和类别聚合，而不是直接硬对齐离散特征，以减轻开放词汇过拟合。
- 用**Natural Modality Alignment (NMA)**做无梯度文本-原型对齐：把文本嵌入和由像素特征得到的语义原型反复融合，得到更一致的共享语义空间，缓解pixel/voxel/text模态鸿沟。
- 框架可建立在MonoScene、SGN等占据网络上训练，损失由语义占据监督、voxel-pixel对齐和OCA损失组成。

## Results
- 在**QuadOcc**上，论文称相对baseline带来 **+2.21 mIoU** 和 **+3.01 Novel mIoU** 提升。
- 在**Human360Occ**上，论文称相对baseline带来 **+0.86 mIoU** 和 **+1.54 Novel mIoU** 提升。
- 图1给出的QuadOcc结果显示，O3N达到 **16.54 mIoU**、**21.16 Novel mIoU**，并宣称为该基准上的SOTA。
- 论文声称在**QuadOcc**和**Human360Occ**两个全景占据基准上均优于现有开放词汇占据方法，并且**超过部分全监督方法**。
- 数据设置上，QuadOcc把 **vehicle/road/building** 设为novel classes，占总体体素约 **68%**；Human360Occ把7个类设为novel，占约 **75%**，说明评测具有较强开放词汇难度。
- 摘要还声称具备显著的**跨场景泛化**与**语义可扩展性**，但在给定摘录中未提供更细的分数据集/分模型完整表格数值。

## Link
- [http://arxiv.org/abs/2603.12144v1](http://arxiv.org/abs/2603.12144v1)
