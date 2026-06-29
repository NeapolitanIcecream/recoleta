---
source: arxiv
url: https://arxiv.org/abs/2606.09577v1
published_at: '2026-06-08T14:52:43'
authors:
- Yuling Shi
- Caiqi Zhang
- Yuexian Li
- Haopeng Wang
- Yeheng Chen
- Nigel Collier
- Xiaodong Gu
topics:
- code-generation
- uncertainty-estimation
- code-intelligence
- software-foundation-models
- self-generated-tests
- llm-calibration
relevance_score: 0.92
run_id: materialize-outputs
language_code: zh-CN
---

# Code Is More Than Text: Uncertainty Estimation for Code Generation

## Summary
## 摘要
本文提出一种面向代码生成的、代码特定的不确定性估计方法。它结合了 token 级熵峰值、采样得到的伪代码计划之间的一致性，以及自生成测试的通过率，用来预测生成的代码是否能通过隐藏测试。

## 问题
- LLM 代码生成器会产出看起来合理、但实际上错误的程序，这会给 IDE 助手、编码代理和多步骤软件流水线带来风险。
- 现有的不确定性方法大多来自自然语言生成，把代码当作 token 序列处理，忽略了代码的特性，比如单个 token 就能导致程序失效、算法意图和实现不一致、以及代码可执行。
- 更好的不确定性分数可以把输出转给人工复核、触发重试，或在自动化软件生产中拦截低置信度代码。

## 方法
- 词法信号先计算生成程序的 token 熵，再对 Top-K 个最不确定位置取平均。论文使用 K=5，这样少量高风险 token 的影响不会被文件其余部分稀释。
- 算法信号采样 N=10 个自然语言解题计划，用考虑步骤的 ROUGE-L 做比较；当这些计划彼此不一致时，就赋予更高的不确定性。
- 功能信号生成 M=10 个测试，在沙箱里运行候选程序，并把自测失败的比例作为不确定性。
- 最终分数先对这三个信号做秩归一化，再用固定权重组合：词法 0.2，功能 0.4，算法 0.4。

## 结果
- 在五个代码 LLM 和四个基准上，这个三轴集成方法把平均 AUROC 从最强的自然语言迁移基线的 0.696 提升到 0.776，提高了 8.1 个百分点。
- 在 Qwen3-14B 上，这个集成方法在 APPS-Intro、APPS-Interview、HumanEval 和 MBPP 上达到 0.800 的平均 AUROC 和 0.835 的平均 PRAUC。
- 在 Qwen3-14B 上，Top-5 熵的平均 AUROC 达到 0.728，与最强的多轮自然语言基线 Consistency VR 的 0.728 持平，而且成本低 3 倍以上。
- 在 Qwen3-14B 的 HumanEval 上，Top-K 熵的墙钟时间是每题 2.29 秒，生成测试是 3.06 秒，伪代码一致性是 6.55 秒，Consistency VR 是 7.10 秒。
- 在表 1 的模型上，这个集成方法对 DeepSeek-Coder-V2 的平均 AUROC 达到 0.770，对 Devstral-Small-2505 达到 0.791。
- 按 token 拆分后，代码 token 熵有用，而注释 token 熵有害：只用代码 token 时 AUROC 为 0.716，只用注释 token 时 AUROC 为 0.375。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.09577v1](https://arxiv.org/abs/2606.09577v1)
