---
source: arxiv
url: http://arxiv.org/abs/2604.03622v1
published_at: '2026-04-04T07:37:55'
authors:
- Ruwei Pan
- Junlei Shen
- Linhao Wu
- Yueheng Zhu
- Zixiong Yang
- Yakun Zhang
- Lu Zhang
- Hongyu Zhang
topics:
- repository-level-code-generation
- environment-alignment
- code-execution
- dependency-resolution
- multi-file-generation
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Toward Executable Repository-Level Code Generation via Environment Alignment

## Summary
## 摘要
EnvGraph 面向仓库级代码生成。这里的成功标准是：生成的多文件项目能否实际完成安装、运行并通过验证。它把执行失败视为一个环境对齐问题，同时处理外部依赖和仓库内部引用，然后在一个定向循环中修改仓库。

## 问题
- 仓库级代码生成在真实执行中经常失败，因为生成的项目无法安装依赖、无法解析跨文件的导入和符号，或者不能正常启动。
- 同一种运行时症状，比如 `ModuleNotFoundError`，可能来自两种不同原因：缺少外部包，或内部引用损坏。只跟着表面报错走的修订循环，可能会修改仓库中错误的部分。
- 这很重要，因为可执行验证比代码表面看起来合理更严格：仓库必须作为一个整体工作，而不是只在逐个文件查看时显得正确。

## 方法
- EnvGraph 为当前仓库构建两张图：一张外部环境图，用于表示包的使用和声明；一张仓库依赖图，用于表示文件、模块、导入、符号、未解析引用和解析错误。
- 它执行仓库，并收集安装失败、运行时错误、堆栈跟踪和测试结果等证据。
- 它先对这些证据做规范化处理，然后应用一套明确的归因策略，按优先级选出主要失败来源：外部依赖失败、内部引用解析失败，最后是剩余的逻辑错误。
- 根据这一诊断，它执行一次定向修订，重点处理依赖修复、内部链接修复或逻辑修复，然后重建两张图并重复这一过程，直到成功或预算耗尽。
- 论文把这描述为环境对齐，而不是一般的生成—执行—修订流程，因为修订方向取决于当前究竟是哪一个执行前提条件出了问题。

## 结果
- 在三个骨干 LLM 上，EnvGraph 在 **Functional Correctness** 上比最强的非 EnvGraph 基线高 **5.72 到 5.87 个百分点**。
- 在 **Non-Functional Quality** 上，它也比最强的非 EnvGraph 基线高 **4.58 到 8.66 个百分点**。
- 评估使用了两个仓库级基准：**RAL-Bench**，包含 **38 个任务**、覆盖 **7 个类别**；以及 **NL2Repo-Bench**，包含 **104 个任务**、覆盖 **9 个类别**。
- **NL2Repo-Bench** 的输入平均约 **18.8k tokens**，并分为 **26 个 easy / 46 个 medium / 32 个 hard** 任务。
- 在一项针对 **GPT-5**、**DeepSeek-V3** 和 **Gemini-3-Pro-Preview** 在 NL2Repo-Bench 上直接生成失败案例的动机性错误研究中，环境相关失败分别占总失败的 **34.7%**、**68.9%** 和 **30.9%**。
- 摘要没有给出完整的分模型得分表、带具体数值的基线名称或消融实验结果，但文中声称，相比有代表性的环境感知方法和仓库级方法，EnvGraph 都有稳定提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03622v1](http://arxiv.org/abs/2604.03622v1)
