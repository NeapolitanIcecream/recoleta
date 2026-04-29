---
source: arxiv
url: http://arxiv.org/abs/2604.23361v1
published_at: '2026-04-25T16:05:30'
authors:
- "Jelena Ili\u0107 Vuli\u0107evi\u0107"
topics:
- local-llms
- bug-detection
- python-code
- code-intelligence
- offline-inference
relevance_score: 0.87
run_id: materialize-outputs
language_code: zh-CN
---

# An Empirical Evaluation of Locally Deployed LLMs for Bug Detection in Python Code

## Summary
## 摘要
这篇论文测试了在完全离线状态下运行的小型开放权重 LLM 是否能找出真实的 Python 缺陷。在 BugsInPy 的 349 个案例上，LLaMA 3.2 和 Mistral 的准确率约为 43% 到 45%；此外还有很多回答能指出问题大致所在的区域，但没能给出精确修复点。

## 问题
- 论文研究的是本地部署 LLM 的缺陷检测。在隐私、成本或网络连接受限的情况下，云端模型往往无法使用。
- 既有工作更多集中在云端系统、合成任务或更窄的缺陷类别上，因此，离线消费者硬件上的模型在真实 Python 缺陷上的实际价值此前并不清楚。
- 这对代码智能和开发者工具很重要，因为团队可能希望在专有代码上做缺陷分析，而不把源代码发送到外部服务。

## 方法
- 作者评估了两个本地模型：**LLaMA 3.2 8B** 和 **Mistral 7B**。它们通过 **Ollama** 在一台 **14 英寸 MacBook Pro（2021，M1 Pro，16GB RAM）** 上完全离线运行，并使用了 **4-bit quantization**。
- 他们使用 **BugsInPy** 基准，在排除源代码获取失败或函数提取失败的案例后，成功处理了来自 **17 个 Python 项目** 的 **501 个缺陷中的 349 个**。
- 对每个缺陷，研究者提取包含缺陷行的外围函数，并给模型一个 **zero-shot prompt**：“Here is a Python function. It contains a bug. Find the bug and explain how to fix it.”
- 他们使用一种基于修复中新增 token 的自动关键词方法来给自由文本回答打分，将输出标记为 **correct**、**partial** 或 **wrong**；对 **50 个回答** 的人工检查显示，人工结果与自动标注高度一致。
- 他们还按项目和 **9 类缺陷类型** 分析结果，例如 Null/None checks、return value bugs、indexing，以及复杂的多组件缺陷。

## 结果
- 总体准确率方面，**LLaMA 3.2** 为 **43.3%**（**151/349 correct，171 partial，27 wrong**），**Mistral** 为 **44.4%**（**155/349 correct，161 partial，33 wrong**）。
- 两个模型之间的差距很小：**McNemar’s test p = 0.68**。配对结果为 **126 both-correct**、**169 both-wrong**、**25 LLaMA-only correct** 和 **29 Mistral-only correct**。论文据此认为两者没有显著差异。
- 不同项目上的准确率差异很大：例如两者在 **PySnooper** 上都是 **100%**，在 **black** 上为 **73.7% / 68.4%**，在 **fastapi** 上为 **69.2% / 61.5%**，在 **pandas** 上为 **38.5% / 44.8%**，在 **tqdm** 上为 **0.0% / 14.3%**，顺序为 LLaMA/Mistral。
- 按缺陷类型看，两个模型在 **Null/None Check** 缺陷上表现最好（**LLaMA 59.5%，Mistral 60.8%**），在 **Return Value** 缺陷上也较好（两者都是 **51.3%**）。它们在 **Type Conversion** 上表现很差（两者都是 **0.0%**），在 **Other/Complex** 缺陷上也较弱（**LLaMA 21.7%，Mistral 16.7%**）。
- 在消费者硬件上进行推理是可行的：**LLaMA 3.2** 的平均响应时间约为 **7 秒**，**Mistral** 约为 **13 秒**，总运行时间分别约为 **40 分钟** 和 **75 分钟**。
- 论文最强的实际结论是：本地模型可以捕捉到相当一部分真实缺陷，并且常常能缩小排查范围；但当缺陷依赖更广的程序上下文或跨函数行为时，精确定位仍然较弱。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23361v1](http://arxiv.org/abs/2604.23361v1)
