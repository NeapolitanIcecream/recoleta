---
source: arxiv
url: https://arxiv.org/abs/2605.21850v1
published_at: '2026-05-21T00:47:03'
authors:
- Qisheng Su
- Zhen Fang
- Shiting Huang
- Yu Zeng
- Yiming Zhao
- Kou Shi
- Ziao Zhang
- Lin Chen
- Zehui Chen
- Lijun Wu
- Feng Zhao
topics:
- long-context-training
- agent-trajectories
- software-engineering-agents
- code-intelligence
- supervised-fine-tuning
- tool-use-data
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# ACC: Compiling Agent Trajectories for Long-Context Training

## Summary
## 总结
ACC 将完整的 agent 运行轨迹转换为长上下文 QA 训练样本，让模型学会根据分散在工具输出中的证据作答。在 Qwen3-30B-A3B-Thinking 上，它提升了 MRCR 和 GraphWalks，同时让通用基准基本保持不变。

## 问题
- 长上下文 LLM 训练通常需要整理好的长文档或合成上下文，这既耗时，也可能错过真实问题求解过程中形成的依赖关系。
- Agent 轨迹在多次工具调用中包含有用证据，但标准 agent SFT 会屏蔽工具响应，主要训练下一步动作预测。
- 这对搜索、软件工程和 SQL agent 都很重要，因为最终答案往往依赖分散在多个轮次里的证据。

## 方法
- 收集来自 Search、SWE 和 SQL agent 的已验证答案轨迹：共 10,802 条，其中 Search 3,369 条，SWE 4,368 条，SQL 3,065 条。
- 从每条轨迹中提取证据片段：Search 包括访问过的页面和干扰项，SWE 包括与补丁相关的文件和检查过的文件，SQL 包括查询过的表。
- 将这些证据打乱后拼接成一个上下文，长度上限为 131,072 tokens，然后把原始问题、整理后的上下文和最终答案配对。
- 使用 DeepSeek-V3.2-Thinking 生成推理轨迹，并只保留能导向正确答案的轨迹；报告的通过率在 Search 上接近 100%，在 SQL 上接近 50%，在 SWE 上接近 10%。
- 用交叉熵损失对 Qwen3-30B-A3B-Thinking 进行 4 个 epoch 的微调，global batch size 为 16，学习率为 1e-5。

## 结果
- MRCR 总分从 Qwen3-30B-A3B-Thinking 基线的 50.19 提升到 68.28，增加 18.09；2-needle 从 61.84 提升到 76.90，4-needle 从 38.41 提升到 59.57。
- GraphWalks 总体 precision 从 69.92 提升到 77.51，增加 7.59；Parents 从 71.19 提升到 81.50，BFS 从 68.47 提升到 72.95。
- 经过 ACC 训练的 Qwen3-30B-A3B 在这两个长程测试上略高于 Qwen3-235B-A22B-Thinking：MRCR 为 68.28 对 67.51，GraphWalks 为 77.51 对 76.63。
- 通用基准分数与基线接近或更高：GPQA-Diamond 70.20 对 67.71，MMLU-Pro 76.00 对 74.50，AIME’24 90.00 对 90.00，AIME’25 90.00 对 86.67，IFEval 86.14 对 86.69。
- 编译后的训练样本长度覆盖 2K 到 128K tokens，微调时使用的序列长度为 131,072 tokens。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.21850v1](https://arxiv.org/abs/2605.21850v1)
