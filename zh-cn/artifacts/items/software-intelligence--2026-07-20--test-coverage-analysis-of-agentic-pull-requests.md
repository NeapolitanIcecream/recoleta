---
source: arxiv
url: https://arxiv.org/abs/2607.18057v1
published_at: '2026-07-20T15:26:30'
authors:
- Atish Kumar Dipongkor
- Talank Baral
- Wing Lam
- Kevin Moran
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- multi-agent-software-engineering
- human-ai-interaction
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# Test Coverage Analysis of Agentic Pull Requests

## Summary
## 摘要
这项研究发现，智能体生成的拉取请求往往没有对新增代码进行充分测试。在来自五个编码智能体的 AIDev 数据集中的 4,882 个 Java 和 Python PR 中，现有测试仅覆盖 61.5% 的 Java 变更可执行代码行和 27.0% 的 Python 变更可执行代码行，而智能体编写的测试只在少数情况下提高了覆盖率。

## 问题
- 自主编码智能体越来越多地提交完整的拉取请求，但人们对其测试行为以及自身变更的覆盖情况仍缺乏了解。
- 现有测试通过并不能说明新增代码已被执行，这可能使容易引发回归的路径，尤其是错误处理路径，处于未测试状态。

## 方法
- 分析 AIDev 数据集中的 4,882 个 PR：其中包括 532 个 Java PR 和 4,350 个 Python PR，由五个编码智能体生成。
- 根据 PR 是否修改生产代码、测试文件或两者兼有对 PR 进行分类，并测量智能体添加或修改测试的频率。
- 重建 PR 补丁，并使用 JaCoCo（Java）和 pytest-cov（Python）运行代码仓库的测试套件。
- 使用现有测试计算新增可执行代码行的差异覆盖率，然后移除智能体编写的测试变更，以估计其带来的增量覆盖率提升。
- 按语法结构标记新增代码行，以识别持续处于测试不足状态的代码类别。

## 结果
- 在修改了受测试代码的 4,387 个 PR 中，50.4% 没有修改测试文件，49.6% 修改了测试文件。
- 现有测试覆盖了 Java 中 61.5% 的变更可执行代码行和 Python 中 27.0% 的变更可执行代码行。在 Python 中，64.8% 的分析 PR 没有任何变更代码行被现有测试执行。
- 智能体编写的测试将 Java 的平均差异覆盖率从 70.5% 提高到 86.1%（增加 15.6 个百分点；64 个 Code + Tests PR；p<0.001），并将 Python 的平均差异覆盖率从 24.8% 提高到 34.5%（增加 9.6 个百分点；605 个 PR；p<0.001）。
- 只有 35.9% 的 Java Code + Tests PR 和 22.5% 的 Python Code + Tests PR 实现了覆盖率提升。在覆盖率未提升的 Java PR 中，智能体删除了 82 个测试、添加了 31 个测试，删除与添加的比例为 2.6 倍；在 Python 中，74.8% 的 PR 虽然添加了测试，但这些测试仍未覆盖其变更代码行。
- 错误处理结构尤其缺乏测试：Java 和 Python 中 Try-Catch 代码行的未覆盖率分别为 86.0% 和 81.0%，而 Throw 代码行的未覆盖率分别为 67.5% 和 82.3%。
- 覆盖率分析仅限于已合并且能够完成构建和插桩的 PR——213 个 Java PR 和 1,664 个 Python PR——因此结果未必适用于所有智能体生成的 PR。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.18057v1](https://arxiv.org/abs/2607.18057v1)
