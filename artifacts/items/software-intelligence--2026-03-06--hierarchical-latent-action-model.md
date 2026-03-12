---
source: arxiv
url: http://arxiv.org/abs/2603.05815v1
published_at: '2026-03-06T01:59:07'
authors:
- Hanjung Kim
- Lerrel Pinto
- Seon Joo Kim
topics:
- latent-action-models
- hierarchical-learning
- skill-discovery
- robot-learning
- imitation-learning
relevance_score: 0.76
run_id: materialize-outputs
---

# Hierarchical Latent Action Model

## Summary
HiLAM旨在从只有视频、没有动作标签的数据中，自动发现持续时间可变的高层技能，而不只是不连续的短时运动。它把已有潜在动作模型提取出的低层潜在动作，再层次化压缩成潜在技能，用于更强的长时程机器人控制预训练。

## Problem
- 现有Latent Action Models通常只建模相邻或短时间帧之间的变化，擅长低层运动，但难以捕捉长时程、可复用的高层技能。
- 真实视频里的技能持续时间不固定；若强行用固定窗口或预定义技能集合，会把本质相同但速度不同的行为编码成不同表示。
- 这很重要，因为动作标注昂贵，而大量无动作标签的人类/机器人视频中其实包含丰富技能结构，若能利用，可提升长时程控制与数据效率。

## Approach
- 先用预训练的逆动力学模型（IDM）从无动作标签视频中提取低层潜在动作序列，把“看视频”转成“看潜在动作token序列”。
- 在其上引入两层H-Net式动态分块：通过相邻token特征不相似度自动判断边界，把可变长度的低层潜在动作段压缩成更短的高层潜在技能表示。
- 训练目标是三部分：下一潜在动作预测损失、用预训练前向动力学模型（FDM）做未来帧重建的视觉约束、以及防止退化分块的ratio regularizer。
- 训练完后，把分块得到的stage-wise表示展开回逐时刻技能序列；再训练分层策略：高层策略预测潜在技能，低层策略在观察+技能条件下预测潜在动作，最后用少量真值动作微调低层策略映射到真实机器人动作。

## Results
- 在LIBERO四个suite（Spatial/Object/Goal/Long）上，论文声称HiLAM始终优于SOTA基线BAKU；图中未给出四个suite逐项精确数值，但定性结论是一致领先。
- 在最难的LIBERO-Long上，只用**10%**专家演示微调时，BAKU成功率为**23%**，HiLAM为**45%**，几乎翻倍。
- 在LIBERO-Long上，用**50%**演示时，HiLAM达到**84%**，与BAKU用**100%**数据时大致相当，表明明显更高的数据效率。
- 在LIBERO-Long上，用**100%**演示时，HiLAM达到**94%**成功率，并显著超过BAKU。
- 消融表明：不做大规模预训练、只训练分层策略时，HiLAM仅**0.67**成功率；而最佳设置（人类视频预训练，latent skill用**stage-2**，latent action用**stage-0**）达到**0.94**。
- 平坦策略的BAKU加潜在条件也有提升，但最好仅到**0.91**（human pretraining, latent action=stage-0），仍低于HiLAM的**0.94**；机器人视频预训练下HiLAM最佳约**0.90**，也优于多数对应BAKU设置。

## Link
- [http://arxiv.org/abs/2603.05815v1](http://arxiv.org/abs/2603.05815v1)
