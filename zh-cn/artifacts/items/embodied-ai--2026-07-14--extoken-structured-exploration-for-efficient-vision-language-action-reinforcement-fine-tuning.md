---
source: arxiv
url: https://arxiv.org/abs/2607.12931v1
published_at: '2026-07-14T16:04:41'
authors:
- Yilun Kong
- Yunpeng Qing
- Guozheng Ma
- Haoyu Wang
- Li Shen
- Zhi Hou
- Dacheng Tao
topics:
- vision-language-action
- robot-reinforcement-learning
- structured-exploration
- robot-data-scaling
- sample-efficiency
- dexterous-manipulation
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# ExToken: Structured Exploration for Efficient Vision-Language-Action Reinforcement Fine-tuning

## Summary
## 摘要
ExToken 通过让 rollout 以从离线示范中学习到的多样化行为令牌为条件，提高了视觉-语言-动作强化微调的样本效率。在模拟和真实世界交互预算受限的情况下，与标准 VLA-RL 相比，该方法取得了更高的成功率并实现了更快的收敛。

## 问题
- VLA 强化学习经常浪费成本高昂的环境交互，因为随机探索会退化为重复的动作模式和相似轨迹。
- 这一点很重要，因为实体 rollout 需要时间、硬件访问、人为干预和安全资源；收集更多冗余轨迹并不能可靠地改善学习效果。

## 方法
- ExToken 使用预训练视频编码器对每条示范轨迹进行嵌入，并应用 K-means 聚类；每个聚类中心成为一个表示行为模式的离散令牌。
- 在监督预热和 RL rollout 收集期间，VLA 策略接收一个令牌；采样不同令牌会将策略引向不同的动作模式，并扩大状态-动作覆盖范围。
- 一个基于 SigLIP、以状态为条件的 Token Selector 根据初始图像和语言指令预测适当的令牌。该选择器使用监督式聚类标签进行训练，并通过 REINFORCE 与策略联合优化。
- 部署期间，选择器以确定性方式选择概率最高的令牌，从而解决随机化训练探索与推理之间的不匹配。

## 结果
- 在四个 LIBERO 套件上，每个优化步骤使用 512 条 rollout、共进行 100 个 RL 步骤时，ExToken 达到 98.2% 的平均成功率，而匹配的 RLinf-GRPO 基线为 96.8%；在 LIBERO-Long 上，ExToken 达到 97.8%，基线为 95.2%。
- 在受控探索研究中，保留 512 条多样化轨迹取得了与 1,024 条标准 rollout 相当的表现，并优于使用 512 条 rollout 的标准训练结果，支持“轨迹多样性是样本效率关键因素”这一结论。
- 在真实世界任务中，每个任务每次迭代仅评估 20 条 rollout；在 Fold clothes、Wipe table with towel、Pour water 和 Insert pen into pen holder 四项任务上，ExToken 的平均原始设置得分比 Evo-RL 提高了 6.25%。
- 在物体、背景和光照发生变化时，ExToken 通常下降 5–10 个百分点，而报告中的基线通常下降 10–25 个百分点。
- 每个优化步骤使用 256 条 rollout 时，ExToken 的成功率为 93.4%，而相同缩减预算下的 RLinf-GRPO 为 90.3%；其表现与使用 512 条 rollout 的 RLinf-GRPO 相当。rollout 数量降至 128 条时，ExToken 的稳定性下降。
- 论文报告称，令牌数量为 K=3 和 K=6 时性能稳定，K=10 时略有下降；该摘录没有提供轨迹空间覆盖范围增加的单一量化指标。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.12931v1](https://arxiv.org/abs/2607.12931v1)
