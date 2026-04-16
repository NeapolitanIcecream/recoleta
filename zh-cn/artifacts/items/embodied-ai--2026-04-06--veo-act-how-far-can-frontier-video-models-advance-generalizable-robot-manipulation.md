---
source: arxiv
url: http://arxiv.org/abs/2604.04502v1
published_at: '2026-04-06T07:57:52'
authors:
- Zhongru Zhang
- Chenghan Yang
- Qingzhou Lu
- Yanjiang Guo
- Jianke Zhang
- Yucheng Hu
- Jianyu Chen
topics:
- vision-language-action
- video-models
- dexterous-manipulation
- hierarchical-control
- sim2real
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# Veo-Act: How Far Can Frontier Video Models Advance Generalizable Robot Manipulation?

## Summary
## 摘要
Veo-Act 测试了前沿视频生成模型 Veo-3 是否能在没有任务示范数据的情况下提升机器人操作能力。论文发现，仅靠视频预测可以给出较好的高层规划，但底层控制较弱；将视频规划器与 VLA 组成分层系统后，在灵巧抓取放置任务上的成功率明显提高。

## 问题
- 论文研究开放场景中的可泛化机器人操作；当前的 vision-language-action 策略在物体歧义、视角变化和高接触的灵巧控制上仍然经常失败。
- 纯视频到动作的流水线可以保留大视频模型的泛化能力，但动作恢复精度不足，难以稳定完成高接触操作。
- 这一点很重要，因为采集专家机器人数据成本很高；如果系统能在几乎不需要示范数据的情况下利用网络规模的视频先验，就有机会以更低的数据成本提升机器人的泛化能力。

## 方法
- 作者先测试了一个零样本流水线：Veo-3 根据当前图像和语言指令生成未来视频，逆动力学模型（IDM）再把帧间变化转换成机器人动作。
- IDM 用随机游玩数据训练，而不是专家示范。它使用 DINOv3 视觉编码器和两个 head：一个预测动作，另一个预测门控值，用来判断机器人是否处于交互阶段。
- Veo-Act 把生成的视频作为高层运动规划，将其转换为动作块，对动作块做平滑处理，并持续执行，直到门控检测器判断机器人应切换到响应式的底层 VLA 策略。
- 在执行过程中，系统也可以在交互阶段结束后，从 VLA 策略切回剩余的规划动作序列，并剪去与门控交互窗口重叠的那部分计划。
- IDM 的训练数据包括 30 万个仿真帧对、10 万个额外的随机运动仿真样本，以及 15 万个真实世界样本，并使用 STEM-OB 增强来缩小 sim-to-real 差距。

## 结果
- 主要结果：论文报告称，在其测试的仿真和真实灵巧手环境中，Veo-Act 将强基线 VLA 策略 \(\pi_{0.5}\) 的平均成功率从 **45% 提高到 80%**。
- 在仿真中，**wrist-camera invisible** 实验设置下，总体任务成功率从 \(\pi_{0.5}\) 的 **10/30 = 0.33** 提高到 Veo-Act 的 **20/30 = 0.67**。指令遵循率从 **11/30 = 0.37** 提高到 **25/30 = 0.83**。
- 在仿真中，在 **similar-object distractors** 条件下，总体成功率从 **12/30 = 0.40** 提高到 **28/30 = 0.93**。在 **pass-by interaction** 条件下，总体成功率从 **0/30 = 0.00** 提高到 **14/30 = 0.47**。
- 在真实机器人测试中，在 **similar-object distractors** 条件下，总体成功率从 **8/16 = 0.50** 提高到 **12/16 = 0.75**。在 **pass-by interaction** 条件下，从 **2/13 = 0.15** 提高到 **11/13 = 0.85**。
- 在带有 **richer semantics** 的真实机器人测试中，总体成功率从 **2/19 = 0.11** 提高到 **15/19 = 0.79**，指令遵循率从 **4/19 = 0.21** 提高到 **18/19 = 0.95**。
- 零样本 Veo-3+IDM 基线表现出部分能力，但控制较弱：在仿真中，视频基线 VPP 在 wrist-camera-invisible 实验设置下总体达到 **15/30 = 0.50**，在 similar-object distractors 条件下为 **6/30 = 0.20**，在 pass-by interaction 条件下为 **1/30 = 0.03**。这支持了论文的结论：当前视频模型能够生成大致正确的任务轨迹，但缺少精确的底层控制。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04502v1](http://arxiv.org/abs/2604.04502v1)
