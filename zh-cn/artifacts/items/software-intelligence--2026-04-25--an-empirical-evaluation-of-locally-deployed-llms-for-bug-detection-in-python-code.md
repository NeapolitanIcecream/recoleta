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
这篇论文测试了完全离线运行的小型开权重 LLM 是否能发现真实的 Python bug。在 349 个 BugsInPy 案例上，LLaMA 3.2 和 Mistral 的准确率约为 43% 到 45%，另外还有不少回答能指出问题区域，但没有给出准确修复。

## 问题
- 这篇论文研究本地部署的 LLM 做 bug 检测。云模型常常因为隐私、成本或需要联网而不适用。
- 以往工作更多关注云端系统、合成任务，或更窄的 bug 类型，所以离线消费级硬件模型对真实 Python bug 的实际价值还不清楚。
- 这对代码智能和开发工具很重要，因为团队可能想在专有代码上做 bug 分析，但不想把源代码发给外部服务。

## 方法
- 作者评估了两个本地模型，**LLaMA 3.2 8B** 和 **Mistral 7B**，用 **Ollama** 在一台 **MacBook Pro 14 英寸（2021）** 上运行，配置是 **M1 Pro 和 16GB RAM**，完全离线，并使用 **4-bit 量化**。
- 他们使用 **BugsInPy** 基准，在排除源代码获取或函数提取失败的案例后，成功处理了来自 **17 个 Python 项目** 的 **349 个 / 501 个 bug**。
- 对每个 bug，他们提取 buggy 代码行外层的函数，并给模型一个 **zero-shot** 提示：“这里有一个 Python 函数。它包含一个 bug。找出这个 bug，并解释如何修复。”
- 他们用一种自动关键词方法给自由文本答案打分，这种方法基于修复时新增的 token，把输出标为 **correct**、**partial** 或 **wrong**；对 **50 条回复** 的人工检查显示，人工判断和自动标签高度一致。
- 他们还按项目和 **9 种 bug 类型** 拆分结果，例如 Null/None 检查、返回值 bug、索引问题，以及复杂的多组件 bug。

## 结果
- 总体准确率上，**LLaMA 3.2** 为 **43.3%**（**151/349 correct, 171 partial, 27 wrong**），**Mistral** 为 **44.4%**（**155/349 correct, 161 partial, 33 wrong**）。
- 两个模型差距很小：**McNemar’s test p = 0.68**，配对结果是 **126 both-correct**、**169 both-wrong**、**25 LLaMA-only correct**、**29 Mistral-only correct**。论文把这视为没有显著差异。
- 不同项目之间的准确率差异很大：例如 **PySnooper** 两个模型都是 **100%**，**black** 为 **73.7% / 68.4%**，**fastapi** 为 **69.2% / 61.5%**，**pandas** 为 **38.5% / 44.8%**，**tqdm** 为 **0.0% / 14.3%**，对应 LLaMA/Mistral。
- 按 bug 类型看，两个模型在 **Null/None Check** bug 上最好（**59.5% LLaMA, 60.8% Mistral**），在 **Return Value** bug 上也表现较好（两者都是 **51.3%**）。它们在 **Type Conversion** 上表现很差（两者都是 **0.0%**），在 **Other/Complex** bug 上也不理想（**21.7% LLaMA, 16.7% Mistral**）。
- 在消费级硬件上推理是可行的：**LLaMA 3.2** 平均响应时间约 **7 秒**，**Mistral** 约 **13 秒**，总运行时间分别约 **40 分钟** 和 **75 分钟**。
- 最强的实际结论是，本地模型能捕捉到相当一部分真实 bug，也经常能缩小排查范围，但当 bug 依赖更广的程序上下文或跨函数行为时，精确定位仍然很弱。

## Problem

## Approach

## Results

## Link
- [http://arxiv.org/abs/2604.23361v1](http://arxiv.org/abs/2604.23361v1)
