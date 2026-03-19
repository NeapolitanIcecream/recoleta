---
source: arxiv
url: http://arxiv.org/abs/2603.03768v1
published_at: '2026-03-04T06:24:55'
authors:
- Hao Zhang
- Ding Zhao
- H. Eric Tseng
topics:
- human-robot-collaboration
- multi-agent-rl
- vision-language-models
- whole-body-control
- collaborative-transport
relevance_score: 0.22
run_id: materialize-outputs
language_code: zh-CN
---

# Cognition to Control - Multi-Agent Learning for Human-Humanoid Collaborative Transport

## Summary
本文提出 C2C（cognition-to-control）分层框架，把视觉语言推理、多智能体策略学习和全身控制串起来，用于人与人形机器人协同搬运。其目标是在长时程任务规划与高频接触稳定控制之间建立清晰通路，并在不显式指定主从角色的情况下实现稳定协作。

## Problem
- 现有人机协作搬运系统常依赖脚本、主从角色设定或意图预测，在人类策略变化时容易脆弱、振荡甚至失败。
- 端到端 VLA/VLM 方法更偏“反应式”行为，难以把高层语义规划稳定地落到接触丰富、约束严格的连续全身控制上。
- 这个问题重要，因为协同搬运同时要求**长时程认知决策**与**毫秒级物理稳定性**；做不好会直接影响效率、安全和真实场景部署能力。

## Approach
- 提出三层层级结构：**VLM 认知层**负责从多视角观测中生成共享锚点/路径；**MARL 技能层**负责围绕这些锚点做战术协同；**WBC 控制层**以高频执行并保证运动学/动力学可行与接触稳定。
- 将人机协同搬运建模为**task-centric Markov potential game**：所有体共享与任务进展一致的潜在函数/团队奖励，从而让协调朝共同目标收敛，减少多智能体振荡。
- 技能层采用**残差策略**：策略不是直接输出全部动作，而是在名义运输控制器之上输出小的修正量，学习如何适应伙伴动态与接触细节。
- 训练采用 **CTDE**（集中训练、分散执行）和联合动作 critic；执行时各体保留独立策略、无需参数共享，也无需显式主从角色或单独意图推断模块。

## Results
- 在 **9 个场景**（OSP/SCT/SLH 三类，每类 3 个子任务）上，MARL 方法整体明显优于 robot-script 基线；文中“overall architecture synergy index”（平均成功率）从 **56.5%** 提升到 **80.6% / 83.0% / 83.2%**（HAPPO/HATRPO/PCGrad），相对增益最高 **+45.6%**。
- 分场景结果显示，对比 robot-script，成功率从约 **49.6%–65.4%** 提升到约 **72.7%–88.6%**。例如：**S21 Narrow gate** 从 **59.2 ± 9.0** 提升到 **88.6 ± 3.5**（PCGrad）；**S31 Facing mode** 从 **52.8 ± 8.1** 提升到 **84.4 ± 1.6**（HATRPO）；**S11 Alignment** 从 **65.4 ± 7.2** 提升到 **87.9 ± 4.5**（HATRPO）。
- 各任务相对脚本基线的结构增益分别达到 **+29.3% 到 +55.9%**，如 **S31 +55.9%**、**S33 +55.2%**、**S32 +50.1%**，表明在长物体处理和受限空间协作中提升更明显。
- 消融实验中，仅保留部分层级会失败：**No cognition = Fails，No skill = Fails**；完整层级达到 **78.6%** 成功率，平均完成时间 **81.2 s**，说明认知层与技能层缺一不可。
- 训练设置包含 **2.0×10^9** steps，策略输入维度 **210**，动作维度 **11**，策略频率 **2 Hz**；这些是具体实现规模而非性能指标。
- 论文还宣称真实机器人（Unitree G1 + 人类）实验中，相比单智能体基线具有更高成功率、更好鲁棒性，并出现**涌现的 leader-follower 行为**；但给定摘录未提供图 4(c) 的完整数值。

## Link
- [http://arxiv.org/abs/2603.03768v1](http://arxiv.org/abs/2603.03768v1)
