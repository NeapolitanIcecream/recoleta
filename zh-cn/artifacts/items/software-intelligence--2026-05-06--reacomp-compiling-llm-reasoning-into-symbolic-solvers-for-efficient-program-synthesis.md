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
ReaComp把少量 LLM 推理轨迹转成可复用的符号程序合成器，用于基于示例的程序合成和逻辑规则合成。生成的求解器在测试时不需要 LLM 调用，能处理很多任务，并在困难样例上提升 LLM 兜底时的准确率和 token 用量。

## 问题
- LLM 可以解决程序合成任务，但困难实例需要很多采样或迭代步骤，这会提高 token 成本，也增加失败风险。
- 对于无结构的 LLM 搜索，长的组合程序很难处理；论文报告说，随着解的长度增加，会出现循环、反复尝试和更低的准确率。
- 这会影响代码智能和自动化软件生产，因为当需要解决很多相似的合成任务时，重复做 LLM 推理的成本很高。

## 方法
- ReaComp 先在每个基准上收集大约 100 条 LLM 推理轨迹，并在任务难度以及成功或失败之间保持平衡。
- 一个编码代理，例如 Claude Code 或带 OpenHands 的 Qwen，读取这些轨迹，并编写一个基于受限 DSL 的独立 Python 符号求解器。
- 求解器直接搜索程序候选，并用验证器挑出与示例匹配的候选。
- 在测试时，先运行符号求解器。如果它解出任务，就不需要 LLM 调用；否则系统回退到 LLM Best-of-K 或直接反馈搜索。
- 构建成本只付一次，然后可以在很多任务上复用。

## 结果
- 在 PBEBench-Lite 上，All Symbolic 求解器集成的准确率达到 91.3%，测试时 LLM token 为 0；相比之下，BoK 的准确率是 93.8%，但用了 68.0M token。BoK + All Symbolic 达到 93.9%，用了 43.5M token，token 用量减少 36%。
- 在 PBEBench-Hard 上，All Symbolic 的准确率达到 84.7%，测试时 LLM token 为 0，比 BoK 的 68.4% 高出 16.3 个百分点。BoK + All Symbolic 达到 85.8%，用了 71.6M token，而 BoK 用了 332.1M token，减少 78%。
- 在 SLR-Bench 上，CC 符号求解器在 hard-tier 上的准确率是 46.8%，测试时 LLM token 为 0；论文报告的 o3 是 45%，GPT-5 是 46%。DF + CC 的 hard-tier 准确率达到 58.0%，整体准确率达到 86.6%。
- 最好的 SLR 混合方案 DF + CC + QO 的整体准确率达到 86.7%，用了 138.8M token，成本为 $16.19；论文报告的 o3 是 77.8%，成本为 $207.24。
- 不使用推理轨迹的消融结果在 PBEBench-Hard 上差很多：使用 CoT 轨迹时准确率是 74.7%，没有 CoT 轨迹时降到 24.8%。
- 在历史语言学迁移案例中，求解器集成在 3,077 对原始语言-后代语言对上零样本达到 80.1% 准确率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.05485v1](https://arxiv.org/abs/2605.05485v1)
