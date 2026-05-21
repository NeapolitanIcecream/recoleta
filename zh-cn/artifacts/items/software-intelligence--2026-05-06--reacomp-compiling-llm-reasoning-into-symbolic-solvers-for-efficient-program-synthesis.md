---
source: arxiv
url: https://arxiv.org/abs/2605.05485v1
published_at: '2026-05-06T22:08:17'
authors:
- Atharva Naik
- Yash Mathur
- Prakam
- Carolyn Rose
- David Mortensen
topics:
- program-synthesis
- code-intelligence
- llm-reasoning
- symbolic-solvers
- neuro-symbolic-ai
- test-time-efficiency
relevance_score: 0.91
run_id: materialize-outputs
language_code: zh-CN
---

# ReaComp: Compiling LLM Reasoning into Symbolic Solvers for Efficient Program Synthesis

## Summary
## 摘要
ReaComp 将少量 LLM 推理轨迹转换为可复用的符号程序合成器，用于基于示例编程和逻辑规则合成。生成的求解器在测试时无需调用 LLM 就能解决许多任务，并在困难样例上提高 LLM 回退方案的准确率，同时减少 token 用量。

## 问题
- LLM 可以解决程序合成任务，但困难样例需要大量采样或多轮改进，这会增加 token 成本和失败风险。
- 长组合程序对无结构的 LLM 搜索较难；论文报告称，随着解法长度增加，会出现循环、重复尝试和准确率下降。
- 这影响代码智能和自动化软件生产，因为在需要解决大量相似合成任务时，重复进行 LLM 推理成本很高。

## 方法
- ReaComp 先为每个基准收集约 100 条 LLM 推理轨迹，并按任务难度以及成功或失败进行平衡。
- Claude Code 或结合 OpenHands 的 Qwen 等编码智能体读取这些轨迹，并在受限 DSL 上编写独立的 Python 符号求解器。
- 求解器直接搜索候选程序，并使用验证器选择与示例匹配的候选项。
- 测试时先运行符号求解器。如果它解决了任务，就不调用 LLM；否则系统回退到 LLM Best-of-K 或直接反馈搜索。
- 构建成本只支付一次，之后可在许多任务中复用。

## 结果
- 在 PBEBench-Lite 上，All Symbolic 求解器集成在测试时使用 0 个 LLM token，准确率达到 91.3%；BoK 使用 68.0M token，准确率为 93.8%。BoK + All Symbolic 使用 43.5M token，准确率达到 93.9%，token 减少 36%。
- 在 PBEBench-Hard 上，All Symbolic 在测试时使用 0 个 LLM token，准确率达到 84.7%，比准确率为 68.4% 的 BoK 高 16.3 个百分点。BoK + All Symbolic 准确率达到 85.8%，使用 71.6M token；BoK 使用 332.1M token，减少幅度为 78%。
- 在 SLR-Bench 上，CC 符号求解器在测试时使用 0 个 LLM token，hard-tier 准确率为 46.8%；报告中的 o3 为 45%，GPT-5 为 46%。DF + CC 的 hard-tier 准确率达到 58.0%，总体准确率达到 86.6%。
- 最佳 SLR 混合方案 DF + CC + QO 使用 138.8M token，成本为 $16.19，总体准确率达到 86.7%；报告中的 o3 为 77.8%，成本为 $207.24。
- 无推理轨迹消融在 PBEBench-Hard 上差很多：有 CoT 轨迹时准确率为 74.7%，没有 CoT 轨迹时降至 24.8%。
- 在历史语言学迁移案例中，求解器并集在 3,077 对原始语-后代语言配对上以零样本方式达到 80.1% 准确率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05485v1](https://arxiv.org/abs/2605.05485v1)
