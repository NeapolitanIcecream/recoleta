---
source: hn
url: https://policycortex.com
published_at: '2026-03-07T23:24:40'
authors:
- policycortex
topics:
- cloud-compliance
- autonomous-remediation
- ai-agent
- cloud-security
- audit-automation
relevance_score: 0.72
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: PolicyCortex – AI agent that autonomously remediates cloud misconfigs

## Summary
PolicyCortex 是一个面向云合规与安全运营的 AI 代理平台，主打对云配置错误进行持续检测、审计证据收集与受控的自主修复。它面向国防承包商、DOE 实验室等高合规场景，强调“持续达标”而非临时应考。

## Problem
- 云环境中的 **CMMC / NIST 800-171 / CIS** 等合规要求通常依赖人工核查、分散工具和临时审计准备，导致配置错误长期存在、证据收集低效。
- 高敏感组织（如国防承包商、联邦机构）需要在 **多云环境** 中持续监控 110+ 控制项，并把发现、修复、审计文档和审批流程串起来。
- 单纯告警并不能解决问题；自动修复若缺少约束又可能误伤生产系统，因此需要“可控自治”的修复机制。

## Approach
- 平台先接入 **AWS / Azure / GCP**，自动发现资源、策略分配和适用合规框架，并进行持续扫描与实时合规监控。
- 将合规发现映射到 **MITRE ATT&CK**，并给出可执行修复路径；对 AI 资产还映射 **MITRE ATLAS** 做 AI 专项可观测与威胁检测。
- 核心机制是其专利申请中的 **Safety Sandwich**：**预执行护栏 → AI 决策层（Xovyr）→ 后执行校验**。简单说，就是先检查风险边界，再让 AI 规划/生成修复动作，最后验证变更并保留回滚能力。
- 自主修复支持多种执行路径：直接修复、向 **CI/CD** 推送 PR、创建 **Jira** 工单或发 **Slack** 通知，并记录审计日志和 rollback ID；生产资源默认需显式批准。
- 除修复外，系统还自动化 **SSP、POA&M、ATO** 等审计材料生成，以及基于 **60–90 天** 使用模式的 FinOps 建议。

## Results
- 文本**未提供标准论文式定量评测**（如误报率、修复成功率、与基线工具对比、公开数据集结果）。
- 明确给出的覆盖规模包括：支持 **12+ 合规框架**、**3 个云提供商**、映射 **110+ NIST 控制项**、提供 **4 种部署模型/形态**（文中详细描述了 SaaS、Private Cloud、Air-Gapped，页面另称 4 deployment models）。
- FinOps 模块声称基于 **60–90 天** 使用模式生成资源规格优化建议，而不是仅依据上月账单。
- 目标市场层面，页面声称面向 **80,000+ defense contractors** 的 CMMC 需求，并已被国防承包商信任使用，但未给出客户数量、转化率或审计通过率。
- 关键产品性主张是：可在“几分钟内”发现云资源与策略，执行**持续监控**、**自动证据收集**、**自主修复且可回滚**，并支持 **air-gapped** 本地推理部署。

## Link
- [https://policycortex.com](https://policycortex.com)
