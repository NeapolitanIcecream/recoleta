---
source: arxiv
url: https://arxiv.org/abs/2605.26017v1
published_at: '2026-05-25T16:35:36'
authors:
- Jian Fang
- Yingfei Xiong
topics:
- formal-verification
- llm-agents
- code-generation
- software-engineering
- interactive-theorem-proving
- risc-v
relevance_score: 0.88
run_id: materialize-outputs
language_code: zh-CN
---

# Trustworthy Software Project Generation : a Case Study with an Interactive Theorem Prover

## Summary
## 摘要
这篇论文介绍了 SPDDwL，一种 LLM 代理工作流，用 Rocq 证明的纯核心和 C++ 主机集成生成可运行的软件项目。案例研究自动根据需求构建了一个 RISC-V RV32I 解释器。

## 问题
- LLM 生成的项目可以编译并通过现有测试，但仍然违反预期语义，这对 CPU 解释器和其他实现状态转换的代码很重要。
- 形式化验证可以捕捉语义错误，但当失败的证明尝试只给出很弱的修复信号时，LLM 代理很难完成项目规模的验证代码。
- 交互式定理证明器适合处理纯总函数，但部署的软件也需要 I/O 和运行时效应，所以系统必须把已验证逻辑和主机侧代码分开。

## 方法
- 需求分析代理把自然语言需求转换成一个编码计划，里面包括数据类型、纯函数、主机职责和形式性质。
- 编码代理为纯核心生成 Rocq 函数定义，证明代理生成 Rocq 命题和战术证明。
- Rocq 检查这些定义和证明；如果失败，SPDDwL 会把证明状态和诊断信息返回给代理进行修复。
- 通过检查的 Rocq 定义会用 Crane 提取为 C++，再和处理效应的主机层链接。形式化保证适用于抽取后的核心及其规格。

## 结果
- 这个案例实现了无特权 RISC-V RV32I 基础中的全部 47 条指令，形式是一个 CPU 解释器。
- 在 Claude Opus 4.7 和 Rocq 9.0.1 下，SPDDwL 在收到需求后，无需人工介入，就在 30 分钟预算内完成了项目。
- 这次运行生成了 1,859 行经过验证的 Rocq 代码，并提取出 2,848 行 C++。
- 解释器通过了 265 个由 LLM 生成的指令测试，覆盖这 47 条指令。
- 12 小时的 AFL++ 模糊测试运行执行了 9,820 万个输入，发现 0 次崩溃和 0 次卡死。
- 在相同的 30 分钟配置下，Dafny 后端没能完成验证；论文把 Rocq 的结果归因于显式的证明状态反馈，这给了代理修复信息。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.26017v1](https://arxiv.org/abs/2605.26017v1)
