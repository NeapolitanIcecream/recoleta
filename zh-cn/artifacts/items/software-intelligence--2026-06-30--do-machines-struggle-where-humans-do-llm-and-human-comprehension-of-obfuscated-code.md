---
source: arxiv
url: https://arxiv.org/abs/2606.31725v1
published_at: '2026-06-30T14:26:46'
authors:
- Jack Le
- Anh H. N. Nguyen
- Tien N. Nguyen
topics:
- code-intelligence
- llm-evaluation
- obfuscated-code
- program-comprehension
- human-ai-alignment
- software-security
relevance_score: 0.78
run_id: materialize-outputs
language_code: zh-CN
---

# Do Machines Struggle Where Humans Do? LLM and Human Comprehension of Obfuscated Code

## Summary
## 摘要
本文测试 LLM 是否会在与人类相同的位置难以理解混淆代码。推理调优模型与人类任务难度更一致，代码模型和指令调优模型的一致性较弱。

## 问题
- 代码混淆会保留行为，同时改变名称和控制流，因此可用于测试模型是在跟踪程序逻辑，还是依赖表层线索。
- 标准代码基准可能掩盖脆弱的代码理解能力，因为熟悉的标识符、惯用写法和控制流形态可能承载了大部分答案信息。
- 这关系到代码智能和软件安全：如果代理误读混淆代码，可能在审计、逆向工程、恶意软件分析或受保护代码维护中给出错误答案。

## 方法
- 研究复用了 Nguyen 等人的人类数据集：50 名本科程序员、20 个函数级输出预测任务、Python 和 JavaScript，以及从 L0 到 L3 的五个混淆层级。
- 研究加入了数据集 B，其中包含来自 HumanEval-X、CruxEval-X 和 LeetCode 的 250 个代码片段，每个片段都按相同五个层级生成实例。
- 研究在精确输出预测任务上评估了 Llama、Qwen、DeepSeek、Phi、SmolLM、CodeLlama 和 DeepSeek-Coder 的多个变体。
- 混淆层级包括标识符重命名、对抗性重命名、控制流扁平化，以及重命名与控制流扁平化的组合。
- 分析使用 Schulte 的 Block Model，将失败定位到 atom、block、relational 和 macro 层级，并采用准确率、思维链长度、调度器复杂度和高置信错误答案等指标。

## 结果
- 在数据集 A 上，DS-R1-Qwen-7B 是表现最强的模型：L0 准确率为 63.8%，L1 为 64.2%，L1b 为 51.8%，L2 为 57.0%，L3 为 56.2%。
- 全体参与者的人类准确率从 L0 的 40.46% 降至 L3 的 31.09%。初学者从 34.21% 降至 23.08%，中级者从 45.10% 降至 33.33%。
- 推理调优模型与人类任务难度一致：Spearman 相关性分别为 Qwen3-0.6B ρ=0.30、Phi-4 Mini ρ=0.47、SmolLM3-3B ρ=0.36、DS-R1-Qwen-7B ρ=0.37，且均为 p≤0.003。
- 代码模型和指令调优模型与人类的一致性接近零：Llama-3.1-8B ρ=0.08、CodeLlama-7B ρ=0.02、DeepSeek-Coder-6.7B ρ=0.10。
- 随着调度器复杂度上升，控制流扁平化会降低准确率：Python while-if 状态数与准确率的相关性为 r=-0.196，q=3.08×10^-23；JavaScript dispatch-call 引用的相关性为 r=-0.130，q=2.76×10^-7。
- 较低的 token 限制会明显降低强推理模型的性能；报告的比较结果为 OR=12.5，95% CI [6.4, 24.2]，p<0.001。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.31725v1](https://arxiv.org/abs/2606.31725v1)
