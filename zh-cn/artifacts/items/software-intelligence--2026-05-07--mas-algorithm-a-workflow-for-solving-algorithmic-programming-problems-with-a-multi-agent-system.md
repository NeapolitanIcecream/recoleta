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
## 摘要
MAS-Algorithm 是一个面向竞赛编程问题的五智能体工作流。它在同一基础模型外围加入算法选择、检索、规划、编码、评测和错误反馈，从而提高 Qwen 编码模型的通过率。

## 问题
- 算法编程任务会测试编码模型能否选择算法、推理约束，并生成正确且高效的代码。
- 直接提示对中间推理过程的控制较弱，因此算法选择、复杂度、边界情况或实现中的错误较难定位。
- 微调成本可能较高，并且在这项研究中增益较小，这使得推理时协调对代码智能系统有用。

## 方法
- Agent1 从候选标签中选择可能的算法和数据结构，并支持多个解法分支。
- Agent2 使用 bge-zh embeddings 从本地 OI-WIKI 存储中检索算法知识，并为求解器总结内容。
- Agent3 编写结构化解题计划，Agent4 将计划转换为 C++ 代码，Agent5 诊断失败原因。
- 评测工具在 Docker gcc 环境中编译并运行代码，比较输出，并将失败用例发送回 Agent5。
- Agent5 返回 PASS、FIX 或 RETHINK，将工作流路由回代码修订或解法重新规划，直到成功或达到迭代上限。

## 结果
- 在自建数据集上，MAS-Algorithm 使五个 Qwen 模型的平均 AC 率相比直接提示提高了 6.48 个百分点，增益范围为 +4.39 到 +9.00 个百分点。
- Qwen3-14B 的 AC 率从 28.98% 升至 37.98%，提高 +9.00 个百分点；其用例通过率从 29.34% 升至 40.14%，提高 +10.80 个百分点。
- Qwen3-Coder-30B-A3B-Instruct 的 AC 率从 32.25% 升至 38.87%，提高 +6.62 个百分点。使用已通过解法进行 LoRA 微调后，直接提示的 AC 率仅提升到 33.14%，提高 +0.89 个百分点。
- Qwen3-235B-A22B-Instruct-2507 的 AC 率从 62.87% 升至 67.26%，提高 +4.39 个百分点。
- 在 LiveCodeBench-Pro 上，Qwen3-Coder-30B-A3B-Instruct 的 AC 率从 5.28% 升至 10.00%，提高 +4.72 个百分点；用例通过率从 9.07% 升至 14.05%。
- 替换研究报告了较大的上界增益：改进 Agent3 后 AC 率达到 66.57%，比该实验中的基础 MAS-Algorithm 设置高 +27.70 个百分点；改进 Agent2 后 AC 率达到 61.82%，高 +22.95 个百分点。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05949v2](https://arxiv.org/abs/2605.05949v2)
