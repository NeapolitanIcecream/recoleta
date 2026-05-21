---
source: arxiv
url: https://arxiv.org/abs/2605.00179v1
published_at: '2026-04-30T19:54:25'
authors:
- Henry Ruckman-Utting
- Vrushal Nedungadi
- Taiga Okuma
- LeTian Wang
- Stephen Ehebald
- Mohammad A. Tayebi
topics:
- dependency-risk
- software-supply-chain
- code-intelligence
- policy-as-code
- llm-verification
- open-source-security
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# DEPTEX: Organization-First, Open Source Dependency Risk Monitoring

## Summary
## 摘要
Deptex 是一个开源依赖风险监控平台，按组织暴露面、资产归属和执行上下文对 OSS 风险排序。它的核心思路是结合组织图、可编程策略检查、基于 CPG 的可达性分析和 LLM 验证，减少低价值安全告警。

## 问题
- 现有 SCA 和可达性工具通常在缺少足够运行位置和运行方式上下文的情况下给易受攻击组件打分，导致告警疲劳。
- 企业需要与资产层级、法务审查、负责人和内部 API 绑定的策略，但许多工具只提供固定的合规控制项。
- 论文引用了运营缺口：只有 15% 的 CISO 表示能全面了解 OSS 使用情况，72% 的专业人员称供应链安全是关键盲点，自动化依赖 PR 的合并比例只有约 32%。

## 方法
- Deptex 将组织、单元、资产、组件、参与者和风险信号建模为类型化属性图，然后把风险从资产汇总到团队和整个组织。
- 其 Security “As Code” 引擎运行用于状态变更、组件规则、PR 门禁和通知的策略逻辑，包括调用 Legal API 或 PagerDuty 等内部系统。
- Execution Path Dominance (EPD)，也称 Depscore，从 Code Property Graph 切片开始，追踪从资产入口点到易受攻击依赖汇点的路径。
- 受约束的 LLM 检查切片代码的暴露类型和自定义净化处理；公共 API 获得更高暴露权重，经过净化的路径被赋予 0.0 的 EPD。
- 随后分数应用几何衰减，EPD = W_entry × α^d，其中 d 是路径深度，α 是衰减因子，例如 0.85。

## 结果
- 摘录没有报告受控基准测试、用户研究或实测告警减少率；它给出了运营场景和功能对比。
- 在 Depscore 场景中，一个 CVSS 9.8 漏洞可在 10 个仓库中到达；Deptex 将其中 8 个降级，因为它们是离线批处理脚本路径且有 6 层函数调用，而 2 条公共未认证 API 路径获得 92 的 EPD。
- 打分示例为面向公共的 API 分配 W_entry = 1.0，为内部后台任务分配 W_entry = 0.1；经过净化的路径被强制设为 0.0。
- 在工具表中，Deptex 被列为支持 7 项对比能力中的全部 7 项：CI/CD 和工单集成、许可证和合规审计、全组织组合视图、自托管部署、结构化 CPG 可达性、上下文漏洞评分和可编程策略。
- 该表称，Deptex 具备 3 项 Dependabot、Dependency-Track 和 Snyk 在表中缺少的能力：完整结构化 CPG 可达性、上下文漏洞评分和可编程 “As Code” 策略。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00179v1](https://arxiv.org/abs/2605.00179v1)
