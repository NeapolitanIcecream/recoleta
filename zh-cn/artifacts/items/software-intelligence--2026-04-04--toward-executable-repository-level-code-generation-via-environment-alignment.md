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
## 总结
EnvGraph 面向仓库级代码生成，这类任务的成功取决于生成的多文件项目能否真正安装、运行并通过验证。它把执行失败看作环境对齐问题，覆盖外部依赖和仓库内部引用两层，然后在一个有针对性的循环里修改仓库。

## 问题
- 仓库级代码生成在真实执行中常常失败，因为生成的项目无法安装依赖、无法解析跨文件的导入和符号，或者无法正常启动。
- 同样的运行时错误，比如 `ModuleNotFoundError`，可能来自两种不同原因：缺少外部包，或者内部引用断裂。只跟着可见错误走的修改循环，可能会改错位置。
- 这很关键，因为可执行验证比代码看起来合理更严格：仓库必须作为一个整体可运行，而不是只在单个文件里看起来正确。

## 方法
- EnvGraph 为当前仓库构建两张图：一张是外部环境图，表示包的使用和声明；另一张是仓库依赖图，表示文件、模块、导入、符号、未解析引用和解析错误。
- 它会执行仓库，并收集安装失败、运行时错误、调用栈和测试结果等证据。
- 它先规范化这些证据，再用明确的归因策略按优先级选择主要失败来源：外部依赖失败、内部引用解析失败，然后是剩余的逻辑错误。
- 根据这个诊断，它进行一次有针对性的修改，重点修复依赖、内部链接或逻辑问题，然后重建这些图并重复，直到成功或预算用完。
- 论文把这称为环境对齐，而不是泛化的生成-执行-修改流程，因为修改方向取决于当前破坏的是哪一个执行前置条件。

## 结果
- 在三个骨干 LLM 上，EnvGraph 在 **Functional Correctness** 上都比最强的非 EnvGraph 基线高 **5.72 到 5.87 个百分点**。
- 它在 **Non-Functional Quality** 上也比最强的非 EnvGraph 基线高 **4.58 到 8.66 个百分点**。
- 评测使用两个仓库级基准：**RAL-Bench**，包含 **38** 个任务，分布在 **7** 个类别中；以及 **NL2Repo-Bench**，包含 **104** 个任务，分布在 **9** 个类别中。
- NL2Repo-Bench 的输入平均约为 **18.8k** tokens，并划分为 **26 个 easy / 46 个 medium / 32 个 hard** 任务。
- 在 NL2Repo-Bench 上，对 **GPT-5**、**DeepSeek-V3** 和 **Gemini-3-Pro-Preview** 的失败直接生成做的一个动机性错误分析中，环境相关失败分别占 **34.7%**、**68.9%** 和 **30.9%**。
- 这段摘要没有给出完整的按模型得分表、带数值的基线名称或消融结果，但它声称相对有代表性的环境感知方法和仓库级方法都有稳定提升。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.03622v1](http://arxiv.org/abs/2604.03622v1)
