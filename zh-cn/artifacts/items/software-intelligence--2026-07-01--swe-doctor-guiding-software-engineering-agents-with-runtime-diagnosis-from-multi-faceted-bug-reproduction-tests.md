---
source: arxiv
url: https://arxiv.org/abs/2607.00990v1
published_at: '2026-07-01T14:27:12'
authors:
- Yaoqi Guo
- Yang Liu
- Jie M. Zhang
- Yun Ma
- Yiling Lou
- Zhenpeng Chen
topics:
- software-agents
- code-intelligence
- bug-fixing
- swe-bench
- runtime-debugging
- test-generation
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# SWE-Doctor: Guiding Software Engineering Agents with Runtime Diagnosis from Multi-Faceted Bug Reproduction Tests

## Summary
## 摘要
SWE-Doctor 是一个修复 bug 的代理，它在生成补丁前，把生成的复现测试用作调试探针。它通过针对多个 issue 需求生成测试，并将测试执行结果转换为运行时诊断记录，报告了更高的 SWE-bench 解决率。

## 问题
- LLM 软件代理通常只在生成补丁后使用 bug 复现测试，因此测试无法帮助识别需要修改的代码。
- 直接让生成的 BRT 通过可能损害补丁生成：在一项包含 100 个 issue 的 SWE-bench Verified 研究中，mini-SWE-agent 解决了 74 个 issue，而加入 e-Otter++、Issue2Test 和 AssertFlip 的变体分别解决了 71、71 和 73 个 issue。
- 单个 fail-to-pass 测试可能只覆盖一种行为，并导致不完整修复；fail-to-fail 测试可能把代理引向无效目标。

## 方法
- 从 issue 报告中提取预期行为，将每个行为视为一个独立方面，并为每个方面生成有针对性的 bug 复现测试。
- 使用标识符匹配和基于 LLM 的定位，为每项需求定位可能相关的文件和函数，然后运行“生成-执行-改进”循环，直到测试因预期行为而失败。
- 在调试器下运行生成的测试，并创建诊断记录，其中包含疑似故障位置、失败症状、传播路径、运行时值、补丁影响说明和建议修复。
- 在生成补丁前，将需求、定位数据和诊断记录输入 mini-SWE-agent，然后在提交前运行完整性检查。

## 结果
- 主要评估覆盖 SWE-bench Verified 和 SWE-bench Pro 上的 Python bug 修复任务，使用 5 个 LLM 后端，共形成 10 个 LLM-benchmark 组合。
- SWE-Doctor 报告在 SWE-bench Verified 上的平均解决率为 75.7%，在 SWE-bench Pro 上为 59.4%。
- 在 SWE-bench Pro 上，它相比 mini-SWE-agent 和 live-SWE-agent 将平均解决率提高了 8.0 到 8.9 个百分点。
- 它在全部 10 个 LLM-benchmark 组合中都超过了两个基线代理。
- 在包含 100 个 issue 的初步研究中，e-Otter++ 使用 50 个 fail-to-pass 测试和 50 个 fail-to-fail 测试解决了 71/100 个 issue；Issue2Test 使用 42 个 fail-to-pass 测试和 58 个 fail-to-fail 测试解决了 71/100 个 issue；AssertFlip 使用 70 个 fail-to-pass 测试和 30 个 fail-to-fail 测试解决了 73/100 个 issue；原始 mini-SWE-agent 解决了 74/100 个 issue。
- 论文称，移除多方面测试生成或基于运行时的诊断都会降低解决率，但摘录没有提供消融实验的具体比率。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2607.00990v1](https://arxiv.org/abs/2607.00990v1)
