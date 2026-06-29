---
kind: trend
trend_doc_id: 443
granularity: day
period_start: '2026-05-26T00:00:00'
period_end: '2026-05-27T00:00:00'
topics:
- robot learning
- vision-language-action
- continual learning
- sim-to-real
- visual reinforcement learning
- humanoid robots
run_id: materialize-outputs
aliases:
- recoleta-trend-443
tags:
- recoleta/trend
- topic/robot-learning
- topic/vision-language-action
- topic/continual-learning
- topic/sim-to-real
- topic/visual-reinforcement-learning
- topic/humanoid-robots
language_code: zh-CN
---

# 机器人学习论文集中在执行控制、保留和更便宜的真实世界验证

## Overview
这一时期最强的信号是面向真实部署约束的实用机器人学习。视觉-语言-动作（VLA）模型正在接受细粒度执行控制和技能保留的测试，而 HyperSim 和 SDPG 降低了真实数据或 GPU 的训练成本。Figure 的包裹分拣运行增加了一个耐久性主张，但其审计细节不如研究论文充分。

## Clusters

### 可控 VLA 策略
FineVLA 针对机器人数据集中的一个具体弱点：很多轨迹只说明任务完成了什么，却没有说明怎么完成的。该工作为 47,159 条筛选后的轨迹补充了经人工核验的执行指令，覆盖手臂选择、接近方向、接触区域、最终姿态和其他动作细节。用细粒度标签和原始标签混合训练时，报告结果最好，AlohaMix-OFT 在 RoboTwin 上达到 86.8% Easy 和 82.5% Hard。在真实双臂操作中，同一组证据给出的结果是细粒度:原始 = 1:1 时为 62.7/100，而只用原始标签训练为 49.9。

#### Evidence
- [FineVLA: Fine-Grained Instruction Alignment for Steerable Vision-Language-Action Policies](../Inbox/2026-05-26--finevla-fine-grained-instruction-alignment-for-steerable-vision-language-action-policies.md): Summary gives the dataset construction, instruction dimensions, RoboTwin results, and real-world dual-arm scores.

### 真实机器人技能的持续学习
这项持续学习 VLA 研究把遗忘变成了硬件风格任务里可测的现象。直接顺序微调会严重削弱先前技能：Stack Bowl 从 100.0 降到 15.0，Hang Cup 从 97.5 降到 25.0，Press Button 从 100.0 降到 13.3。把回放率和动作归一化设置好后，经验回放会改变结果。缓冲区比例 0.2、回放频率 0.2 时，最终平均分达到 93.5，而顺序微调只有 37.3。动作归一化的结果给出一个明确警告：按任务归一化后平均分掉到 23.7，说明部署细节可能比学习方法更关键。

#### Evidence
- [Can VLA Models Learn from Real-World Data Continually without Forgetting?](../Inbox/2026-05-26--can-vla-models-learn-from-real-world-data-continually-without-forgetting.md): Summary reports the four-task dataset, forgetting numbers, replay settings, and normalization failure.

### 更便宜的训练和仿真到真实迁移
HyperSim 和 SDPG 都在压低视觉机器人策略训练的成本。HyperSim 用重建场景、对抗式合成轨迹和 35 条真实示教做联合训练。在少样本测试里，混合仿真和真实数据用 pi0 达到 95% SR3，高于同样真实示教数量下 70% 的纯真实基线。SDPG 通过用随机扰动估计动作序列梯度，降低了视觉强化学习的渲染和显存开销。它在 Visual MuJoCo 任务上的报告显存大约是 10.2 到 10.5 GB，而 PPO 估计大约是 48 到 50 GB。

#### Evidence
- [HyperSim: A Holistic Sim-To-Real Framework For Robust Robotic Manipulation](../Inbox/2026-05-26--hypersim-a-holistic-sim-to-real-framework-for-robust-robotic-manipulation.md): Summary gives HyperSim's components, few-shot setup, and success rates against real-only baselines.
- [Efficient On-policy Visual-RL via Stochastic Decoupled Policy Gradient](../Inbox/2026-05-26--efficient-on-policy-visual-rl-via-stochastic-decoupled-policy-gradient.md): Summary gives SDPG's training method, memory comparison, and single-GPU claim.

### 人形机器人耐久性主张需要更好的测量
Figure 报告了 Figure 03 人形机器人连续 200 小时的自动包裹分拣运行，共分拣 249,560 个包裹。任务很具体：找到小包裹上的条码，并把它正面朝下放到传送带上。文章还给出了一次更早的 10 小时运行中的人工对比，人工分拣了 12,924 个包裹，机器人分拣了 12,735 个。这个结果可作为耐久性指标，但来源没有提供独立审计、错误率、停机时间拆分，也没有和现有仓储自动化做比较。

#### Evidence
- [Figure's robots sorted packages for 200 hours straight](../Inbox/2026-05-26--figure-s-robots-sorted-packages-for-200-hours-straight.md): Summary gives the 200-hour run, package count, human comparison, and missing audit details.
