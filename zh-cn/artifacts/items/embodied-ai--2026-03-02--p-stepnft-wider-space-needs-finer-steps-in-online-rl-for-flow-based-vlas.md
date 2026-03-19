---
source: arxiv
url: http://arxiv.org/abs/2603.02083v2
published_at: '2026-03-02T17:04:49'
authors:
- Siting Wang
- Xiaofeng Wang
- Zheng Zhu
- Minnan Pei
- Xinyu Cui
- Cheng Deng
- Jian Zhao
- Guan Huang
- Haifeng Zhang
- Jun Wang
topics:
- vision-language-action
- online-rl
- flow-matching
- embodied-control
- ood-generalization
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# $π$-StepNFT: Wider Space Needs Finer Steps in Online RL for Flow-based VLAs

## Summary
本文提出 **π-StepNFT**，一种面向流式 vision-language-action 模型的在线强化学习方法，用逐步、无 critic、无显式似然的方式来微调机器人策略。核心观点是：**探索空间更宽时，监督必须更细**，因此要用带噪 SDE 扩大探索，再用逐步排序信号稳定对齐。

## Problem
- 流式 VLA 在机器人控制上很强，但其多步采样下的动作似然难以精确计算，导致标准 PPO/策略梯度类在线 RL 很难直接用。
- 纯 ODE 采样探索太窄，策略容易困在专家轨迹附近；一旦测试时偏离，恢复能力差，这对真实操作很重要，因为微小误差会累积成失败。
- 直接把更随机的 SDE 探索搬进来又会带来监督失配：如果只在最终输出上做粗粒度纠正，噪声累积会让训练不稳定、对齐变差。

## Approach
- 用 **SDE 采样** 代替纯 ODE 进行训练时动作生成，向去噪过程注入结构化噪声，主动扩大策略可探索的行为空间。
- 把监督目标从最终去噪结果 **x0** 改为**相邻一步转移** `x_t -> x_t-`，也就是逐步监督下一小步，而不是只看终点；这样更局部、方差更低。
- 不训练额外 value/critic 网络，也不计算显式动作 likelihood；只利用 SDE 单步转移的高斯形式，对观测到的下一步状态做误差比较。
- 构造围绕旧策略的两个镜像分支（正/负扰动），再用 **logistic contrastive ranking loss**：成功轨迹推动“正分支比负分支更能解释该转移”，失败轨迹则反过来，实现 push-pull 更新。
- 每个优化步只需**单次前向传播**，并通过 trust-region 式镜像扰动与 EMA rollout policy 保持更新稳定。

## Results
- 在 **LIBERO** 上，论文声称 **π-StepNFT 相比 SFT 提升 32.9%**，并强调其能释放 few-shot 设置下流式 VLA 的潜力。
- 在 **ManiSkill** 的视觉多样化 **OOD** 场景中，方法相对 critic/value-based baseline **提升 11.1%**，论文将其归因于避免了 critic 对多模态特征的过拟合。
- 论文还声称该方法在 **few-shot robustness** 上具有竞争力，但给定摘录中未提供更细的任务级数值、数据集拆分或与每个具体基线的完整表格。
- 方法层面的强结论包括：**无需辅助 value 网络**、**无需显式 likelihood**、且**每次优化仅需一次前向传播**，目标是更可扩展地服务复杂真实机器人应用。

## Link
- [http://arxiv.org/abs/2603.02083v2](http://arxiv.org/abs/2603.02083v2)
