---
source: arxiv
url: http://arxiv.org/abs/2603.03485v2
published_at: '2026-03-03T20:01:43'
authors:
- Haoran Lu
- Shang Wu
- Jianshu Zhang
- Maojiang Su
- Guo Ye
- Chenwei Xu
- Lie Lu
- Pranav Maneriker
- Fan Du
- Manling Li
- Zhaoran Wang
- Han Liu
topics:
- video-diffusion
- world-model
- physics-consistency
- 4d-modeling
- synthetic-data
- reinforcement-learning
relevance_score: 0.45
run_id: materialize-outputs
---

# Phys4D: Fine-Grained Physics-Consistent 4D Modeling from Video Diffusion

## Summary
Phys4D把预训练视频扩散模型提升为更符合物理规律的4D世界模型，不只生成好看的视频，还显式建模随时间变化的几何与运动。核心贡献是三阶段训练、超大规模物理仿真数据，以及一套超越外观指标的4D物理一致性评测。

## Problem
- 现有视频扩散/世界模型主要拟合外观，常出现**局部几何不一致、运动不稳定、时间上非因果**等细粒度物理错误。
- 训练这种物理一致的4D模型需要**密集、时序对齐的几何和运动监督**，但真实视频很难大规模获得这类标注。
- 仅靠图像级或像素级损失，难以保证**长时程、世界级别**的物理合理性，因此需要新的训练与评测方式。

## Approach
- 采用**RGB-D + 光流/场流**作为2.5D中间表示，让视频扩散模型除了生成RGB，还预测每帧深度和帧间运动，从而显式表示4D世界状态。
- 提出**三阶段训练**：先用伪标签在生成视频与互联网视频上预训练深度/运动头；再用仿真真值做监督微调，并加入**warp一致性损失**，约束“当前深度沿预测运动变换后应匹配下一帧深度”。
- 第三阶段用**仿真支撑的强化学习**进一步修正监督难覆盖的残余物理错误：把生成结果提升为4D点云轨迹，并以与仿真真值的**4D Chamfer Distance**作为奖励，用PPO优化采样策略。
- 构建了大规模物理仿真数据管线：基于Isaac Sim覆盖**9类物理现象**，约**20,000+**独特物理配置，从**200**个基础场景扩展到约**250,000**环境，产生**1,250,000**个视频、总计**20,800小时**、**1080p/60FPS**、**15TB+**多模态标注。
- 提出4D世界一致性评测，既看视频层物理合理性，也看**几何一致性、运动稳定性、长时程物理可行性**。

## Results
- 在**Physics-IQ**上，**CogVideoX + Phys4D**相对原始CogVideoX：**Score 30.2% vs 18.8%**（+11.4个百分点），**MSE 0.009 vs 0.013**，**ST-IoU 0.169 vs 0.116**，**S-IoU 0.252 vs 0.222**，**WS-IoU 0.157 vs 0.142**。
- **WAN2.2 + Phys4D**相对WAN2.2：**Score 25.6% vs 16.8%**（+8.8个百分点），**MSE 0.014 vs 0.016**，**ST-IoU 0.107 vs 0.088**，**S-IoU 0.214 vs 0.150**，**WS-IoU 0.122 vs 0.105**。
- **Open-Sora V1.2 + Phys4D**相对原始Open-Sora：**Score 22.4% vs 14.5%**（+7.9个百分点），**MSE 0.016 vs 0.021**，**ST-IoU 0.098 vs 0.072**，**S-IoU 0.195 vs 0.135**，**WS-IoU 0.112 vs 0.092**。
- 与文中列出的商业模型聚合分数相比，**CogVideoX + Phys4D 30.2%** 高于 **VideoPoet 20.3% / Pika 13.0% / Sora 10.0%**；但商业模型未报告相同细项指标，严格可比性有限。
- 论文还声称在保持强生成能力的同时，显著提升**细粒度时空一致性与物理一致性**；除Physics-IQ表格外，摘录中未给出更多完整数值。

## Link
- [http://arxiv.org/abs/2603.03485v2](http://arxiv.org/abs/2603.03485v2)
