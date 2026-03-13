---
source: arxiv
url: http://arxiv.org/abs/2603.10057v1
published_at: '2026-03-09T19:11:45'
authors:
- Petar Radanliev
- Carsten Maple
- Omar Santos
- Kayvan Atefi
topics:
- sbom
- aibom
- multi-agent-systems
- software-supply-chain-security
- reproducibility
- vex-csaf
relevance_score: 0.85
run_id: materialize-outputs
---

# SBOMs into Agentic AIBOMs: Schema Extensions, Agentic Orchestration, and Reproducibility Evaluation

## Summary
本文将静态 SBOM 扩展为具备上下文推理能力的 agentic AIBOM，使软件物料清单不仅记录组件，还能结合运行时证据与策略输出可审计的漏洞可利用性判断。其核心贡献是多智能体编排、对 CycloneDX/SPDX 的最小模式扩展，以及围绕可复现性与漏洞解释稳定性的评估。

## Problem
- 传统 SBOM 只描述静态依赖，无法反映运行时行为、环境漂移、动态加载与真实可利用性，因此难以支持高可信的软件供应链安全与可复现审计。
- 在海量 CVE 背景下，组件“存在”不等于漏洞“可利用”；若缺少上下文过滤，安全团队会被大量不可利用漏洞淹没。
- 受监管或高保证分析环境需要把软件组成、执行上下文和审计证据绑定到一起，否则即使代码与数据不变，环境差异也会破坏结果复现与合规判断。

## Approach
- 提出 agentic AIBOM 框架：把 SBOM 从被动清单变成主动溯源对象，输出与 CSAF v2.0 / VEX 对齐的结构化可利用性声明，而不是直接执行封禁动作。
- 采用三类多智能体协作：MCP 负责基线环境重建，A2A 负责运行时依赖与环境漂移监测，AGNTCY 负责结合策略、缓解措施与执行证据进行漏洞/VEX 推理。
- 对 CycloneDX 和 SPDX 做“最小且兼容”的 schema 扩展，新增执行上下文、依赖演化时间线、agent 决策来源与 advisory 证据字段，同时保持互操作性。
- 通过 pre/mid/post 多阶段快照、导入钩子与包管理器插桩建立运行时依赖真值，并用 Capture Rate、FPR、FNR、语义/精确复现率、延迟与开销评测。
- 为保证高可信性，系统加入故障闭锁、跨快照一致性校验、分段签名和完整性阈值；例如缺失或错误哈希组件超过 **2%** 时触发完整性违规并要求人工裁决。

## Results
- 论文明确声称：在异构分析工作负载上，agentic AIBOM 相比 ReproZip、SciUnit、ProvStore 等既有溯源系统，提高了**运行时依赖捕获**、**复现保真度**和**漏洞解释稳定性**，且计算开销较低。
- 论文还声称消融实验表明三个 agent 各自提供了确定性自动化无法替代的独特能力，支持其多智能体设计必要性。
- 文中给出了可量化的评测定义与阈值：精确复现使用 **SHA-256** 字节级一致；语义复现容差为确定性任务 **ε=1e-12**、浮点 ML 任务 **ε=1e-6**。
- 可靠性机制中给出明确规则：若跨阶段校验发现预计组件中**超过 2%** 缺失或哈希错误，则阻止流程继续并升级人工审查。
- 背景数据强调问题规模：截至写作时 CVE 超过 **191,633** 条，后续已超过 **200,000**；**2022 年 32,760** 条、**2021 年约 22,000** 条；约 **11%** 被归为 critical；约 **95%** 的 SBOM 组件漏洞通常在产品中不可利用。
- 提供的摘录**没有出现直接的最终 benchmark 数值表**（如具体提升百分比、各数据集绝对分数或开销毫秒数），因此无法从摘录中提取更细的定量对比结果。

## Link
- [http://arxiv.org/abs/2603.10057v1](http://arxiv.org/abs/2603.10057v1)
