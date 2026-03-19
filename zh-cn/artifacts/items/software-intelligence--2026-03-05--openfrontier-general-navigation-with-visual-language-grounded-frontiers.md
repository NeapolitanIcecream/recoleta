---
source: arxiv
url: http://arxiv.org/abs/2603.05377v1
published_at: '2026-03-05T17:02:22'
authors:
- Esteban Padilla
- Boyang Sun
- Marc Pollefeys
- Hermann Blum
topics:
- robot-navigation
- vision-language-models
- frontier-based-exploration
- zero-shot-learning
- open-world-navigation
relevance_score: 0.36
run_id: materialize-outputs
language_code: zh-CN
---

# OpenFrontier: General Navigation with Visual-Language Grounded Frontiers

## Summary
OpenFrontier提出一种**免训练**的开放世界机器人导航框架，把“前沿点（frontiers）”作为视觉-语言语义与实际导航之间的桥梁。它不依赖稠密3D建图、策略训练或微调，却能在多个导航基准上实现强零样本表现，并完成真实机器人部署。

## Problem
- 现有开放世界导航方法常依赖**稠密3D重建、语义地图或手工目标度量**，系统重、泛化差，在杂乱场景和开放词汇目标下不稳。
- 端到端VLN/VLA方法虽然能用自然语言控制导航，但通常需要**交互式训练、大规模数据采集或任务专用微调**，成本高且难直接落到度量空间中的可执行导航决策。
- 核心难点是：如何把高层视觉-语言语义，可靠地**落地到物理上可到达的导航目标**上，这对开放词汇机器人导航很重要，因为机器人必须在未知环境中既理解语义又高效探索。

## Approach
- 将导航重写为“**找稀疏子目标并依次到达**”的问题：从当前RGB图像中检测视觉前沿点，把它们作为候选导航目标，而不是先构建完整3D语义地图。
- 使用**set-of-marks**提示：在图像中给每个前沿点打标记，再把图像和自然语言目标一起输入VLM，让模型一次性给每个前沿点打出与任务相关的概率分数 \(p_i\)。
- 把VLM语义分数与前沿点自带的探索信息增益 \(\hat g_i\) 相乘，得到最终效用 \(g_i = p_i \cdot \hat g_i\)，即用最简单的方式平衡“哪里值得探索”和“哪里更像目标所在方向”。
- 在全局层面维护一个稀疏前沿集合，按 \(u_i = g_i / \|p_r - p_i\|\) 选择兼顾**语义相关性与到达代价**的前沿点，并交给低层PointNav/规划器执行。
- 当开放词汇分割检测到疑似目标时，系统会生成一个高优先级“视点前沿”靠近目标，再用同一VLM做目标确认，确认后才终止导航。

## Results
- 在**HM3D ObjNav Val**上，OpenFrontier达到**77.3% SR / 35.6% SPL**，优于零样本基线：BeliefMapNav **61.4 / 30.6**、InstructNav **58.0 / 20.9**、OpenFMNav **52.5 / 24.1**、VLFM **52.5 / 30.4**、UniGoal **54.5 / 25.1**；其SR也高于非零样本Uni-NaVid的**73.7%**，但SPL略低于其**37.1%**。
- 在**MP3D ObjNav Val**上，OpenFrontier为**40.7% SR / 17.8% SPL**；与零样本方法相比，优于BeliefMapNav **37.3 / 17.6**、VLFM **36.4 / 17.5**、OpenFMNav **37.2 / 15.7**，与UniGoal **41.0 / 16.4**接近（SR略低0.3点，SPL更高1.4点）。
- 在**OVON Val Unseen**开放词汇导航上，OpenFrontier达到**39.0% SR / 20.1% SPL**，优于零样本VLFM **35.2 / 19.6** 和非零样本DAgRL+OD **37.1 / 19.9**，接近非零样本Uni-NaVid **39.5 / 19.8**（SR低0.5点，但SPL高0.3点）。
- 论文还声称系统在**同一统一配置**下跨三个基准表现稳定，只需**稀疏关键帧推理**（每6步做一次前沿检测与推理），避免了逐步高频动作推断或持续稠密语义建图。
- 真实世界方面，作者展示了在移动机器人上寻找**fire extinguisher**的部署案例，并声称对不同VLM具有可替换性，但节选文本未给出真实机器人实验的量化成功率或路径效率数字。

## Link
- [http://arxiv.org/abs/2603.05377v1](http://arxiv.org/abs/2603.05377v1)
