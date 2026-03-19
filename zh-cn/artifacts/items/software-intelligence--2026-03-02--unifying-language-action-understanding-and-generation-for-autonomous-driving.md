---
source: arxiv
url: http://arxiv.org/abs/2603.01441v1
published_at: '2026-03-02T04:41:10'
authors:
- Xinyang Wang
- Qian Liu
- Wenjie Ding
- Zhao Yang
- Wei Li
- Chang Liu
- Bailin Li
- Kun Zhan
- Xianpeng Lang
- Wei Chen
topics:
- autonomous-driving
- vision-language-action
- instruction-following
- multimodal-alignment
- coarse-to-fine-decoding
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Unifying Language-Action Understanding and Generation for Autonomous Driving

## Summary
LinkVLA提出一种把自然语言指令与驾驶动作统一到同一离散token空间中的自动驾驶VLA框架，以同时提升指令-动作对齐和推理效率。它还加入“由轨迹反推语言”的理解任务，并用两阶段粗到细解码替代逐点自回归生成。

## Problem
- 现有自动驾驶VLA模型常出现**语言理解与实际动作不一致**：例如能说出“向左变道”，却生成“保持车道”的轨迹，这直接影响安全性、可控性和用户信任。
- 典型的**自回归动作生成太慢**，长轨迹需要逐步解码，部署时会带来明显推理延迟。
- 以数据增强、后验RL修正或隐式潜空间对齐为主的方法，往往没有在监督学习阶段建立**可验证的双向语言-动作联系**。

## Approach
- **统一token空间**：把语言token和轨迹token合并到一个共享离散codebook中；连续轨迹先量化为动作token，再由单一多模态模型统一处理，从结构上缩小模态鸿沟。
- **更好的动作token化**：对轨迹坐标做对数变换，提高近车区域精度；再用空间soft label（高斯邻域）训练，而不是硬one-hot，使邻近动作在学习中也被视为“相近”。
- **双向语义对齐**：除了常规的“看图+指令生成动作”外，还加入“看图+动作生成指令描述”的辅助目标，迫使模型学会从轨迹反推语言含义，形成双向一致性。
- **粗到细生成（C2F）**：先一次前向预测轨迹终点，再通过线性插值得到粗轨迹，最后并行细化全部waypoint，替代逐点自回归解码。

## Results
- 在**Bench2Drive闭环评测**上，LinkVLA取得**DS 91.01**、**SR 74.55%**、**Efficiency 255.84**、**Comfort 34.62**。相较最强列出的指令跟随基线**SimLingo**（DS **85.07** / SR **67.27%** / Efficiency **259.23** / Comfort **33.67**），分别提升**+5.94 DS**、**+7.28 SR**、**-3.39 Efficiency**、**+0.95 Comfort**。
- 在**Multi-Ability平均分**上，LinkVLA达到**73.40%**，高于**SimLingo 67.28%**和**Orion 54.72%**。分项上包括：Merging **60.00**、Overtake **80.00**、Brake **93.33**、Give-Way **50.00**、Traffic-Sign **83.68**。
- 在**延迟对比**中，LinkVLA自回归版本为**361ms**，C2F版本降至**48ms**，相当于节省约**86.7%**推理时间；同时驾驶分数从**90.66**提升到**91.01**。
- 与其他方法相比，C2F版LinkVLA延迟**48ms**，快于**Orion 65ms**，接近**SimLingo 34ms**，但驾驶分数更高（LinkVLA **91.01** vs Orion **77.74** vs SimLingo **85.07**）。
- 论文还声称在闭环驾驶性能和指令跟随能力上实现了**state-of-the-art**，核心证据来自Bench2Drive主表与延迟表中的领先分数。

## Link
- [http://arxiv.org/abs/2603.01441v1](http://arxiv.org/abs/2603.01441v1)
