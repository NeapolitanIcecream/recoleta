---
source: arxiv
url: https://arxiv.org/abs/2605.30054v1
published_at: '2026-05-28T15:05:53'
authors:
- Boqi Chen
- "Jos\xE9 Antonio Hern\xE1ndez L\xF3pez"
- Aren A. Babikian
topics:
- constrained-decoding
- semantic-validation
- code-generation
- partial-models
- software-engineering
- llm-decoding
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# Projectional Decoding: Towards Semantic-Aware LLM Generation

## Summary
## 摘要
projectional decoding 在 token 流旁保留一个部分图模型，让 LLM 在生成过程中就拒绝语义无效的软件制品。论文称，在 CLEVR DSL 程序生成任务上取得了初步提升，Qwen3 系列模型的语义有效率升至 73.33%–79.67%。

## 问题
- LLM 可以生成语法上正确、但仍然违反类型规则、不变量、数据流约束、契约或领域规则的软件制品。
- 生成后修复在输出过于破碎、无法解释时会失效，而且在解码过程中没有保证。
- 这会影响代码生成、DSL 生成、建模、API 使用以及其他软件工程任务，因为无效制品会破坏执行或集成。

## 方法
- 该方法在解码时维护两个相连状态：文本前缀和所生成制品的部分图模型。
- 每个候选 token 先通过语法检查，再按照元模型和约束更新部分模型。
- 部分模型记录确定、可能、缺失和错误元素，让解码器可以推理不完整制品。
- 会在采样前屏蔽会造成约束违反的 token；其余 token 让生成继续沿着仍可能产生有效制品的路径前进。
- 论文把这一机制与用于结构约束的图模式匹配和用于行为约束的抽象解释联系起来。

## 结果
- 在使用 Qwen3-4B 进行 CLEVR 程序生成时，语义有效率从无引导的 4.33% 和仅语法解码的 48.67% 提升到 projectional decoding 的 73.67%。
- 在 Qwen3-8B 上，语义有效率从无引导的 60.33% 和仅语法解码的 61.00% 提升到 projectional decoding 的 79.67%。
- 在 Qwen3-14B 上，语义有效率从无引导的 55.44% 和仅语法解码的 58.33% 提升到 projectional decoding 的 73.33%。
- 使用 projectional decoding 时，任务准确率在 4B、8B 和 14B 上分别为 36.00%、40.00% 和 37.33%；它在三种情况下都优于仅语法解码，并在 3 次中的 2 次中优于无引导。
- 相比无引导，平均生成时开销在 Qwen3-4B 上为 1.1x，在 Qwen3-8B 上为 1.5x，在 Qwen3-14B 上为 1.1x。
- 评估仍然是初步结果，只使用了一个 DSL 基准；该方法仍未达到 100% 语义有效率，因为解码可能到达没有有效完成方式的前缀。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.30054v1](https://arxiv.org/abs/2605.30054v1)
