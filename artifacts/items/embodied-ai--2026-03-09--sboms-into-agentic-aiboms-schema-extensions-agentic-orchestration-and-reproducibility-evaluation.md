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
- software-supply-chain-security
- multi-agent-systems
- runtime-dependency-analysis
- vex-csaf
- reproducibility
relevance_score: 0.03
run_id: materialize-outputs
---

# SBOMs into Agentic AIBOMs: Schema Extensions, Agentic Orchestration, and Reproducibility Evaluation

## Summary
本文提出将静态 SBOM 扩展为“代理式”AIBOM：在标准兼容的前提下，把运行时上下文、依赖漂移和漏洞可利用性推理纳入可审计的软件溯源工件。其目标是提升软件供应链安全中的复现性、漏洞解释稳定性与运行时依赖捕获能力。

## Problem
- 传统 SBOM 只记录静态依赖清单，无法反映运行时行为、环境漂移和漏洞是否真正可利用，因此难以支持高可信的安全评估与可复现审计。
- 现代软件存在动态加载、延迟绑定和联邦服务，单看组件“存在”不足以判断风险；这很重要，因为海量 CVE 中大量漏洞在具体环境里并不可利用。
- 现有 provenance/复现工具多偏向打包回放、单元验证或元数据图谱，缺少把运行时证据、策略约束和标准化 VEX/CSAF 语义统一到同一工件中的机制。

## Approach
- 核心方法是一个三代理多智能体框架：MCP 负责执行前环境重建，A2A 负责运行时依赖与环境漂移监测，AGNTCY 负责结合策略与 VEX 规则做漏洞可利用性判断。
- 该框架把 SBOM 从“被动清单”变成“主动推理工件”：代理读取运行时遥测、依赖使用情况和环境缓解措施，输出结构化的 VEX 断言，而不是直接执行封禁。
- 作者对 CycloneDX 和 SPDX 做了最小化、标准对齐的 schema 扩展，新增执行上下文、依赖演化时间线、代理决策来源和 CSAF 证据链接，同时保持与现有生态互操作。
- 评测设计将其与 ReproZip、SciUnit、ProvStore 等 provenance 系统对比，并用 pre/mid/post 快照、导入钩子和包管理器记录来构建运行时依赖真值；复现性区分 exact parity 与 semantic parity，阈值设为 ε=1e-12（确定性统计）和 ε=1e-6（浮点 ML）。
- 系统还加入容错与审计机制，如心跳检查、失败即关闭、跨快照一致性校验、会话密钥签名，以及当缺失或错误哈希组件超过 2% 时触发完整性违规并要求人工裁决。

## Results
- 论文声称在异构分析工作负载上，相比既有 provenance 系统，实现了更好的**运行时依赖捕获**、**复现保真度**和**漏洞解释稳定性**，且计算开销较低。
- 文中给出了若干评测/判定阈值与规模背景：语义复现阈值为 ε=1e-12（确定性）和 ε=1e-6（浮点 ML）；若预期组件缺失或哈希错误 **>2%**，系统触发完整性违规；CV E 生态在 2025 年约 **191,633** 条，2026 年已超 **200,000**，年新增超过 **30,000**。
- 论文还用外部背景数据说明问题规模：约 **95%** 的 SBOM 中漏洞在产品中通常不可利用；Dependency-Track 对 OSS Index 的请求从每月 **2.02 亿** 增至 **2.7 亿**；平均产品约 **135-150** 个第三方组件；估算至少 **50,000** 家组织在用 SBOM 做漏洞管理。
- 但在给定摘录中，**没有看到完整的主实验定量结果表**（例如具体 capture rate、FPR/FNR、复现率、延迟、开销百分比、与各基线的精确差值），因此无法准确复述核心改进幅度。
- 摘录中最强的实证性主张是：消融实验表明三个代理各自提供了确定性自动化无法替代的独特能力；系统能生成 “Not Affected / Affected: Mitigated / Affected: Requires Review / Under Investigation” 四类上下文化 VEX 状态。

## Link
- [http://arxiv.org/abs/2603.10057v1](http://arxiv.org/abs/2603.10057v1)
