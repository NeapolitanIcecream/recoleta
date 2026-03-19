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
- llm-training
- trajectory-learning
- reinforcement-learning
- bug-fixing
- swe-bench
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-Fuse: Empowering Software Agents via Issue-free Trajectory Learning and Entropy-aware RLVR Training

## Summary
SWE-Fuse 是一个面向软件修复智能体的训练框架，核心目标是在问题描述不可靠甚至缺失时，仍让模型学会逐步调试并稳定优化。它把“有问题描述”和“无问题描述”的轨迹混合训练，再配合基于熵的 RLVR 更新策略，在 SWE-bench Verified 上取得了强结果。

## Problem
- 论文要解决的是：真实软件工程数据里的 issue 描述经常与实际修复补丁不对齐，甚至为空，导致基于 issue 的软件智能体被错误引导。
- 这很重要，因为 SWE agent 需要依赖 issue 文本理解 bug，但现实数据噪声大、可扩展的高质量 issue-PR 配对又稀缺，会直接限制修复成功率与训练规模。
- 文中举例说明 issue 说的是 warning 处理问题，但 gold patch 实际修 TIFF 编码逻辑；此外 SWE-smith 中有 18,033/59,136（30.49%）样本问题描述为空。

## Approach
- 核心方法很简单：不要只教模型“看 issue 修 bug”，还要教它“即使没有 issue，也能靠测试失败和逐步调试找到问题”。因此作者把 issue-guided 样本和 issue-free 样本融合训练。
- 第一部分是 issue-free-driven trajectory learning：先在可执行仓库沙箱里生成多步 reasoning+action 调试轨迹，再做规则过滤和防 git 泄漏过滤，最后用混合轨迹做 SFT，让模型学会一步步查代码、跑命令、看报错、改补丁。
- issue-free 样本会移除 issue 描述，只保留其他上下文和部分测试，用“成功轨迹”训练模型，从而减少错误 issue 文本带来的干扰。
- 第二部分是 entropy-aware RLVR：在强化学习时，不同样本根据策略熵动态调整 clipping 范围。高熵且优势为正时放宽裁剪以鼓励探索；高熵但优势非正时收紧裁剪，避免因噪声错误惩罚潜在有用行为。
- 训练上还采用 RLOO 风格的相对优势估计，并只依赖基础 bash 工具调用的沙箱环境，降低系统复杂度。

## Results
- 在 SWE-bench Verified 上，SWE-Fuse-Qwen3-8B 的 issue resolve rate 达到 **43.0%**，SWE-Fuse-Qwen3-32B 达到 **60.2%**。
- 论文声称其分别优于最佳 **8B** 和 **32B** 基线：solve rate 相对提升 **43.0%** 和 **60.2%**；文中另称在开放模型比较里，相对改进为 **9.1%（8B）** 和 **11.7%（32B）**。
- 加入 test-time scaling 后，在 **TTS@8** 下，8B 和 32B 模型分别达到 **49.8%** 与 **65.2%** solve rate。
- 作者称 32B 开源模型在排行榜上位列同规模第一，并且 **比 OpenAI-o3 高 1.8%** resolved rate，但仍低于 Claude-4-Sonnet 和 Claude-4.5-Sonnet。
- 训练数据方面，作者构建了 **14,350** 条有效轨迹、覆盖 **14,329** 个实例和 **111** 个项目；总交互轮数 **401,958**，平均 **28.05** 轮，平均 token 消耗 **19,676.08**。
- 论文的最强主张是：通过“无 issue 轨迹学习 + 熵感知 RLVR”，即使只用较简单的 bash 工具链，也能让 8B/32B 软件智能体在真实仓库修复任务上达到新的开源 SOTA。

## Link
- [http://arxiv.org/abs/2603.07927v1](http://arxiv.org/abs/2603.07927v1)
