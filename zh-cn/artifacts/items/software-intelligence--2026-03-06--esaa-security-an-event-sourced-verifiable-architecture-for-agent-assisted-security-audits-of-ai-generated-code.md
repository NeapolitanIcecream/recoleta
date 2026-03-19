---
source: arxiv
url: http://arxiv.org/abs/2603.06365v1
published_at: '2026-03-06T15:15:26'
authors:
- Elzo Brito dos Santos Filho
topics:
- agentic-security-audit
- event-sourcing
- verifiable-ai-systems
- code-security
- multi-agent-governance
relevance_score: 0.93
run_id: materialize-outputs
language_code: zh-CN
---

# ESAA-Security: An Event-Sourced, Verifiable Architecture for Agent-Assisted Security Audits of AI-Generated Code

## Summary
本文提出 ESAA-Security，一种面向 AI 生成或 AI 修改代码的代理辅助安全审计架构，把“让 LLM 聊天式找漏洞”改造成“可验证、可重放、可追溯的事件驱动审计流程”。其核心贡献不是宣称发现更多漏洞，而是让审计过程和最终报告在治理与证据层面可审计。

## Problem
- 论文解决的是：AI 辅助开发加快了交付，但代码即使功能正确，仍可能在认证、授权、输入校验、密钥处理、依赖安全等方面存在结构性不安全。
- 现有基于提示词的 LLM 安全审查通常存在覆盖不均、结果不可复现、证据弱、严重性划分不一致、且缺少不可篡改审计轨迹的问题；这会使安全结论难以信任和复核。
- 这很重要，因为在代理式软件工程和长时程自动化流程中，若中间状态与结论不可验证，安全审计就很难支撑治理、整改优先级判断和最终问责。

## Approach
- 核心方法是事件溯源式治理：代理不直接修改审计状态，只能输出受约束的结构化“意图”；编排器负责校验、接受后写入追加式事件日志，再通过确定性投影重建当前审计状态。
- 审计被拆成 4 个阶段：侦察、领域审计执行、风险分类、最终报告；并进一步落地为 26 个任务、16 个安全领域、95 个可执行检查，把“审什么”显式编码出来。
- 机制上依赖一组 fail-closed 协议不变量，例如 claim-before-work、complete-after-work、锁归属、边界写入、done 不可静默重开；任何 schema、状态或边界违规都会在入库前被拒绝。
- 为保证可验证性，系统把追加式事件日志作为真实来源，并通过 replay + hashing 重放校验，确保最终报告、风险矩阵、漏洞清单等都能追溯到检查级证据。
- 输出不是自由文本，而是结构化证据链：检查结果 → 漏洞清单 → 严重性分类与风险矩阵 → 修复建议与高管摘要 → 最终 Markdown/JSON 报告。

## Results
- 论文的主要结果是架构与系统化设计结果，而不是实证性能结果；文中**没有提供**真实数据集上的定量实验指标、召回率/准确率/F1、或相对 baseline 的数值提升。
- 其最具体的实现性成果是：定义了 **4 个审计阶段、26 个任务、16 个安全域、95 个可执行检查**，覆盖如 authentication、authorization、input validation、dependencies、API security、cryptography、AI/LLM security、DevSecOps 等。
- 报告产物方面，系统声称可生成 **结构化检查结果、漏洞清单、CRITICAL/HIGH/MEDIUM/LOW/INFO 严重性分类、风险矩阵、技术修复建议、最佳实践建议、0–100 安全分数、执行摘要，以及最终 Markdown/JSON 审计报告**。
- 论文提出了明确评估维度与 baseline，但仍处于验证设计阶段：建议与 **prompt-only review** 和 **checklist-only review** 对比，比较覆盖显式性、证据结构、可重放性、报告完整性等，而非单纯漏洞数量。
- 作者的最强主张是：相较于自由式 LLM 审查，ESAA-Security 能让审计结果在**可追溯性、可复现性、覆盖显式性、工件完整性、整改可用性**方面更强；但这些主张在本文摘录中尚未用案例数字正式验证。

## Link
- [http://arxiv.org/abs/2603.06365v1](http://arxiv.org/abs/2603.06365v1)
