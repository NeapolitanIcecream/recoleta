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
Deptex 是一个开源依赖风险监控平台，按组织暴露面、资产归属和执行上下文来排序 OSS 风险。它的主要思路是把组织图、可编程策略检查、基于 CPG 的可达性分析和 LLM 验证结合起来，减少低价值安全告警。

## 问题
- 现有 SCA 和可达性工具常常在缺少足够上下文的情况下给受漏洞影响的组件打分，看不清脆弱代码在哪里、如何运行，从而造成告警疲劳。
- 企业需要把策略绑定到资产等级、法务审查、负责人和内部 API，但很多工具只提供固定的合规控制。
- 文中引用的运营差距包括：只有 15% 的 CISO 表示对 OSS 使用情况有完整可见性，72% 的从业者把供应链安全称为关键盲区，只有约 32% 的自动依赖 PR 会被合并。

## 方法
- Deptex 将组织、部门、资产、组件、角色和风险信号建模为一个有类型的属性图，然后把风险从资产汇总到团队再到整个组织。
- 它的 Security “As Code” 引擎会运行状态变更、组件规则、PR 门禁和通知的策略逻辑，包括调用 Legal API 或 PagerDuty 等内部系统。
- Execution Path Dominance（EPD），也叫 Depscore，从 Code Property Graph 切片开始，追踪从资产入口点到有漏洞依赖 sink 的路径。
- 一个受约束的 LLM 会检查切分后的代码，判断暴露类型和自定义净化情况；公共 API 的暴露权重更高，而已净化路径的 EPD 设为 0.0。
- 之后分数使用几何衰减，EPD = W_entry × α^d，其中 d 是路径深度，α 是衰减因子，例如 0.85。

## 结果
- 这段摘录没有报告受控基准测试、用户研究或测得的告警减少率；它给出的是运行场景和功能对比。
- 在 Depscore 场景中，一个 CVSS 9.8 的漏洞可在 10 个仓库中到达；Deptex 将其中 8 个降级，因为它们是离线批处理脚本路径，深度为 6 次函数跳转，而 2 条面向公网、未认证的 API 路径得到的 EPD 为 92。
- 这些评分示例把面向公网的 API 的 W_entry 设为 1.0，把内部后台任务的 W_entry 设为 0.1；已净化路径被强制设为 0.0。
- 在工具对比表中，Deptex 被列为支持 7 项对比能力中的 7 项：CI/CD 和工单集成、许可证与合规审计、全组织组合视图、自托管部署、结构化 CPG 可达性、上下文漏洞评分，以及可编程策略。
- 该表称，和 Dependabot、Dependency-Track、Snyk 的列出能力相比，Deptex 多出 3 项：完整的结构化 CPG 可达性、上下文漏洞评分，以及可编程的 “As Code” 策略。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2605.00179v1](https://arxiv.org/abs/2605.00179v1)
