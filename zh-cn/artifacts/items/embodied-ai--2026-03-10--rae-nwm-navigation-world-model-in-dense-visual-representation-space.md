---
source: arxiv
url: http://arxiv.org/abs/2603.09241v1
published_at: '2026-03-10T06:16:23'
authors:
- Mingkun Zhang
- Wangtian Shen
- Fan Zhang
- Haijian Qin
- Zihao Pei
- Ziyang Meng
topics:
- world-model
- visual-navigation
- dinov2
- diffusion-transformer
- representation-learning
relevance_score: 0.83
run_id: materialize-outputs
language_code: zh-CN
---

# RAE-NWM: Navigation World Model in Dense Visual Representation Space

## Summary
RAE-NWM提出在**稠密视觉表征空间**而不是VAE压缩潜空间中学习导航世界模型，以减少长时预测中的结构崩塌和动作偏差。核心思想是利用DINOv2特征更易于线性刻画动作条件动态，并用扩散Transformer在该空间中生成未来状态。

## Problem
- 现有导航世界模型多在VAE压缩潜空间中预测未来观测，但压缩会丢失细粒度几何结构，导致长时滚动预测出现结构退化与运动学偏移。
- 这会直接削弱下游规划与导航，因为世界模型不仅要“生成像真的图像”，还要保持空间稳定性和动作可控性。
- 作者要解决的问题是：如何选择更适合动作条件动态建模的视觉状态空间，并在其中稳定地做长时导航预测。

## Approach
- 先做一个**线性动态探针**：冻结不同视觉编码器，只训练线性模型预测动作条件下的未来状态；结果显示稠密DINOv2特征比VAE、MAE、SigLIP、ResNet50等更具线性可预测性。
- 基于此，提出**RAE-NWM**：用冻结的DINOv2提取未压缩patch tokens，用冻结的RAE解码器仅在需要可视化/像素评估时重建图像。
- 在表示空间中训练**Conditional Diffusion Transformer with Decoupled Head (CDiT-DH)**，直接对连续视觉状态转移做流匹配建模，而不是离散token自回归预测。
- 引入**time-driven gating**动态条件模块：根据扩散/流时间调节动作与预测步长条件的注入强度，早期更强调运动学先验，后期更放松以保留细节与减少伪影。
- 下游规划直接在表示空间上进行，避免像素解码带来的几何失真与信息损失。

## Results
- 在SACSoN数据集的**直接长时预测**中，RAE-NWM相对NWM显著更优：LPIPS从**0.407/0.470**降到**0.303/0.349**（4s/16s），DreamSim从**0.229/0.281**降到**0.145/0.171**，DINO Distance从**0.402/0.460**降到**0.327/0.367**，FID从**26.15/33.06**降到**15.09/15.90**。
- 论文声称在**16秒顺序滚动预测**中，RAE-NWM保持更强时间稳定性和结构一致性；图示显示基线NWM在后期发生明显结构崩塌，而RAE-NWM仍保持几何完整性。
- 在**轨迹预测/规划相关评估**上，RAE-NWM在SACSoN与SCAND上优于NWM：SACSoN的ATE/RPE从**4.12/0.96**改善到**2.91/0.70**，SCAND从**1.28/0.33**改善到**1.14/0.28**。
- 在RECON上，RAE-NWM结果为**ATE 1.36, RPE 0.37**，相比NWM的**1.13, 0.35**略差，说明改进并非在所有数据集上都全面领先。
- 线性探针的定量数值在摘录中未给出，但作者明确声称DINOv2未压缩token空间在全预测时域内表现出更高的全局$R^2$，且空间打乱后性能明显下降，支持“空间结构本身有助于动作条件动态建模”的论点。

## Link
- [http://arxiv.org/abs/2603.09241v1](http://arxiv.org/abs/2603.09241v1)
