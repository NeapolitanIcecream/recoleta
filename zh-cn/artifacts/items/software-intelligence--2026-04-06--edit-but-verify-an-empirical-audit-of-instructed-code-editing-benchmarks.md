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
这篇论文审计了两个主要的带有人类编写指令和基于测试评估的指令式代码编辑基准：CanItEdit 和 EDIT-Bench。论文认为，这两个基准衡量的只是实际代码编辑中的一小部分，不能满足部署决策的需要，而且 EDIT-Bench 的测试材料尤其薄弱，甚至有缺陷。

## 问题
- 论文想回答的是，现有的指令式代码编辑基准是否真的反映了真实开发者的编辑工作，以及它们的测试能否可靠地判断正确性。
- 这个问题很重要，因为指令式代码编辑大约占真实编程助手交互的 19%，而基准分数常被用来为 IDE 助手等工具选择模型。
- 如果基准过度集中在错误的语言、领域或编辑类型上，或者测试漏掉回归，那么模型排名就会误导产品和部署决策。

## 方法
- 作者调研了 150 多个代码基准，发现只有两个符合他们的标准：基于人类编写的自然语言编辑指令、作用于已有代码、单文件局部范围、并且采用基于测试评估的 CanItEdit 和 EDIT-Bench。
- 他们把这两个基准与真实世界的参考来源进行比较：Copilot Arena、AIDev 和 GitHub Octoverse，比较了三个代表性维度：编程语言、编辑意图和应用领域。
- 他们在带有插桩的 Docker 环境中运行了所有基准测试套件，测量测试数量、整文件语句覆盖率、差分区域覆盖率，以及测试是否只检查请求的编辑，还是也能捕捉编辑区域外的非预期改动。
- 对于不发布参考解答的 EDIT-Bench，他们从已公布通过率为 100% 的模型中重建了可通过解答，以估计 91 个可执行问题的覆盖情况。
- 他们还检查了 15 个被全部 40 个模型都未解出的 EDIT-Bench 问题，并核查了两个基准内部的代码库重复情况。

## 结果
- 语言覆盖高度偏斜：CanItEdit 的 105/105 题都是 Python，EDIT-Bench 中 Python 占 89.8%。合在一起，这两个基准把 90% 以上的任务放在 Python 上，而 Python 在真实世界 AI 辅助编码活动中只占大约 20% 到 30%。按贡献者数量计算，GitHub 最常用的语言 TypeScript 完全缺失。
- 编辑意图范围很窄：EDIT-Bench 中 78.7%、CanItEdit 中 85.7% 都是功能或修复任务。AIDev 中占人类 PR 31.4% 的四类任务，即 docs、chore、build 和 ci，在这两个基准里都为 0%。编写测试的任务在两个基准里都只有 1.9%，而在 agent PR 中是 4.5%。
- 领域覆盖不匹配：后端和前端工作合计占真实世界编辑活动的 46%，但 CanItEdit 的后端和前端覆盖都为 0%，EDIT-Bench 也只到后端 13.9%、前端 10.2%。CanItEdit 把 68.6% 的任务放在算法题上，而真实世界参考中这一比例是 18%；EDIT-Bench 把 36.1% 放在 AI/ML 上，而参考中是 7%。
- 测试充分性差异很大：CanItEdit 每题测试数的中位数是 13，整文件覆盖率几乎完整（中位数 100.0%，均值 99.8%）。EDIT-Bench 的测试数中位数是 4（均值 4.7），有 14 道题只有一个测试，整文件覆盖率中位数为 40.0%（均值 48.7%），差分区域覆盖率中位数为 85.7%，均值为 64.9%；有 11 道题的差分区域覆盖率是 0%，91 道可执行题中有 39 道（42.9%）低于 75%。
- EDIT-Bench 的范围检查较弱：59% 的低覆盖测试套件无法发现请求编辑区域之外的额外改动，56% 的测试只检查被编辑的代码。论文举了一个例子：在悄悄改动卷积核大小的同时加入请求中的 Dropout 层，测试仍然通过。
- 在 15 个被全部 40 个模型都未解出的 EDIT-Bench 问题中，11 个被归因于基准材料问题，而不是模型能力限制。论文还报告了代码库重叠：EDIT-Bench 中 29% 的问题、CanItEdit 中 6% 的问题与同一基准里的另一个问题共享一个代码库。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.05100v1](http://arxiv.org/abs/2604.05100v1)
