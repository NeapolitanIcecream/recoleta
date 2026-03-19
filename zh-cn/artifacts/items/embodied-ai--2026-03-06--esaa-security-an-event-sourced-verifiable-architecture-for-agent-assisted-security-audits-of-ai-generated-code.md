---
source: arxiv
url: http://arxiv.org/abs/2603.06365v1
published_at: '2026-03-06T15:15:26'
authors:
- Elzo Brito dos Santos Filho
topics:
- security-audit
- event-sourcing
- llm-agents
- ai-generated-code
- verifiable-systems
relevance_score: 0.03
run_id: materialize-outputs
language_code: zh-CN
---

# ESAA-Security: An Event-Sourced, Verifiable Architecture for Agent-Assisted Security Audits of AI-Generated Code

## Summary
ESAA-Security提出一种面向AI生成/修改代码安全审计的事件溯源架构，把LLM从“自由对话式审查”改成“可验证的审计流水线”。其核心价值不在于宣称发现更多漏洞，而在于让审计范围、证据链、状态变化和最终报告都可追踪、可重放、可审计。

## Problem
- 解决的问题：AI辅助编程提高了开发速度，但代码即使功能正确，仍可能在认证、授权、输入校验、密钥管理、依赖安全等方面存在结构性安全缺陷。
- 为什么重要：现有基于提示词的LLM安全审查常见问题是覆盖不稳定、结论难复现、证据弱、严重性划分不一致，且缺少不可篡改的审计轨迹，难以用于治理和问责。
- 对代理式软件工程而言，长时程、多步骤、可变状态的执行会放大上下文遗漏和中间步骤不可验证的风险，因此单纯改进prompt不够。

## Approach
- 核心机制：把安全审计建模为**事件驱动的受治理流程**，而不是让LLM直接“读仓库后写一段审计意见”。代理只输出结构化意图，真正的状态变更由确定性的编排器验证后写入追加式事件日志。
- 架构上采用事件溯源与CQRS思想：**事件日志是唯一事实源**，当前审计状态由事件投影得到，并通过重放与哈希校验验证一致性，从而保证可追踪和可复现。
- 审计流程被拆成4个阶段：侦察（reconnaissance）、领域审计执行、风险分类、最终报告；并细化为26个任务、16个安全域、95个可执行检查，显式约束覆盖范围。
- 通过严格协议和不变量控制代理行为，如claim-before-work、complete-after-work、锁所有权、边界写入、done不可静默重开；任何schema错误、非法状态迁移或越界写入都在落库前被拒绝。
- 输出不是一篇随意生成的文字报告，而是从检查级证据对象出发，逐步汇总为漏洞清单、严重性分级、风险矩阵、修复建议、执行摘要以及最终Markdown/JSON报告。

## Results
- 论文的主要贡献是**架构与方法论**，不是已完成的大规模定量实验；文中**没有提供具体基准数据、准确率/召回率、或与baseline的数字对比结果**。
- 明确声称的结构化成果包括：**4个审计阶段、26个任务、16个安全域、95个可执行检查**，并生成漏洞清单、风险矩阵、修复建议、执行摘要和最终报告。
- 执行摘要中定义了一个**0–100安全评分**输出，但摘录中未报告任何真实案例得分或统计结果。
- 论文提出了评估维度与案例研究协议：比较ESAA-Security与prompt-only review、checklist-only review，重点看可重放性、可追踪性、覆盖显式性、工件完整性和修复实用性，而非仅比较漏洞数量。
- 最强的具体主张是：该系统能把AI辅助安全审计的“信任单位”从自由文本意见，转移为**协议有效、事件可追溯、状态可重放验证**的审计过程与报告。

## Link
- [http://arxiv.org/abs/2603.06365v1](http://arxiv.org/abs/2603.06365v1)
