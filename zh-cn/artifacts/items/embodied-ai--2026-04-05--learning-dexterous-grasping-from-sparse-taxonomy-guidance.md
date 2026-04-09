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
GRIT 用稀疏的高层抓握分类标签学习灵巧抓握，而不是依赖稠密的位姿示范。它把问题拆成抓握类型选择和底层手指控制两个阶段，目标是提升泛化能力和用户控制性。

## 问题
- 灵巧抓握既需要合适的抓握规划，也需要协调的多指执行，但为每个物体-任务组合标注稠密抓握位姿或接触标签，成本很高。
- 只根据任务奖励进行端到端强化学习也能学会抓握，但当机器人失败时，这种方法几乎无法控制它采用哪种抓握策略。
- 论文关注在新物体上的抓握，同时通过抓握分类保留一个可由人调整的高层接口。

## 方法
- GRIT 是一个两阶段系统：先选择抓握配置，再用受分类条件约束的控制策略执行。
- 抓握配置由离散的人类启发式分类和目标手腕朝向组成。分类库包含 30 种抓握类型，基于 Feix et al.
- 在推理时，视觉语言模型根据场景图像和任务文本选择分类。为帮助空间推理，该方法会在图像上叠加候选手腕方向。
- 底层策略的输入包括选定的分类、手腕目标、本体感觉，以及物体几何特征，如局部点云、手物距离、桌面距离和 Basis Point Set 特征。
- 控制器通过强化学习训练，使用乘法奖励，结合接近质量、物体交互、分类遵循度、物体稳定性，以及对非预期接触的惩罚。随后通过教师-学生蒸馏，将策略迁移到一个使用部分观测和 LSTM 接触重建器的学生模型，以便真实部署。

## 结果
- 论文报告 GRIT 的总体成功率为 **87.9%**。
- 训练使用 **30 个 YCB 物体**，对新物体的评估在过滤后的 **373 个 Objaverse/RoboCasa 物体** 上进行，分为 **135 个 fruit_vegetable**、**82 个 household_utensil_tool** 和 **156 个 packed_goods/drink/bread_food** 实例。
- 通用 GRIT 策略在训练时对 **30 种分类** 进行采样。
- 评估流程围绕每个物体采样 **8 个手腕方向**，并对每个方向运行 **30 次试验**。
- 论文称，GRIT 在新物体上的泛化优于 **RDG** 和 **GraspXL**，但摘录中没有给出各基线的具体数值对比表。
- 真实世界实验称该方法具有可控性：用户可以根据物体几何形状和任务意图，通过选择分类来调整抓握策略，但摘录中没有提供真实世界成功率数字。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04138v1](http://arxiv.org/abs/2604.04138v1)
