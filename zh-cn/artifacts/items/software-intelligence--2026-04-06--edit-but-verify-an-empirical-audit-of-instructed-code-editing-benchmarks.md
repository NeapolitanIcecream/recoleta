---
source: arxiv
url: http://arxiv.org/abs/2604.05100v1
published_at: '2026-04-06T18:59:42'
authors:
- Amir M. Ebrahimi
- Gopi Krishnan Rajbahadur
topics:
- code-editing-benchmarks
- llm-evaluation
- benchmark-audit
- software-engineering
- test-coverage
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Edit, But Verify: An Empirical Audit of Instructed Code-Editing Benchmarks

## Summary
## 摘要
这篇论文审查了两个主要的、带有人类编写指令并采用基于测试评估的指令式代码编辑基准：CanItEdit 和 EDIT-Bench。论文认为，这两个基准覆盖的真实代码编辑范围都比部署决策所需的更窄，而且 EDIT-Bench 尤其存在薄弱或有缺陷的测试产物。

## 问题
- 论文要回答的是：当前的指令式代码编辑基准是否真的反映了开发者的实际编辑工作，以及它们的测试是否能可靠地判断正确性。
- 这很重要，因为指令式代码编辑约占真实编码助手交互的 19%，而基准分数会被用来为 IDE 助手等工具选择模型。
- 如果基准过度集中在错误的语言、领域或编辑类型上，或者测试漏掉了回归问题，那么模型排名就会误导产品和部署选择。

## 方法
- 作者调研了 150 多个代码基准，只发现两个符合其标准：在人类编写的自然语言编辑指令下对现有代码进行修改、范围限于单文件局部编辑，并采用基于测试的评估。这两个基准是 CanItEdit 和 EDIT-Bench。
- 他们将这两个基准与真实世界的参考来源进行对比：Copilot Arena、AIDev 和 GitHub Octoverse，并使用三个代表性维度：编程语言、编辑意图和应用领域。
- 他们在加入插桩的 Docker 环境中执行了所有基准测试套件，并测量了测试数量、整文件语句覆盖率、diff 区域覆盖率，以及测试是否只检查请求的编辑，还是也能捕捉编辑区域之外的不需要修改。
- 对于不发布参考解答的 EDIT-Bench，作者从公开通过率为满分的模型中重建了可通过的解答，以估计 91 个可执行问题上的覆盖率。
- 他们还检查了 15 个被 40 个已评估模型全部未解出的 EDIT-Bench 问题，并检查了两个基准内部的代码库重复情况。

## 结果
- 语言覆盖严重失衡：CanItEdit 的 105/105 题全是 Python，EDIT-Bench 中 89.8% 是 Python。合在一起，这两个基准把超过 90% 的任务放在 Python 上，而 Python 在真实世界 AI 辅助编码活动中的占比只有约 20–30%。按贡献者数量计，GitHub 使用最多的语言 TypeScript 完全缺失。
- 编辑意图很窄：EDIT-Bench 中 78.7%、CanItEdit 中 85.7% 的任务都是功能或修复任务。在 AIDev 中占人类 PR 31.4% 的四类任务——docs、chore、build 和 ci——在两个基准中的占比都是 0%。测试编写任务在每个基准中都只有 1.9%，而在 agent PR 中是 4.5%。
- 领域覆盖与现实不匹配：后端和前端工作合计占真实编辑活动的 46%，但 CanItEdit 的后端覆盖和前端覆盖都是 0%，EDIT-Bench 也只有 13.9% 的后端和 10.2% 的前端。CanItEdit 把 68.6% 的任务放在算法问题上，而真实世界参考中这一比例是 18%；EDIT-Bench 把 36.1% 的任务放在 AI/ML 上，而参考中是 7%。
- 测试充分性差异很大：CanItEdit 每题测试数的中位数是 13，整文件覆盖率接近完整（中位数 100.0%，均值 99.8%）。EDIT-Bench 每题测试数中位数是 4（均值 4.7），其中 14 题只有一个测试；整文件覆盖率中位数为 40.0%（均值 48.7%），diff 区域覆盖率中位数为 85.7%，但均值只有 64.9%；有 11 题的 diff 区域覆盖率是 0%，在 91 个可执行问题中有 39 题（42.9%）低于 75% 的 diff 区域覆盖率。
- EDIT-Bench 的范围检查较弱：59% 的低覆盖率测试套件无法检测出请求编辑区域之外的额外修改，56% 的全部测试只检查被编辑的代码。论文给出的一个例子是：按要求加入 Dropout 层的同时，偷偷修改卷积核大小，测试仍然会通过。
- 在 15 个被全部 40 个模型都未解出的 EDIT-Bench 问题中，11 个失败原因被归因于基准产物，而不是模型能力上限。论文还报告了代码库重叠：EDIT-Bench 中 29% 的问题、CanItEdit 中 6% 的问题与同一基准中的其他问题共享代码库。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05100v1](http://arxiv.org/abs/2604.05100v1)
