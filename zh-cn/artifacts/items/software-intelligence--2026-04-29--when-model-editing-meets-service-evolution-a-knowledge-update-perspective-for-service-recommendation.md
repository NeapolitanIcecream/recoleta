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
EvoRec 会在 API 和服务变化时更新基于 LLM 的服务推荐器，并约束解码过程，使模型只输出有效且不重复的服务。

## 问题
- 服务仓库会因新增服务、API 更新、弃用服务和版本变化而改变，因此用旧数据训练的推荐器可能返回过时或无效的服务流水线。
- LLM 可以把自然语言需求或代码上下文映射到服务序列，但也可能幻觉出当前目录中不存在的服务名称或调用。
- 当服务事实频繁变化时，完整重新训练或频繁微调的成本很高。

## 方法
- EvoRec 使用 ROME 风格的先定位后编辑模型编辑方法，在选定的 Transformer 前馈层中插入或更新服务事实。
- 每次编辑都会把一个需求模式或代码上下文键映射到更新后的目标服务值，并使用目标服务的交叉熵和 KL 散度来保留无关行为。
- 检索增强提示会在生成前从服务语料库提供相关服务示例。
- Trie 引导的有限自动机约束解码会屏蔽无效的下一个 token，使生成的名称符合服务目录和有效列表结构。
- 解码器会跟踪已使用的服务 ID，并且只阻断剩余子树中没有未使用服务的分支，从而在允许共享前缀的同时防止重复。

## 结果
- 论文声称，在真实服务数据集上，相比现有基线，Recall@5 的平均相对提升为 25.9%。
- 根据摘录，在服务演化场景下，EvoRec 比模型微调方法高出 22.3%。
- 摘录称 EvoRec 在保持低维护成本的同时提高了推荐准确性和适应性，但没有提供数据集名称、Recall@5 绝对值、模型规模或完整基线表。
- 最具体的有效性主张是，FA 和 Trie 解码会在生成期间强制执行有效服务名称、有效分隔符/结束 token，以及服务级去重。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2604.26686v1](https://arxiv.org/abs/2604.26686v1)
