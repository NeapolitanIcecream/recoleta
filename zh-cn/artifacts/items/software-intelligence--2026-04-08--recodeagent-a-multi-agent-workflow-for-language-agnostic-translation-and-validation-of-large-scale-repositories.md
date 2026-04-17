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
ReCodeAgent 是一个多智能体系统，用于在编程语言之间翻译整个软件仓库，而不需要为每种语言对单独构建一条流程。它面向大型真实项目，并报告了比以往神经符号和智能体基线更高的编译成功率和测试成功率。

## 问题
- 论文处理的是多个源语言-目标语言对之间的仓库级代码翻译与验证。以往系统通常只支持一种语言对，因为工程适配成本很高。
- 这很重要，因为代码库迁移会影响可靠性、安全性和技术债，而大型仓库包含依赖、测试、命名一致性和长程交互，简单的逐文件翻译会漏掉这些内容。
- 论文还针对智能体翻译中的两类失败模式：长流程中产生幻觉式代码修改，以及在测试翻译和代码修复被草率混合时出现的验证薄弱问题。

## 方法
- ReCodeAgent 将任务拆分给四个智能体：Analyzer、Planning、Translator 和 Validator。
- Analyzer 研究仓库结构、依赖关系、错误处理和库的使用情况，然后编写目标项目设计，其中包含目标语言的库选择和结构映射。
- Planning 智能体识别翻译单元，构建名称映射和项目骨架，并生成考虑依赖关系的实现计划。
- Translator 将源代码和测试一起翻译到目标仓库中；Validator 运行已翻译的测试，检查覆盖缺口，为未覆盖函数生成额外测试，并将修复报告发回给 Translator。
- 为了保持语言无关性，系统使用通过 MCP 暴露的通用工具，尤其是 Language Server Protocol 工具和轻量级项目分析工具，而不是为每种语言对手工构建程序分析。

## 结果
- 评估覆盖 118 个真实项目、4,583 个翻译单元，以及超过 23 万行代码，涉及 6 种语言和 4 种语言对：C-Rust、Go-Rust、Java-Python 和 Python-JavaScript。
- ReCodeAgent 平均达到 99.4% 的编译成功率和 86.5% 的测试通过率。论文称，在真实测试集上，这比其他方法的编译成功率高 2.5 个百分点，测试通过率高 60.8 个百分点。
- 项目平均规模为 1,975 行代码和 43 个翻译单元。平均运行时间为 57 分钟，平均成本为每个项目 15.3 美元。
- 对于已翻译的测试，论文报告了 99.3% 的断言等价率、0.91 的余弦相似度和 94.9% 的断言类型匹配率。
- 在消融实验中，移除 Analyzer、Planning 和 Validator 会使测试通过率分别下降 22.7、25.3 和 30.3 个百分点，并使轨迹复杂度增加 28%。
- 与两个基线智能体相比，这些基线的测试通过率只有 25.3% 和 24.1%。论文称，这比 ReCodeAgent 分别低 61.2 和 62.4 个百分点。单智能体设计也会使测试通过率下降 40.4 个百分点，并产生长 28% 的轨迹。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.07341v1](http://arxiv.org/abs/2604.07341v1)
