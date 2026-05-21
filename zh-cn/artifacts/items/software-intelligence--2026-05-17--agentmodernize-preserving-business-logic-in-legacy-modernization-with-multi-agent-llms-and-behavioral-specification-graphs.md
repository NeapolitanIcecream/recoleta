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
## 摘要
AgentModernize 是一个用于遗留代码现代化的多智能体 LLM 系统，目标是在迁移语法的同时保留业务行为。论文最强的主张是，显式的 Behavioral Specification Graph 加上验证反馈，相比单提示词和思维链基线能提高行为等价性，但绝对 BER 仍然较低。

## 问题
- 遗留系统现代化后的代码可能可以编译，却改变业务行为，例如隐藏在 COBOL、PL/SQL、shell 脚本和配置文件中的边界情况规则、校验逻辑和异常处理。
- 这在银行、电信、医疗和其他受监管场景中很重要，因为未文档化的规则常常承载生产和合规含义。
- 单轮 LLM 翻译在写出新代码前，没有显式产物可用于检查模型理解了什么。

## 方法
- 四个智能体将任务拆分为遗留系统分析、规范生成、代码转换和等价性验证。
- Legacy Analyzer 将业务规则、控制流、约束、源码位置和置信度标签提取到 Business Rule Inventory 中。
- Specification Generator 将这些规则转换为 Behavioral Specification Graph，其中包含操作节点、控制/数据边、前置条件、后置条件、不变量、输入、输出和错误行为。
- Transformer 根据 BSG 生成 Python/FastAPI 服务代码，将操作映射到端点，并把契约转换为校验和错误处理。
- Validator 根据 BSG 创建测试和差分跟踪，报告行为失败，并将定向修复发回 Transformer，最多进行 3 轮反馈迭代。

## 结果
- 在 LegacyModernize-8 上，该基准包含 8 个场景，其中 7 个电信场景和 1 个银行场景；每个场景有 12-15 条规则和 195-310 LOC。
- 使用 GPT-4o-mini 时，带反馈的 AgentModernize 达到 9.4% 平均 Behavioral Equivalence Rate (BER)；SP-LLM、CoT-LLM 和无反馈的 AgentModernize 平均 BER 都为 0.0%。
- GPT-4o 的结果是：完整 AgentModernize 的平均 BER 为 8.1%；无反馈变体的平均 BER 为 5.6%，且只有 S1 产生非零分数，为 44.4%。
- GPT-5.3-codex 上，完整 AgentModernize 的平均 BER 达到 19.4%，而无反馈的 AgentModernize 平均 BER 为 0.0%。
- SP-LLM 和 CoT-LLM 在每个场景和每个测试骨干模型上的 BER 都为 0.0%。
- BSG 捕获了 91.2% 的金标准规则，因此论文认为，提取之后的主要瓶颈是代码生成和修复。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.17535v1](https://arxiv.org/abs/2605.17535v1)
