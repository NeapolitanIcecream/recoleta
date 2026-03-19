---
source: hn
url: https://omnifish.ee/eclipse-glassfish-this-isnt-your-fathers-glassfish/
published_at: '2026-03-05T23:18:57'
authors:
- henk53
topics:
- java-application-server
- jakarta-ee
- microprofile
- enterprise-java
- glassfish
relevance_score: 0.0
run_id: materialize-outputs
language_code: zh-CN
---

# Eclipse GlassFish: This Isn't Your Father's GlassFish

## Summary
这是一篇介绍 Eclipse GlassFish 现代化演进的文章，核心是反驳其“慢、无人支持、只适合开发环境”的旧印象。文章强调自 GlassFish 7.0 起，该平台已成为具备商业支持、现代 Java 标准兼容性和轻量化部署能力的企业级应用服务器。

## Problem
- 文章要解决的问题是：开发者和企业仍基于旧版本经验，把 GlassFish 视为**不适合生产、缺乏支持、性能落后**的应用服务器。
- 这很重要，因为这类认知会阻碍企业升级或采用一个其实已经成熟的 Java/Jakarta EE 平台，影响生产部署、标准兼容和现代化迁移决策。
- 文中还隐含对比问题：老 Oracle GlassFish / 早期 Eclipse GlassFish 与现代 Eclipse GlassFish 的能力差异常被忽视。

## Approach
- 核心机制很简单：作者通过**版本分界（尤其是 7.0 之后）+ 功能清单 + 支持能力说明**，证明现代 Eclipse GlassFish 已与旧版显著不同。
- 具体做法包括强调 **OmniFish 自 2022 年起提供商业支持**，覆盖 24×7 支持、SLA、受支持构建、漏洞修复、热补丁和咨询服务，以回应“无人支持、不能生产用”的质疑。
- 文章还用**标准合规与平台能力升级**作为证据：如率先通过 Jakarta EE 11 Web Profile 和 Platform TCK，并支持多个 MicroProfile API（Health、Config、REST Client、JWT）。
- 另一个关键点是将 **Embedded GlassFish** 从偏开发工具改造成可用于命令行微服务和云容器的轻量级、可观测、生产就绪运行时。
- 同时强调性能和安全改进，包括更快启动、更好的 JDBC 连接池吞吐、更好的资源管理、支持到 Java 25，以及默认转向 PKCS12 keystore 并修复关键漏洞。

## Results
- 文中最明确的可量化时间节点是：**自 2022 年、GlassFish 7.0 起**，作者声称平台已转变为“production-ready, enterprise-grade platform”。
- 文章声称 Eclipse GlassFish **率先通过 Jakarta EE 11 Web Profile 和 Jakarta EE 11 Platform TCK**，这是其最强的技术背书之一，但**未提供具体测试分数、耗时或与其他服务器的数值对比**。
- 支持能力上给出明确服务形式：**24×7 支持**、严格 **SLA**、安全测试构建、漏洞修复、热补丁和专家咨询，但没有披露客户数量、故障恢复时间或支持基准数据。
- 兼容性上，文章明确称可支持**最高到 Java 25**，并支持多项 MicroProfile API；这是具体版本层面的进展。
- 性能方面，作者声称有**更快启动时间、改进的 JDBC pool throughput、更好的资源管理**，但摘录中**没有提供任何 benchmark 数字、数据集、基线或百分比提升**。
- 因此，这篇文章的“突破性结果”主要是**平台定位和生态成熟度的改变**，而不是严格论文式实验结果。

## Link
- [https://omnifish.ee/eclipse-glassfish-this-isnt-your-fathers-glassfish/](https://omnifish.ee/eclipse-glassfish-this-isnt-your-fathers-glassfish/)
