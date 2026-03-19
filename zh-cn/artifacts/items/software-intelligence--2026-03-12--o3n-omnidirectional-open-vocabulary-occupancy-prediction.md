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
- 3d-occupancy-prediction
- open-vocabulary
- omnidirectional-vision
- embodied-ai
- mamba
- scene-understanding
relevance_score: 0.29
run_id: materialize-outputs
language_code: zh-CN
---

# O3N: Omnidirectional Open-Vocabulary Occupancy Prediction

## Summary
O3N提出了首个仅用单张全景RGB图像进行端到端开放词汇3D占据预测的框架，目标是在360°场景中同时恢复几何与可扩展语义。它通过适配全景几何的3D表示、体素-文本代价聚合和无梯度模态对齐，提升对未见类别与跨场景的泛化能力。

## Problem
- 现有3D占据预测大多依赖有限视角输入和封闭类别集合，难以支持具身智能体在开放世界中的安全、完整感知。
- 全景图像采用ERP投影，会带来极区不连续、几何畸变和非均匀采样，导致3D几何恢复和语义对齐更困难。
- 直接做“像素-体素-文本”特征对齐容易对已见类别过拟合，从而削弱对新类别的开放词汇识别能力。

## Approach
- 提出**O3N**：首个**purely visual、end-to-end**的全景开放词汇占据预测框架，输入为单张全景RGB图像和类别文本。
- 用**Polar-spiral Mamba (PsM)**在极坐标/柱坐标体素上按螺旋方式扫描，并与立方体体素融合，以更自然地建模360°空间连续性和长程上下文。
- 用**Occupancy Cost Aggregation (OCA)**先计算体素嵌入与文本嵌入的相似度，形成体素-文本“代价体”，再做空间聚合和类别聚合，而不是生硬地直接对齐离散特征。
- 用**Natural Modality Alignment (NMA)**做无梯度的文本-原型对齐：利用EMA得到已见类原型，并通过随机游走式迭代更新文本/原型，缓解像素、体素、文本之间的模态鸿沟。
- 训练时把新类别统一为unknown，只用基类语义监督，并结合占据损失、体素-像素对齐损失和OCA损失联合优化。

## Results
- 论文声称在**QuadOcc**和**Human360Occ**两个全景占据基准上达到**state-of-the-art**。
- 在**QuadOcc**上，O3N相对基线提升**+2.21 mIoU**和**+3.01 Novel mIoU**；图1还给出其达到**16.54 mIoU**与**21.16 Novel mIoU**。
- 在**Human360Occ**上，O3N相对基线提升**+0.86 mIoU**和**+1.54 Novel mIoU**。
- 论文强调其不仅优于现有开放词汇占据方法，还**超过部分全监督方法**，但当前摘录未完整给出所有对比表的最终数字。
- 数据设定具有较强难度：**QuadOcc**中被设为新类别的体素约占**68%**；**Human360Occ**中新类别约占**75%**，且基类中有些类别占比**低于1%**。
- 基准规模方面，**QuadOcc**使用**64×64×8**体素网格、**6**个语义类加empty；**Human360Occ**使用**10**个语义类加empty，并包含同城/跨城评测划分。

## Link
- [http://arxiv.org/abs/2603.12144v1](http://arxiv.org/abs/2603.12144v1)
