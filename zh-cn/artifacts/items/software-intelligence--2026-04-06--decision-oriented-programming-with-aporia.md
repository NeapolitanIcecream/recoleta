---
source: arxiv
url: http://arxiv.org/abs/2604.05203v1
published_at: '2026-04-06T22:02:01'
authors:
- Saketh Ram Kasibatla
- Raven Rothkopf
- Hila Peleg
- Benjamin C. Pierce
- Sorin Lerner
- Harrison Goldstein
- Nadia Polikarpova
topics:
- ai-programming-agents
- code-intelligence
- human-ai-interaction
- software-engineering
- test-based-specification
relevance_score: 0.89
run_id: materialize-outputs
language_code: zh-CN
---

# Decision-Oriented Programming with Aporia

## Summary
## 摘要
Aporia 是一个 VS Code 编程助手，它围绕明确的设计决策来组织交互，而不是依赖自由形式的提示和计划。论文认为，这种交互方式能让开发者持续参与设计，并帮助他们理解代理实际实现了什么。

## 问题
- 编码代理通过让开发者在高层次上说明目标来降低工作量，但代理随后会自行补全许多设计细节。
- 这些隐藏的决策会造成“认知债务”：开发者会逐渐失去对系统行为的把握，脑中的理解模型也可能与代码不一致。
- 现有的“提示-生成-审查”工作流很容易让人不经意地接受代理的选择，忽略策略、约束条件和边界情况等关键设计分支。

## 方法
- 论文提出了 **decision-oriented programming (DOP)**，即围绕明确、可编辑的设计决策来组织程序员与代理的协作。
- Aporia 将这一思路实现为一个 VS Code 扩展，其中包含一个持久化的 **Decision Bank**，用于存储结构化决策，程序员可以查看、编辑或补充这些决策。
- 一个 **questioner** 代理会提出带可选评论的是/否设计问题，从程序员那里引出决策；系统还会显示相关代码引用，让问题与代码库中的具体内容对应起来。
- 一个 **planner** 代理会把每个被接受的决策转成一组测试，因此每个决策都有一个与代码行为绑定的可执行规格。
- 一个 **implementer** 代理会结合目标、Decision Bank 和生成的测试来修改代码库；随后这些测试会验证实现是否符合已记录的决策。

## 结果
- 评估采用被试内用户研究，包含 **14 名程序员**，比较 Aporia 与 **Claude Code** 在现有 Python 代码库上添加功能时的表现。
- 论文称 Aporia 提高了开发者在设计过程中的**参与度**：参与者表达出的**设计决策显著更多**，并且在开发过程中表现出更持续的反思。摘录没有给出确切数量或检验统计量。
- Aporia 提高了理解准确性：与基线代理相比，参与者的心理模型与代码发生不一致的可能性**降低到 1/5**。
- 引言还报告称，与基线编码代理相比，参与者心理模型与实际实现之间出现不匹配的可能性**降低了 79%**。
- 文中称，该系统通过把决策转成可检查的测试，并把 Decision Bank 用作审查清单，帮助完成**探索**和**验证**。
- 除了上述用户研究结论外，摘录没有提供任务层面的准确率、通过率、时间或生产率数据。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05203v1](http://arxiv.org/abs/2604.05203v1)
