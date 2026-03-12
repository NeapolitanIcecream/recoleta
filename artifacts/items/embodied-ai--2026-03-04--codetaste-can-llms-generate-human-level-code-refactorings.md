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
- llm-for-code
- code-refactoring
- software-engineering-benchmark
- agent-evaluation
- static-analysis
relevance_score: 0.03
run_id: materialize-outputs
---

# CodeTaste: Can LLMs Generate Human-Level Code Refactorings?

## Summary
CODETASTE研究LLM是否不仅能“改对代码”，还能做出接近人类开发者选择的重构决策。论文提出一个面向真实多文件仓库重构的基准，显示当前前沿模型在按详细指令执行重构时表现较强，但在自主发现应做什么重构上明显不足。

## Problem
- 现有LLM编码代理能生成功能正确的补丁，但常积累复杂度、重复代码和架构债务；真正可持续的软件开发需要**保持行为不变地改善结构**，即重构。
- 现有重构基准多为小范围、低难度任务，难以衡量模型在**真实大型代码库**中的能力，也无法测试模型是否能**自主识别人类会选择的重构**。
- 这很重要，因为如果代理无法识别并执行合适重构，它们构建出的代码库会越来越难维护、扩展和继续演化。

## Approach
- 构建了**CODETASTE**：从GitHub历史提交中挖掘**100个真实的大型多文件重构**，覆盖**87个仓库、6种编程语言**。
- 为每个任务自动生成可复现实验环境，并结合**仓库测试套件**与**静态规则**评测：既要求功能不回归，也要求真正把“不想要的代码模式”变成“想要的代码模式”。
- 静态规则使用带有**AST模式和文件内数据流推理**的规则语言，避免只做表面字符串匹配，更贴近重构的语义意图。
- 设计两条评测轨道：**Instructed track**给出详细重构说明，测试执行能力；**Open track**只给模糊改进方向，测试是否能发现与人类一致的重构选择。
- 在Open track中进一步比较三种模式：**Direct**直接改、**Plan**先提计划再实现、**Oracle Multiplan**先生成多个计划再用有完整说明的判别器选最接近人类方案的计划。

## Results
- 基准本身规模较大：单任务平均需修改**91.52个文件**、**2605.39行代码**；最多达**290个文件**、**18821行变更**。每个实例平均运行**1638.53个测试**，并检查**29.66条加性规则**与**63.41条减性规则**。
- 在**Instructed track**，GPT-5.2取得最佳平均对齐分数**69.6%**；相比之下，SONNET 4.5为**32.4%**，GPT-5.1 CODEX MINI为**34.6%**，QWEN3为**11.8%**。
- 指令执行层面，前沿模型的IFR较高：GPT-5.2 **89.3%**，GPT-5.1 M **72.2%**，SONNET 4.5 **69.2%**；但功能正确率PASS差距明显，GPT-5.2为**76.0%**，而GPT-5.1 M和SONNET 4.5分别只有**47.0%**和**43.0%**。
- 在**Open track**，即只给模糊目标时，最好直接推理结果也只有**7.7% alignment**（GPT-5 CODEX）；QWEN3 direct仅**2.3%**。论文还概括称所有模型总体上在该设置下**低于8% alignment**，说明“知道该重构什么”远难于“照说明去重构”。
- **先提计划再实现**有明显帮助：GPT-5.2的alignment从**7.7%**提升到**14.1%**，几乎翻倍；平均提升接近**3个百分点**，相当于**50%以上相对增幅**，且IFR最高可提升**72%相对增幅**。
- 在**Oracle Multiplan**下，GPT-5.2达到**19.4% alignment**，表明模型提出的多个候选方案中常常包含更接近人类选择的方案；但SONNET 4.5从Plan的**10.2%**略降到**9.7%**。此外，开放轨道的PREC最高仅**21.0%**，说明模型常伴随大量无关修改。

## Link
- [http://arxiv.org/abs/2603.04177v1](http://arxiv.org/abs/2603.04177v1)
