---
source: arxiv
url: http://arxiv.org/abs/2603.10448v1
published_at: '2026-03-11T06:03:53'
authors:
- Teli Ma
- Jia Zheng
- Zifan Wang
- Chuili Jiang
- Andy Cui
- Junwei Liang
- Shuo Yang
topics:
- robot-control
- video-diffusion
- vision-language-action
- flow-matching
- embodied-ai
relevance_score: 0.62
run_id: materialize-outputs
---

# DiT4DiT: Jointly Modeling Video Dynamics and Actions for Generalizable Robot Control

## Summary
本文提出 DiT4DiT，把视频生成模型与动作生成模型端到端联合训练，用视频扩散过程中的中间特征来指导机器人控制。核心主张是：视频生成可作为比静态视觉语义更强的机器人策略学习“缩放代理”，从而带来更好的泛化、样本效率和控制性能。

## Problem
- 现有 VLA 机器人模型多继承自静态图文预训练，缺少对**时序变化与物理动力学**的先验，导致控制能力主要依赖昂贵的动作标注数据来补足。
- 以往把视频模型用于机器人，常是**多阶段**流程，如先生成视频或提取特征，再单独训练动作模型，控制链路间接且优化不一致。
- 这个问题重要，因为机器人泛化控制需要同时理解“未来会怎么动”和“我该怎么做”，而仅靠静态语义往往难以高效学习复杂操控。

## Approach
- 提出一个统一的 **dual-DiT** 架构：一个 Video Diffusion Transformer 预测未来视频动态，一个 Action Diffusion Transformer 预测动作轨迹。
- 关键机制不是使用重建出的未来帧本身，而是从**视频去噪过程的中间隐藏状态**中提取特征，把这些特征当作对动作模型的时序条件；可简单理解为：让动作模型“偷看”视频模型脑中对未来动态的内部表征，而不是只看最终画面。
- 采用 **dual flow-matching** 联合目标，同时训练视频生成与动作生成，避免传统分阶段训练造成的错配。
- 设计 **tri-timestep** 解耦方案：视频模块用均匀采样时间步学习完整去噪轨迹；特征提取用固定时间步保证条件稳定；动作模块用 Beta 分布采样时间步，把训练重点放在更关键的控制阶段。
- 初始化上，视频骨干来自 Cosmos-Predict2.5-2B，动作头改自 GR00T-N1，并冻结文本编码器与 VAE，只联合微调两个 DiT 模块。

## Results
- 在 **LIBERO** 仿真基准上达到 **98.6%** 平均成功率，论文称为新的 **state-of-the-art**；文中并明确指出其优于近期强 VLA 模型，如 **π0.5** 和 **CogVLA**。
- 在 **RoboCasa GR1** 的 24 个桌面任务上达到 **50.8%** 平均成功率，同样声称为 **SOTA**；并称相对 **GR00T** 系列等强预训练策略取得“substantial margins”的明显领先，但摘录中未给出逐项对比数值。
- 作为训练代理任务，视频生成相比 grounding 和 FLARE-style latent modeling，**样本效率提升超过 10×**，**收敛速度最高提升 7×**；这些结论来自 RoboCasa-GR1 24 任务实验。
- 论文强调其在**更少训练数据**下仍达到上述性能，表明视频生成目标可作为可扩展的策略学习信号，但摘录中未给出精确数据量配置。
- 在真实 **Unitree G1** 机器人上，作者声称优于预训练基线 **GR00T-N1.5** 和参数量匹配基线，并具备强**零样本泛化**，可适应未见物体、类别变化和数量变化；但摘录中未提供真实机的具体成功率数字。

## Link
- [http://arxiv.org/abs/2603.10448v1](http://arxiv.org/abs/2603.10448v1)
