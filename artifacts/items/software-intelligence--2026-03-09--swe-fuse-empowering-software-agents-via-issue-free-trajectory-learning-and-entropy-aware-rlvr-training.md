---
source: arxiv
url: http://arxiv.org/abs/2603.07927v1
published_at: '2026-03-09T03:47:10'
authors:
- Xin-Cheng Wen
- Binbin Chen
- Haoxuan Lan
- Hang Yu
- Peng Di
- Cuiyun Gao
topics:
- software-agents
- swe-bench
- trajectory-learning
- reinforcement-learning
- code-repair
relevance_score: 0.96
run_id: materialize-outputs
---

# SWE-Fuse: Empowering Software Agents via Issue-free Trajectory Learning and Entropy-aware RLVR Training

## Summary
SWE-Fuse 是一个面向软件修复代理的训练框架，核心目标是在真实软件问题中减少低质量 issue 描述带来的误导。它通过把“有 issue 描述”和“无 issue 描述”的轨迹数据结合起来，并配合熵感知的 RLVR 训练，提升了 SWE-bench Verified 上的解题率。

## Problem
- 论文解决的是：真实世界软件修复数据里，**issue 描述与真实补丁常常不匹配**，这会把自动化软件代理带偏，导致调试和补丁生成失败。
- 这很重要，因为当前 SWE 代理高度依赖 issue 文本作为任务入口；一旦描述含噪、缺失或误导，代理即使有很强代码能力，也可能在错误方向上搜索。
- 数据规模和质量也受限，例如文中提到 SWE-smith 中有 **18,033 / 59,136（30.49%）** 的样本问题描述为空，说明仅依赖高质量 issue-supervision 难以扩展。

## Approach
- 核心思路很简单：**不要只教模型“看 issue 修 bug”，还要教它“即使没有靠谱 issue，也能靠测试和调试自己找问题”**。
- 为此，作者构建了一个混合训练框架，把两类样本融合：一类有 issue 描述，另一类是 **issue-free** 样本，只保留测试与环境，让模型通过多轮调试学习定位问题。
- 在监督学习阶段，作者先用教师代理生成多步 ReAct 轨迹（显式包含 reasoning 与 bash action），再做过滤，去掉格式差、无中间推理、可能利用 git 元数据作弊的轨迹，最终得到 **14k** 级高质量轨迹数据。
- 在强化学习阶段，作者提出 **entropy-aware RLVR**：如果模型当前不确定性高且样本优势为正，就放宽 clipping 让它多探索；如果优势非正且不确定性高，就更保守，避免因为噪声过度惩罚潜在有用探索。
- 训练和执行环境保持较简单，主要依赖基本 bash 工具调用和 sandbox 执行，而不是更复杂的专用工具链。

## Results
- 在 **SWE-bench Verified** 上，作者报告 SWE-Fuse-Qwen3-8B 的解决率达到 **43.0%**，SWE-Fuse-Qwen3-32B 达到 **60.2%**。
- 相比最优基线，论文声称 SWE-Fuse 分别在 **8B** 和 **32B** 档上实现 **43.0%** 和 **60.2%** 的 solve rate，并在正文中进一步描述为相对提升 **9.1%**（8B）和 **11.7%**（32B）。
- 加入测试时扩展 **TTS@8** 后，8B 和 32B 模型的 solve rate 进一步提升到 **49.8%** 和 **65.2%**。
- 论文称 32B 开源模型结果达到当时同尺寸开源模型的最佳水平，并且 **比 OpenAI-o3 高 1.8%** 的 resolved rate，但仍低于 Claude-4-Sonnet 与 Claude-4.5-Sonnet。
- 作者还发布了一个轨迹数据集：**14,350** 条有效轨迹、覆盖 **14,329** 个实例和 **111** 个项目；总交互轮数 **401,958**，平均 **28.05** 轮，平均 token 消耗 **19,676.08**。

## Link
- [http://arxiv.org/abs/2603.07927v1](http://arxiv.org/abs/2603.07927v1)
