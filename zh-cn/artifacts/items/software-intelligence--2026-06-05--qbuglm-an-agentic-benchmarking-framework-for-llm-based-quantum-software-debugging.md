---
source: arxiv
url: https://arxiv.org/abs/2606.07314v1
published_at: '2026-06-05T14:34:46'
authors:
- An B. B. Pham
- Hoa T. Nguyen
- Muhammad Usman
topics:
- quantum-software-debugging
- llm-agents
- code-repair
- openqasm
- benchmarking
- multi-agent-systems
relevance_score: 0.86
run_id: materialize-outputs
language_code: zh-CN
---

# QBugLM: An Agentic Benchmarking Framework for LLM-based Quantum Software Debugging

## Summary
## 总结
QBugLM 是一个多智能体基准测试系统，用来测试 LLM 是否能在 OpenQASM 3.0 量子程序中发现并修复错误。它的主要发现是，反馈重试会显著提高修复成功率，而在报告的案例研究中，简单的结构化提示词比 CoT 和 ReAct 表现更好。

## 问题
- 量子错误可能在没有运行时错误的情况下给出错误答案，因此语法检查和常规调试往往会漏掉那些改变电路行为的缺陷。
- 之前针对量子代码的 LLM 基准测试主要考代码生成或特定 SDK 的代码；这篇论文测试的是 SDK 无关的 OpenQASM 3.0 的检测和修复。
- 这一点很重要，因为自动化量子编码代理需要在没有人工提示的情况下找到、修复并验证程序。

## 方法
- QBugGen 使用四类错误，在每个有效的 MQT Bench OpenQASM 3.0 电路中注入一个受控错误：废弃语法、结构性电路错误、门冗余和语义偏差。
- QBugFind 让一个 LLM 代理报告错误行和错误类别。QBugFix 让另一个 LLM 代理编辑程序。
- QBugCheck 在无噪声的 Qiskit Aer 模拟器上运行参考程序和修复后的程序，使用总变差距离比较输出分布，阈值为 εδ = 0.05，并要求门数量容差 εg = 0。
- 案例研究使用五个 5 量子比特电路：dj、grover、bv、ghz 和 wstate。它测试 Claude Sonnet 4.6 和 Qwen3 Coder Next，在结构化提示词、CoT 和 ReAct 三种提示方式下的表现。
- 每种配置允许 K = 3 次尝试，也就是 1 次初始尝试加 2 次重试，验证时使用 1,024 次 shots。

## 结果
- 在 Bernstein-Vazirani 电路上，结构化提示词给出最高的 Pass@1：Claude Sonnet 4.6 达到 97%，Qwen3 Coder Next 达到 95%。CoT 下 Claude 为 90%，Qwen3 为 45%；ReAct 下 Claude 为 95%，Qwen3 为 63%。
- 论文报告称，1 次重试会把 Pass@1 从 25% 以下提升到 80% 以上，反馈是修复成功率中测得影响最大的因素。
- 在 BV 上使用结构化提示词且不重试时，Qwen3 在语义偏差、废弃语法和门过度使用这三类错误上的 Pass@1 为 20%；Claude 在这三类上的 Pass@1 为 0%。两个模型在结构性错误上的 Pass@1 都是 60%。
- 经过 2 次重试后，Claude 在语义偏差、废弃语法和门过度使用上都达到 100%，但在结构性错误上为 80%。Qwen3 在结构性错误、废弃语法和门过度使用上都达到 100%，但在语义偏差上为 92%。论文还报告，在 2 次重试后，所有类别的 Pass@5 都是 100%。
- 在结构性错误、废弃语法和门过度使用这三类上，Qwen3 比 Claude 更便宜：每个 mutant 分别为 $0.042、$0.036 和 $0.061，而 Claude 分别为 $0.202、$0.327 和 $0.496，成本降低了 4.8 倍、9.1 倍和 8.1 倍。
- 在这三类上，Qwen3 也快 1.5 倍到 4.6 倍；在结构性错误上，它平均每个 mutant 用 28 秒，而 Claude 用 127.6 秒。在语义偏差上，Qwen3 使用大约 350,000 个 token，而 Claude 使用 91,000 个 token；Qwen3 的 Pass@1 为 92%，Claude 为 100%。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.07314v1](https://arxiv.org/abs/2606.07314v1)
