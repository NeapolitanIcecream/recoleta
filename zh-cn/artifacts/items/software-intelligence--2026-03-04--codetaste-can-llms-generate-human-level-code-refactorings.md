---
source: arxiv
url: http://arxiv.org/abs/2603.04177v1
published_at: '2026-03-04T15:34:18'
authors:
- Alex Thillen
- "Niels M\xFCndler"
- Veselin Raychev
- Martin Vechev
topics:
- code-refactoring
- llm-agents
- benchmarking
- code-intelligence
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# CodeTaste: Can LLMs Generate Human-Level Code Refactorings?

## Summary
本文提出了 **CODETASTE**，一个面向真实开源仓库的大规模代码重构基准，用来衡量 LLM 是否不仅能“执行”重构，还能自主发现与人类开发者一致的重构选择。结论是：当前前沿模型在详细指令下能较好完成重构，但在只给出模糊改进方向时，与人类重构偏好的对齐仍然很弱。

## Problem
- 现有 LLM 编码代理虽然能生成可运行代码，但容易累积复杂度、重复代码和架构债，长期可维护性差。
- 现有重构基准多是小范围、低难度任务，不能衡量模型是否能在真实多文件代码库中**自主识别**该做什么重构。
- 这个问题重要，因为自动化软件生产若无法持续改善代码结构，代理生成的代码库会逐渐变得难以扩展、难以维护，限制真实工程落地。

## Approach
- 构建 **CODETASTE**：从 GitHub 挖掘 **100 个**由人类开发者完成的真实大型多文件重构，覆盖 **87 个仓库、6 种语言**。
- 为每个任务建立可复现容器环境，运行仓库测试套件，并生成静态分析规则来检查“坏模式是否被移除、好模式是否被引入”。这些规则支持基于 AST 和文件内数据流的语义匹配。
- 设计两条评测轨道：**Instructed track** 给出详细重构说明，测“按要求执行”；**Open track** 只给出模糊的改进焦点，测“能否发现人类实际选择的重构”。
- 提出核心指标 **alignment score = PASS × IFR**：只有在测试通过的前提下，才奖励对重构意图的遵循；同时还度量 precision 以检查是否引入无关修改。
- 在 Open track 中进一步测试 **Direct / Plan / Oracle Multiplan** 三种模式，验证“先提案再实现”是否更接近人类重构决策。

## Results
- 基准规模较大：平均每个任务需修改 **91.52 个文件**、**2605.39 行代码**；最复杂任务达到 **290 个文件**、**18821 行改动**。每个实例平均运行 **1638.53 个测试**，并检查 **93.07 条**静态规则。
- **Instructed track** 中，GPT-5.2 最强，平均 alignment **69.6%**；SONNET 4.5 为 **32.4%**，GPT-5.1 CODEX MINI 为 **34.6%**，QWEN3 为 **11.8%**。这说明“已知该做什么重构”时，前沿模型已能较好执行大型重构。
- 在同一轨道中，GPT-5.2 的 PASS 为 **76.0%**，明显高于 SONNET 4.5 的 **47.0%** 和 GPT-5.1 M 的 **43.0%**；但三者 IFR 仍较高，分别为 **89.3% / 69.2% / 72.2%**，表明主要差距在于保持功能正确性而非理解指令。
- Instructed track 的 precision 与人类接近：SONNET 4.5 **58.9%**、GPT-5.1 M **58.5%**、GPT-5.2 **56.2%**，而人类为 **57.5%**。说明在明确任务下，模型大体能把修改限制在相关范围内。
- **Open track** 中，模型只能取得很低对齐：Direct 模式最佳仅 **7.7%**（GPT-5.2），论文还概括整体“无具体重构说明时总体 alignment **低于 8%**”，显示模型很难自主找出与人类一致的重构决策。
- “先提案再实现”有效：GPT-5.2 在 Open track 从 Direct 的 **7.7%** 提升到 Plan 的 **14.1%**；Oracle Multiplan 进一步到 **19.4%**。论文还称平均提升接近 **3 个百分点**、相对增幅 **超过 50%**，个别情况下 IFR 相对提升可达 **72%**。不过更大范围改动也可能导致 PASS 最多下降 **24%**。

## Link
- [http://arxiv.org/abs/2603.04177v1](http://arxiv.org/abs/2603.04177v1)
