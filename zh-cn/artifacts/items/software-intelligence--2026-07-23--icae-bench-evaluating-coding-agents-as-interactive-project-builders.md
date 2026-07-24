---
source: arxiv
url: https://arxiv.org/abs/2607.21217v1
published_at: '2026-07-23T11:31:38'
authors:
- Zhongyuan Peng
- Dan Huang
- Chuyu Zhang
- Caijun Xu
- Changyi Xiao
- Shibo Hong
- David Lo
- Lin Qiu
- Xuezhi Cao
- Jiyuan He
- Yixin Cao
topics:
- code-intelligence
- automated-software-production
- coding-agents
- interactive-benchmark
- repository-generation
- multi-agent-software-engineering
relevance_score: 0.97
run_id: materialize-outputs
language_code: zh-CN
---

# ICAE-Bench: Evaluating Coding Agents as Interactive Project Builders

## Summary
## 总结
ICAE-Bench 评估编码代理能否通过需求澄清、规划、工具使用、调试和实现，将不完整的产品意图转化为可运行的代码仓库。该基准包含覆盖 12 种语言的 480 个任务，实验显示，代理通常能够复现可见行为，但难以处理隐藏约束、边界情况和长周期集成。

## 问题
- 现有编码基准主要使用完整规格说明或现有代码仓库，因此无法衡量代理能否澄清模糊意图并从头构建项目。
- 这一点很重要，因为交互式项目构建要求代理提取需求，在实现过程中保持这些需求，并在代码仓库级约束下交付可运行的软件。

## 方法
- 从经过验证的开源代码仓库中派生每个任务，创建完整的 GroundPRD 和黑盒行为用例，然后隐藏选定的 API、边界情况和架构约束，以生成 Fuzzy L1、L2 和 L3 需求。
- 使用由编写好的 User Agent Data 支持的、基于事实约束的 User Agent 模拟澄清过程，避免需求幻觉、实现细节泄露和不可复现的交互。
- 从预配置的执行镜像中移除原始代码和测试，使代理能够根据模糊需求和恢复的信息构建代码仓库。
- 使用黑盒 Native 和 Enhanced 测试以及多维诊断，对开放式实现进行评分；诊断指标包括功能正确性、语义和 API 相似度、结构保真度、设计质量和交互质量。

## 结果
- ICAE-Bench 包含 480 个任务，覆盖 12 种语言，每种语言 40 个任务；ICAE-Bench-Lite 包含覆盖 10 种语言的 50 个任务。
- 该基准在 2 个代理框架 Claude Code 和 OpenHands 中评估了 6 个编码模型，结果发现模糊项目生成仍然具有挑战性。
- 研究报告称 GroundPRD 是一个较强的性能上界；澄清只能弥合部分性能差距，而更高的约束覆盖率并不会自动带来更高的通过率。
- 代理通常能够复现可见行为，但难以处理隐藏约束、边界情况和长周期集成；摘要未提供总体通过率或各模型的指标数值。
- 在 ICAE-Bench-Lite 上，Fuzzy L1 和 L3 在全部 50 个代码仓库中都被判定为与 GroundPRD 等效；两者的平均语义相似度得分分别为 0.952 和 0.942，并且没有任何案例被判定为可能无法通过相同的测试。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.21217v1](https://arxiv.org/abs/2607.21217v1)
