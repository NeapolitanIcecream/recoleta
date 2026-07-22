---
source: arxiv
url: https://arxiv.org/abs/2607.19343v1
published_at: '2026-07-21T17:59:11'
authors:
- Hadi Alzayer
- Wenlong Huang
- Haonan Chen
- Christopher Luey
- Lvmin Zhang
- Maneesh Agrawala
- Gordon Wetzstein
- Li Fei-Fei
- Yilun Du
- Jiajun Wu
- Jia-Bin Huang
topics:
- robot-world-model
- masked-video-modeling
- pixel-space-actions
- embodiment-generalization
- model-based-planning
- inverse-dynamics
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Masked Visual Actions for Unified World Modeling

## Summary
## 摘要
Masked Visual Actions 将机器人运动表示为部分揭示的像素空间轨迹，使预训练视频模型能够预测场景响应，或根据期望的物体运动推断机器人行为。经过 15 小时真实数据和仿真数据的适配后，单个检查点提升了视觉预测效果，并且相较于稀疏或特定于机器人形态的动作表示，在未见过的机器人形态上具有更好的泛化能力。

## 问题
- 机器人世界模型需要将动作与其视觉后果联系起来，同时还要推断能够实现期望结果的动作。
- 关节指令、末端执行器状态、骨架和轨迹等现有控制表示通常较为稀疏、特定于机器人形态，或与视频模型学习到的视觉表示不够对齐。
- 这一点很重要，因为视觉化且与机器人形态无关的动作接口，可以让同一个模型支持仿真、策略评估、基于模型的规划和逆控制。

## 方法
- 将动作表示为视频中某个实体的掩码像素空间轨迹。模型接收初始场景和已揭示的轨迹，然后补全其余实体及后续帧。
- 揭示机器人运动，以获得预测物体和场景响应的正向模型；揭示期望的物体运动，以获得预测相容机器人运动的逆向模型。
- 使用来自 DROID 和 Robocasa 的掩码样例，对 Wan-Fun-Control 2.2 14B 进行微调，采用 LoRA rank 256，约训练 10,000 步，数据总量约为 15 小时。
- 通过机器人分割或渲染的机器人网格构建条件输入，使不同机器人形态的轨迹能够共享同一个像素空间接口。

## 结果
- 在 DROID 上，Masked Visual Actions 的 LPIPS 为 0.0945、SSIM 为 0.887、PSNR 为 23.74；Ctrl-World 的对应数值分别为 0.362、0.708 和 18.15。
- 在未见过的双臂 BEHAVIOR 机器人形态上，其 LPIPS 为 0.123、SSIM 为 0.843、PSNR 为 22.90；Ctrl-World 的对应数值分别为 0.196、0.837 和 18.39。
- 与稀疏的末端执行器可视化和骨架可视化相比，该方法在 DROID、真实世界数据和 BEHAVIOR 上的表现最佳；在真实世界数据上，其 LPIPS 为 0.148、SSIM 为 0.864、PSNR 为 22.79，而骨架可视化对应的数值为 0.169、0.866 和 21.02。
- 论文报告称，想象 rollout 与真实执行结果在策略评估中具有相关性，能够改进基于模型的规划中的候选选择，并支持逆向建模；但所提供的摘录未包含下游任务成功率数据。
- 该模型使用一个检查点完成正向预测、规划、策略评估和逆向运动合成，并且支持对被动物体轨迹进行零样本条件控制，尽管训练时的掩码主要针对主动机器人实体。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.19343v1](https://arxiv.org/abs/2607.19343v1)
