---
source: arxiv
url: http://arxiv.org/abs/2604.01346v2
published_at: '2026-04-01T19:57:33'
authors:
- Manoj Parmar
topics:
- world-models
- ai-safety
- adversarial-robustness
- threat-modeling
- alignment
relevance_score: 0.73
run_id: materialize-outputs
language_code: zh-CN
---

# Safety, Security, and Cognitive Risks in World Models

## Summary
## 摘要
本文综述了世界模型中的安全、安全防护和人类信任风险，并补充了一个威胁模型和概念验证攻击指标。论文的主要观点是，世界模型会产生可在想象 rollout 过程中持续存在的失效模式，因此在安全关键系统中需要更强的评估和控制。

## 问题
- 论文研究了世界模型在机器人、自动驾驶和 agentic AI 中为规划预测未来状态时产生的风险。
- 微小的输入扰动或被污染的模型状态可能会在多个 rollout 步骤中持续传播，导致规划以难以察觉的方式失败。
- 作者还认为，配备世界模型的智能体会带来对齐风险，例如目标错误泛化和奖励劫持，而人类用户也可能过度信任模型预测。

## 方法
- 这篇论文主要是一篇综述和威胁建模论文，不是新的世界模型训练方法。
- 论文用放大比率 $\mathcal{A}_k$ 定义了**轨迹持续性**，用于比较攻击在循环世界模型内部的增长幅度与单步编码器相比有多大。
- 论文将**表征风险** $\mathcal{R}(\theta,\mathcal{D})$ 定义为部署分布上真实环境动力学与学习到的动力学之间的差距，并给出了一些实用代理指标，例如集成分歧和潜在空间 OOD 分数。
- 论文建立了一个五类攻击者分类：白盒、灰盒、黑盒、内部人员和供应链，并将威胁映射到世界模型系统各层以及 MITRE ATLAS 和 OWASP LLM Top 10 等现有安全参考框架中。
- 论文包含了针对 GRU/RSSM 风格模型的概念验证实验，以及对 DreamerV3 的 checkpoint probing，用来测试对抗效应是否会在 rollout 过程中持续存在。

## 结果
- 论文报告了一个针对**基于 GRU 的 RSSM**的**轨迹持续性对抗攻击**，其中 **$\mathcal{A}_1 = 2.26\times$**，表示第 1 步的攻击误差超过单步基线的两倍。
- 在**对抗微调**下，论文报告基于 GRU 的设置中攻击效果降低了 **59.5%**。
- 在一个**随机 RSSM 代理模型**中，论文报告放大率下降到 **$\mathcal{A}_1 = 0.65\times$**，作者据此认为漏洞程度依赖于架构。
- 对于一个**真实的 DreamerV3 checkpoint**，论文通过 checkpoint-level probing 报告了**非零动作漂移**，但摘录中没有给出完整的端到端任务指标、基准分数或失败率数字。
- 论文引用的是既有背景而不是新的任务性能提升，包括 **DreamerV3 在 150+ 个任务上的结果**以及一项先前自动驾驶攻击研究中**最高 67% 的攻击成功率**，但这些是背景参考，不是本文的主要实验结果。
- 作者说明，他们的实证结果是基于代理模型的**概念验证**，而对于已部署大规模系统的判断主要来自理论分析和文献综合，而不是完整系统测量。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.01346v2](http://arxiv.org/abs/2604.01346v2)
