---
source: arxiv
url: http://arxiv.org/abs/2604.04138v1
published_at: '2026-04-05T14:53:43'
authors:
- Juhan Park
- Taerim Yoon
- Seungmin Kim
- Joonggil Kim
- Wontae Ye
- Jeongeun Park
- Yoonbyung Chai
- Geonwoo Cho
- Geunwoo Cho
- Dohyeong Kim
- Kyungjae Lee
- Yongjae Kim
- Sungjoon Choi
topics:
- dexterous-manipulation
- grasp-taxonomy
- vision-language-planning
- reinforcement-learning
- sim-to-real
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# Learning Dexterous Grasping from Sparse Taxonomy Guidance

## Summary
## 摘要
GRIT 从稀疏的高层抓取分类标签学习灵巧抓取，而不是依赖密集的位姿示范。它把问题拆成抓取类型选择和低层手指控制，目标是提升泛化能力和用户可控性。

## 问题
- 灵巧抓取既需要合适的抓取计划，也需要协调多指执行，但为每个物体-任务对标注密集的抓取位姿或接触标签成本很高。
- 只靠任务奖励进行端到端强化学习可以学会抓取，但在失败时，机器人会采用哪种抓取策略，用户几乎无法控制。
- 这篇论文面向新物体抓取，同时保留一个可由人调整的高层接口，通过抓取分类来实现。

## 方法
- GRIT 是一个两阶段系统：先选择抓取构型，再用受分类条件约束的控制策略执行。
- 抓取构型由离散的人类启发式分类和目标腕部朝向组成。分类库包含基于 Feix 等人的 30 种抓取类型。
- 推理时，视觉语言模型使用场景图像和任务文本来选择分类。为了帮助空间推理，方法把候选腕部方向叠加到图像上。
- 低层策略接收所选分类、腕部目标、本体感觉信息，以及部分点云、手-物体距离、桌面距离和 Basis Point Set 特征等物体几何特征。
- 控制器用强化学习训练，使用一个乘性奖励，结合接近质量、物体交互、分类一致性、物体稳定性，以及对非预期接触的惩罚。教师-学生蒸馏阶段把策略迁移到一个学生模型，后者使用部分观测和一个 LSTM 接触重建器用于实际部署。

## 结果
- 论文报告 GRIT 的总体成功率为 **87.9%**。
- 训练使用 **30 个 YCB 物体**，在过滤后对新物体的评估使用 **373 个 Objaverse/RoboCasa 物体**，并分为 **135 个 fruit_vegetable**、**82 个 household_utensil_tool** 和 **156 个 packed_goods/drink/bread_food** 实例。
- 通用 GRIT 策略在训练中采样的 **30 种分类** 上训练。
- 评估协议为每个物体采样 **8 个腕部方向**，并在每个方向上运行 **30 次试验**。
- 论文声称 GRIT 在新物体上的泛化优于 **RDG** 和 **GraspXL**，但摘要中没有给出逐个基线的数值对比表。
- 真实世界实验声称系统具有可控性：用户可以根据物体几何和任务意图，通过选择分类来调整抓取策略，但摘要没有提供真实世界成功率。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04138v1](http://arxiv.org/abs/2604.04138v1)
