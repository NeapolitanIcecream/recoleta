---
source: arxiv
url: http://arxiv.org/abs/2604.04979v1
published_at: '2026-04-04T18:52:44'
authors:
- "\xC1d\xE1m Kov\xE1cs"
topics:
- coding-agents
- context-pruning
- tool-output-extraction
- code-intelligence
- swe-bench
relevance_score: 0.95
run_id: materialize-outputs
language_code: zh-CN
---

# Squeez: Task-Conditioned Tool-Output Pruning for Coding Agents

## Summary
## 摘要
Squeez 针对编码代理中的一个范围较窄但很实用的任务：给定一个查询和一条工具输出，只保留对下一步有用的最小逐字文本块。论文发布了这个任务的基准，并表明一个用 LoRA 微调的 Qwen 3.5 2B 模型优于更大的零样本模型和简单的剪枝启发式方法。

## 问题
- 编码代理会反复重读很长的工具输出，例如文件读取结果、日志、堆栈跟踪、grep 命中和 git 历史，即使其中只有一小部分与下一步动作有关。
- 这会在代理循环中浪费上下文和算力，尤其是在软件调试和仓库操作里，因为相关证据可能出现在输出的任何位置。
- 论文聚焦于单条观测的剪枝：针对一个聚焦查询，提取最小的逐字证据块，让代理保留有用的文本行并丢弃其余内容。

## 方法
- 作者定义了 **task-conditioned tool-output pruning**：输入是一个简短查询和一条原始工具观测；输出是原文中的一个或多个连续片段。
- 他们构建了一个包含 **11,477 个样本**、覆盖 **27 种工具类型** 的数据集，其中包括 **9,205 个源自 SWE-bench 的样本**、**1,697 个合成正例** 和 **575 个合成负例**；测试集包含 **618 个人工审核样本**。
- 标注通过一个两阶段教师流水线生成，使用 **openai/gpt-oss-120b** 编写聚焦的提取查询并选出最小支持片段；发布的标注可映射回原始文本，因此目标保持逐字不变。
- 模型是用 **LoRA** 微调的 **Qwen 3.5 2B**，输出格式是在 `<relevant_lines>` 标签内给出提取文本。评估指标包括按行计算的 **recall**、**F1**、**exact match** 和 **compression**。
- 基线包括零样本 **Qwen 3.5 35B A3B**、**Kimi K2**、未微调的 **Qwen 3.5 2B**，以及启发式方法 **BM25**、**First-N**、**Last-N** 和 **Random**。

## 结果
- 在保留出的 **618 个样本** 测试集上，**Squeez-2B** 达到 **0.86 recall**、**0.80 precision**、**0.80 F1**、**0.79 strict F1**、**0.49 exact match** 和 **0.92 compression**，也就是去掉了 **92%** 的输入 token。
- 与主要的零样本大模型基线 **Qwen 3.5 35B A3B** 相比，Squeez-2B 在同样 **0.92 compression** 下，将 **recall 从 0.75 提高到 0.86**，将 **F1 从 0.73 提高到 0.80**。
- 与未微调的 **Qwen 3.5 2B** 基础模型相比，Squeez-2B 将 **recall 从 0.53 提高到 0.86**，将 **F1 从 0.55 提高到 0.80**。
- 启发式剪枝的效果弱得多：**BM25** 在 **0.90 compression** 下只有 **0.22 recall** 和 **0.23 F1**；**First-N** 的 **recall** 为 **0.14**；**Last-N** 的 **recall** 为 **0.05**。
- 在 **59 个负例测试样本** 上，Squeez-2B 有 **80%** 的情况下返回空输出，而 **Qwen 35B** 只有 **7%**，说明它在不存在相关证据的情况下处理得更好。
- 论文没有报告端到端的代理任务完成率提升，因此它的主要结论是在一个新的编码代理工具输出基准上，在高压缩率下仍能较好地保留证据。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.04979v1](http://arxiv.org/abs/2604.04979v1)
