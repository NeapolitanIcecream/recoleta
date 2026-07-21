---
source: arxiv
url: https://arxiv.org/abs/2607.18161v1
published_at: '2026-07-20T17:06:19'
authors:
- Alex Mathai
- Shobini Iyer
- Aleksandr Nogikh
- Petros Maniatis
- Franjo Ivancic
- Junfeng Yang
- Baishakhi Ray
topics:
- code-intelligence
- automated-software-production
- coding-agents
- code-quality
- program-repair
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# TRIM: Reducing AI-Generated CodeSlop via Agent Trajectory Minimization

## Summary
## 摘要
TRIM 利用智能体的修复轨迹来引导保持行为不变的最小化，从而减少 AI 生成的修复补丁中的不必要编辑。在四种智能体框架和两个基准测试中，它减少了 17.8%–32.9% 的 CodeSlop，正确性几乎没有回归，验证成本约为 Delta Debugging 的一半。

## 问题
- 编码智能体经常在通过测试的补丁中留下推测性、已放弃和临时性的编辑，导致补丁规模扩大，并增加审查和维护成本。
- 论文将这种残留且可移除的功能冗余定义为 CodeSlop，并以此为目标，因为仅通过测试并不能找出最小的正确修复。

## 方法
- TRIM（Trajectory-guided Redundancy Identification and Minimization）重建智能体的修复轨迹，保留最终存活的编辑和与任务相关的反馈请求。
- 它执行分层反事实搜索：首先测试移除编辑序列，然后测试移除文件，最后测试移除单个编辑。
- 只有当执行测试仍然通过且补丁规模变小时，系统才接受候选移除操作；同时利用轨迹顺序近似依赖关系，以缩小搜索空间。

## 结果
- 使用 CrashFixer、SWE Agent、MiniSWE Agent 和 OpenHands，在 Live-kBench 和 SWE-Bench 上进行评估。
- 在报告的各项设置中，CodeSlop 减少了 17.8%–32.9%；摘要报告的范围为 17.9%–32.9%。
- 相比基于智能体的最小化基线，性能提升了 1.6×–3.1×，且正确性几乎没有回归。
- 所需验证成本约为 Delta Debugging 等算法基线的一半。
- 在某些情况下，最小化后的补丁与开发者编写的补丁完全一致；其中一个示例将 SWE-Bench 中包含三个文件、五个代码块的补丁缩减为人工修复中的单行代码。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.18161v1](https://arxiv.org/abs/2607.18161v1)
