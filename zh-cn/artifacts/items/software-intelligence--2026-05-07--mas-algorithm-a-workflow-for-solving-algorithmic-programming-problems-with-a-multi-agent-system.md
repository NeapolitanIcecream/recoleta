---
source: arxiv
url: https://arxiv.org/abs/2605.05949v2
published_at: '2026-05-07T09:57:53'
authors:
- Yuliang Xu
- Xiang Xu
- Yao Wan
- Hu Wei
- Tong Jia
topics:
- multi-agent-systems
- code-generation
- algorithmic-reasoning
- competitive-programming
- software-agents
- retrieval-augmented-generation
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# MAS-Algorithm: A Workflow for Solving Algorithmic Programming Problems with a Multi-Agent System

## Summary
## 总结
MAS-Algorithm 是一个面向竞赛编程问题的五智能体工作流。它在同一基础模型外增加了算法选择、检索、规划、编码、判题和错误反馈，从而提升了 Qwen 编码模型的通过率。

## 问题
- 算法编程任务检验编码模型能否选择算法、推理约束，并生成正确且高效的代码。
- 直接提示对中间推理的控制较弱，因此算法选择、复杂度、边界情况或实现中的错误都很难单独定位。
- 本研究中，微调成本较高，而且收益很小，所以推理时协调对代码智能系统更有用。

## 方法
- Agent1 根据候选标签选择可能的算法和数据结构，并支持多条解法分支。
- Agent2 使用 bge-zh 嵌入从本地 OI-WIKI 存储中检索算法知识，并将其总结给求解器。
- Agent3 编写结构化解题计划，Agent4 将计划转换为 C++ 代码，Agent5 诊断失败原因。
- 判题工具在 Docker gcc 环境中编译并运行代码，比较输出，并把失败案例发回 Agent5。
- Agent5 返回 PASS、FIX 或 RETHINK，将工作流转回代码修改或方案重规划，直到成功或达到迭代上限。

## 结果
- 在自建数据集上，MAS-Algorithm 相比直接提示，使五个 Qwen 模型的平均 AC 率提高了 6.48 个百分点，增幅在 +4.39 到 +9.00 个百分点之间。
- Qwen3-14B 的 AC 率从 28.98% 提高到 37.98%，增加 9.00 个百分点；其 case pass rate 从 29.34% 提高到 40.14%，增加 10.80 个百分点。
- Qwen3-Coder-30B-A3B-Instruct 的 AC 率从 32.25% 提高到 38.87%，增加 6.62 个百分点。对已接受解答进行 LoRA 微调后，直接提示的 AC 率只提高到 33.14%，增加 0.89 个百分点。
- Qwen3-235B-A22B-Instruct-2507 的 AC 率从 62.87% 提高到 67.26%，增加 4.39 个百分点。
- 在 LiveCodeBench-Pro 上，Qwen3-Coder-30B-A3B-Instruct 的 AC 率从 5.28% 提高到 10.00%，增加 4.72 个百分点；case pass rate 从 9.07% 提高到 14.05%。
- 替换实验给出了很高的上限收益：改进 Agent3 后 AC 率达到 66.57%，比该实验中的基础 MAS-Algorithm 设置高 27.70 个百分点；改进 Agent2 后 AC 率达到 61.82%，高 22.95 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05949v2](https://arxiv.org/abs/2605.05949v2)
