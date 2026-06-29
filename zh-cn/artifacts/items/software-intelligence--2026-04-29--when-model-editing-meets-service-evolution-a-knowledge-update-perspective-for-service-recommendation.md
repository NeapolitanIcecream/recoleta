---
source: arxiv
url: https://arxiv.org/abs/2604.26686v1
published_at: '2026-04-29T13:51:56'
authors:
- Guodong Fan
- Cuiyun Gao
- Chun Yong Chong
- Lu Zhang
- Jing Li
- Jinglin Zhang
- Shizhan Chen
topics:
- service-recommendation
- model-editing
- llm-agents
- constrained-decoding
- code-intelligence
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# When Model Editing Meets Service Evolution: A Knowledge-Update Perspective for Service Recommendation

## Summary
## 摘要
EvoRec 会在 API 和服务发生变化时更新基于 LLM 的服务推荐器，然后用受限解码让模型只输出有效、无重复的服务。

## 问题
- 服务仓库会随着新服务、API 更新、服务弃用和版本变化而变化，所以在旧数据上训练的推荐器会返回过时或无效的服务流水线。
- LLM 可以把自然语言需求或代码上下文映射到服务序列，但它们可能会幻觉出当前目录中不存在的服务名或调用。
- 当服务事实经常变化时，完全重训或频繁微调的成本很高。

## 方法
- EvoRec 使用类似 ROME 的 locate-then-edit 模型编辑，把服务事实写入选定的 Transformer 前馈层，或更新这些事实。
- 每次编辑都会把需求模式或代码上下文键映射到更新后的目标服务值，并用交叉熵优化目标服务，用 KL 散度保留无关行为。
- 检索增强提示会在生成前从服务语料库中提供相关的服务示例。
- 由 Trie 引导的有限自动机受限解码会屏蔽无效的下一个 token，使生成的名称符合服务目录和有效列表结构。
- 解码器会跟踪已使用的服务 ID，只阻止那些剩余子树中没有未使用服务的分支，这样既能防止重复，也能保留共享前缀。

## 结果
- 论文声称，在真实世界服务数据集上，EvoRec 的 Recall@5 平均相对提升了 25.9%，优于现有基线。
- 根据摘要，在服务持续演化的场景下，EvoRec 比模型微调方法高 22.3%。
- 摘要还说，EvoRec 在保持维护成本较低的同时提高了推荐准确率和适应性，但没有给出数据集名称、Recall@5 的绝对值、模型规模或完整的基线表。
- 最明确的有效性结论是，FA 和 Trie 解码在生成过程中强制服务名有效、分隔符和结束 token 有效，并在服务层面去重。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26686v1](https://arxiv.org/abs/2604.26686v1)
