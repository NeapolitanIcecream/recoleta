---
source: hn
url: https://jacobxli.com/blog/2026/machine-studying/
published_at: '2026-06-21T23:26:12'
authors:
- meander_water
topics:
- machine-studying
- agent-evaluation
- code-intelligence
- rag
- continual-learning
- software-agents
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Machine Studying

## Summary
## 摘要
Machine Studying 定义了一种测试：智能体能否在看到考试之前，把新的文档语料转化为可用的专业能力。论文加入了 StudyBench，并报告了早期证据：搜索、长上下文和简单微调都不能稳定地产生这种专业能力。

## 问题
- 智能体在训练后常常会遇到新的代码库、论文、手册和私有语料，而特定任务的 RL 数据或标注样例可能不可用。
- RAG 和长上下文搜索让智能体能够访问文档，但不能保证智能体知道该搜索什么、该怀疑哪些先验，或如何高效使用找到的证据。
- 这对软件智能体和研究智能体很重要，因为过时或缺失的领域知识会导致错误的 API、糟糕的配置选择和薄弱的文献覆盖，即使正确证据已经存在于语料中。

## 方法
- 论文把专业能力定义为随着推理 token 增加而形成的性能曲线下的加权面积。专业能力越高，表示能用更低的 token 成本给出更好的答案；测试时仍可访问语料。
- 学习算法可以只使用语料，在下游任务已知之前，改变模型权重、提示、工具、索引、笔记或其他 harness 状态。
- StudyBench 将一个语料与一套隐藏考试配对，覆盖三个领域：DSPy 代码、OpenClaw 代码和近期机器学习文献。
- 智能体在带有 grep、glob 和 read_file 工具的 ReAct harness 中运行。评估比较直接回答、最多 5 轮工具迭代、最多 20 轮工具迭代，以及强制 20 轮迭代。
- 论文测试了早期基线，包括用原始语料文本通过 LoRA 做持续预训练，以及用生成的问答对做合成监督微调。

## 结果
- StudyBench 目前包含 3 个任务：Studying-DSPy，含 30 道编程题；Studying-OpenClaw，含 20 道题；Studying-Literature，基于约 50,000 篇 2018 到 2025 年的 ICLR、CVPR、ICML 和 NeurIPS 全文论文构建。
- 专业能力指标使用对数 token 预算，其中 x=0 等于生成 3k token，每 +1 表示 token 增加 10 倍。论文使用指数衰减 w(x)=(ln 10)10^-x，因此计算量每翻倍，预算权重就减半。
- 在一个示例中，5k、10k、20k 和 100k token 预算下的得分分别为 10%、20%、30% 和 40%，估计专业能力约为 10.8%。实测预算权重之和为 0.60，因此即使这些实测预算下都拿到满分，专业能力上限也只有 60%，因为低于 5k 的区域记为零。
- GPT-5.4-mini 在 DSPy 上的每个已测试推理预算下都超过 GPT-5.1；DSPy 是一个在 2024 年后变得流行的库。在 OpenClaw 上，这个优势消失了；OpenClaw 晚于两个模型的知识截止时间，即使用更多搜索，两个模型也都只略高于 10%。
- 对于学习前的 Qwen3.5-9B 在 DSPy 上的表现，强制完整 20 轮搜索迭代把宽松评分从 9.6 提高到 29.4，约为 3.1 倍增益。这说明如果没有更好的学习行为，可触达的证据常常仍未被使用。
- 报告中的学习基线仍是初步结果。摘录称，简单的自监督或监督适配对原始模型的提升往往低于预期，并且还不能让智能体专业能力稳定跃升。

## Problem

## Approach

## Results

## Link
- [https://jacobxli.com/blog/2026/machine-studying/](https://jacobxli.com/blog/2026/machine-studying/)
