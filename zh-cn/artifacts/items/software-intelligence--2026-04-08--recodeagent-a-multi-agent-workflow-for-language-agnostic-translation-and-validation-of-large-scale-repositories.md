---
source: arxiv
url: http://arxiv.org/abs/2604.07341v1
published_at: '2026-04-08T17:54:08'
authors:
- Ali Reza Ibrahimzada
- Brandon Paulsen
- Daniel Kroening
- Reyhaneh Jabbarvand
topics:
- multi-agent-systems
- code-translation
- repository-level-analysis
- code-validation
- language-agnostic
relevance_score: 0.96
run_id: materialize-outputs
language_code: zh-CN
---

# ReCodeAgent: A Multi-Agent Workflow for Language-agnostic Translation and Validation of Large-scale Repositories

## Summary
## 摘要
ReCodeAgent 是一个多智能体系统，用于在不同编程语言之间翻译整个软件仓库，而不需要为每种语言对单独构建流程。它面向大型真实项目，在编译成功率和测试成功率上都高于以往的神经符号方法和智能体基线。

## 问题
- 这篇论文处理的是跨多个源语言和目标语言对的仓库级代码翻译与验证，而以往系统通常只支持一对语言，因为工程适配成本很高。
- 这之所以重要，是因为代码库迁移会影响可靠性、安全性和技术债；大型仓库还包含依赖、测试、命名一致性和长距离交互，简单的逐文件翻译会漏掉这些内容。
- 论文也针对智能体翻译中的两类失败模式：长流程中的幻觉式代码修改，以及在混合处理测试翻译和代码修复时验证薄弱。

## 方法
- ReCodeAgent 把任务拆成四个智能体：Analyzer、Planning、Translator 和 Validator。
- Analyzer 分析仓库结构、依赖、错误处理和库的使用，然后写出目标项目设计，包括目标语言的库选择和结构映射。
- Planning 智能体识别翻译单元，建立名称映射和项目骨架，并制定考虑依赖关系的实现计划。
- Translator 将源代码和测试都翻译到目标仓库中，而 Validator 运行翻译后的测试，检查覆盖缺口，为未覆盖函数生成额外测试，并把修复报告发回给 Translator。
- 为了保持与语言无关，系统通过 MCP 暴露通用工具，尤其是 Language Server Protocol 工具和轻量级项目分析工具，而不是为每种语言对手工构建程序分析流程。

## 结果
- 评估覆盖 118 个真实项目、4,583 个翻译单元，以及 6 种语言和 4 种语言对上的 23 万多行代码：C-Rust、Go-Rust、Java-Python 和 Python-JavaScript。
- ReCodeAgent 的平均编译成功率达到 99.4%，测试通过率达到 86.5%。论文称，这比基于真实标签测试的其他方法高出 2.5 个百分点的编译成功率和 60.8 个百分点的测试通过率。
- 平均项目规模为 1,975 行代码和 43 个翻译单元。平均运行时间为 57 分钟，平均每个项目成本为 15.3 美元。
- 对翻译后的测试，论文报告了 99.3% 的断言等价性、0.91 的余弦相似度和 94.9% 的断言类型匹配率。
- 消融实验中，去掉 Analyzer、Planning 和 Validator 后，测试通过率分别下降 22.7、25.3 和 30.3 个百分点，轨迹复杂度增加 28%。
- 与两个基线智能体相比，这些基线的测试通过率只有 25.3% 和 24.1%，论文报告它们分别比 ReCodeAgent 低 61.2 和 62.4 个百分点。单智能体设计的测试通过率也下降 40.4 个百分点，轨迹长度增加 28%。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07341v1](http://arxiv.org/abs/2604.07341v1)
