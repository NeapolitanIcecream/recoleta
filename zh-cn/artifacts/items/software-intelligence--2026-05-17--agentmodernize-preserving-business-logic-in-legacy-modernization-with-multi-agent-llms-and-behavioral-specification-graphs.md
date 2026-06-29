---
source: arxiv
url: https://arxiv.org/abs/2605.17535v1
published_at: '2026-05-17T16:39:48'
authors:
- Sheikh Nazib Ahmed
- Marnim Galib
topics:
- multi-agent-software-engineering
- code-intelligence
- legacy-modernization
- behavioral-equivalence
- llm-agents
- software-foundation-models
relevance_score: 0.9
run_id: materialize-outputs
language_code: zh-CN
---

# AgentModernize: Preserving Business Logic in Legacy Modernization with Multi-Agent LLMs and Behavioral Specification Graphs

## Summary
## 概要
AgentModernize 是一个用于遗留代码现代化的多智能体 LLM 系统，目标是保留业务行为，而不只是转换语法。它最强的主张是：显式的 Behavioral Specification Graph 加上验证反馈，能比单轮提示和思维链基线更好地保持行为等价性，但绝对 BER 仍然偏低。

## 问题
- 遗留系统现代化后，即使能编译，也可能改变业务行为，比如 COBOL、PL/SQL、shell 脚本和配置文件里隐藏的边界规则、校验逻辑和异常处理。
- 这在银行、电信、医疗和其他受监管场景里很重要，因为未文档化规则往往承载生产和合规含义。
- 单轮 LLM 翻译没有明确工件可在模型写新代码之前检查它理解了什么。

## 方法
- 四个智能体把任务拆成遗留分析、规格生成、代码转换和等价性验证。
- Legacy Analyzer 提取业务规则、控制流、约束、源码位置和置信度标签，写入 Business Rule Inventory。
- Specification Generator 把这些规则转换为 Behavioral Specification Graph，包含操作节点、控制/数据边、前置条件、后置条件、不变式、输入、输出和错误行为。
- Transformer 根据 BSG 生成 Python/FastAPI 服务代码，把操作映射为端点，并把契约转换为校验和错误处理。
- Validator 基于 BSG 生成测试和差分轨迹，报告行为失败，并将定向修复结果回传给 Transformer，最多进行 3 轮反馈迭代。

## 结果
- 在 LegacyModernize-8 上，这个基准包含 8 个场景，其中 7 个是电信，1 个是银行；每个场景有 12 到 15 条规则，代码行数为 195 到 310。
- 使用 GPT-4o-mini 时，带反馈的 AgentModernize 达到 9.4% 的平均 Behavioral Equivalence Rate (BER)；SP-LLM、CoT-LLM 和不带反馈的 AgentModernize 的平均 BER 都是 0.0%。
- GPT-4o 的结果中，完整 AgentModernize 的平均 BER 为 8.1%；不带反馈版本的平均 BER 为 5.6%，且只有 S1 得到非零分数，44.4%。
- GPT-5.3-codex 中，完整 AgentModernize 的平均 BER 为 19.4%，而不带反馈的 AgentModernize 的平均 BER 为 0.0%。
- SP-LLM 和 CoT-LLM 在所有场景和所有测试 backbone 上的 BER 都是 0.0%。
- BSG 覆盖了 91.2% 的 gold-standard rules，所以论文认为，在提取之后，代码生成和修复是主要瓶颈。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17535v1](https://arxiv.org/abs/2605.17535v1)
