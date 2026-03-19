---
source: hn
url: https://policycortex.com
published_at: '2026-03-07T23:24:40'
authors:
- policycortex
topics:
- cloud-security
- compliance-automation
- autonomous-remediation
- misconfiguration-detection
- ai-ops
relevance_score: 0.04
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: PolicyCortex – AI agent that autonomously remediates cloud misconfigs

## Summary
PolicyCortex 是一个面向云安全与合规的自动化平台，主打持续监控、审计证据收集和自治式修复云配置错误。其核心卖点是用带确定性护栏与回滚能力的 AI 代理，在不牺牲安全性的前提下把“发现问题”推进到“自动修复问题”。

## Problem
- 云环境中的 CMMC、NIST 800-171、CIS 等合规要求通常依赖人工检查、分散工具和临时性审计准备，导致效率低、遗漏多、难以持续保持审计就绪。
- 仅有告警而没有修复会让云配置错误长期存在；而直接让 AI 改生产环境又存在误操作、爆炸半径和合规风险。
- 对国防承包商、DOE 实验室和联邦机构而言，这很重要，因为它们面临严格的授权与评估要求，失败会影响业务准入、审计通过和安全态势。

## Approach
- 平台接入 AWS、Azure、GCP 账户后，自动发现资源、策略分配和适用的合规框架，并持续扫描环境。
- 将发现的配置问题映射到 CMMC、NIST 800-171、CIS、自定义框架，以及 MITRE ATT&CK/ATLAS，用于优先级排序、解释风险和生成修复路径。
- 核心机制是所谓的 **Safety Sandwich**：**执行前护栏检查 → AI 决策层（Xovyr）规划修复/生成代码/选择执行路径 → 执行后验证**，并保存回滚 ID。
- 为降低自治风险，系统声称不会在未经明确批准的情况下触碰生产资源，同时支持通过直接修复、推送 CI/CD PR、创建 Jira 工单或 Slack 通知等多种执行方式落地。
- 除修复外，还自动收集合规证据，生成 SSP、POA&M 和 ATO 包，把持续治理、审计准备、FinOps 和 AI 可观测性整合到一个平台中。

## Results
- 文本**没有提供论文式实验结果或基准测试**，没有给出误报率、修复成功率、审计通过率、时延、成本节省或与竞品/人工流程的定量对比。
- 最具体的覆盖指标包括：支持 **12+** 个合规框架、**3** 个云提供商、映射 **110+** 个 NIST 控制、提供 **4** 种部署模型。
- FinOps 模块的建议基于 **60–90 天** 的使用模式，而不是上月账单；这是产品机制说明，不是效果指标。
- 面向市场规模的陈述包括：有 **80,000+** 家国防承包商面临 CMMC 截止要求；这是应用场景背景，不是系统性能结果。
- 创始人相关的非研究性数字包括：平台由 **600K+** 行生产代码构建、已提交 **4** 项美国专利；这些说明工程投入与知识产权布局，但不能替代技术验证结果。
- 因此，最强的可验证主张是：该系统宣称可在持续监控基础上实现“带护栏的自治修复”和“自动化审计证据/授权文档生成”，但**缺少公开定量证据**来证明其相对现有方案的提升幅度。

## Link
- [https://policycortex.com](https://policycortex.com)
