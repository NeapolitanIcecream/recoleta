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
- cloud-runtime
relevance_score: 0.12
run_id: materialize-outputs
---

# Eclipse GlassFish: This Isn't Your Father's GlassFish

## Summary
这篇文章不是学术论文，而是一篇产品/技术宣传文，核心在于纠正“GlassFish 过时、慢、只适合开发环境”的旧印象，强调 Eclipse GlassFish 7.0 之后已成为可生产部署、持续演进的企业级 Java 应用服务器。

## Problem
- 要解决的问题是：开发者和企业仍把旧版 Oracle GlassFish / 早期 Eclipse GlassFish 的负面认知，套用到现代 Eclipse GlassFish 上。
- 这很重要，因为这种认知会阻碍团队采用一个已支持新 Jakarta EE、微服务部署和商业支持的 Java 平台。
- 文中明确针对“不可用于生产、缺乏支持、性能和安全不足、过时不适合现代轻量部署”等质疑。

## Approach
- 核心机制很简单：通过对比旧版与 7.0+ 之后的 Eclipse GlassFish，说明其在支持模式、标准兼容性、嵌入式运行时、性能和安全上的现代化变化。
- 强调商业支持能力：OmniFish 自 2022 年起提供 24×7 支持、SLA、受支持构建、补丁、安全修复和咨询服务，把“社区项目”转化为“可企业落地平台”。
- 强调标准与生态更新：声称率先通过 Jakarta EE 11 Web Profile 和 Platform TCK，并加入 MicroProfile Health、Config、REST Client、JWT 等 API 支持。
- 强调运行形态升级：把 Embedded GlassFish 从开发工具转为可用于命令行微服务和云容器的轻量、可观测生产运行时，并支持 JMX 监控。
- 强调工程改进：支持到 Java 25，默认采用 PKCS12 keystore，并持续改进启动速度、JDBC 连接池吞吐和资源管理。

## Results
- 文中给出的最明确时间节点是 **自 2022 年和 GlassFish 7.0 起**，其定位从“非生产”转向“production-ready, enterprise-grade platform”。
- 声称 **率先通过 Jakarta EE 11 Web Profile TCK 和 Jakarta EE 11 Platform TCK**；但未提供具体测试分数、耗时或与其他服务器的数值对比。
- 声称已支持多项 **MicroProfile API**：Health、Config、REST Client、JWT，用于微服务构建；未给出覆盖率或性能数据。
- 声称性能方面有 **更快启动时间、更高 JDBC pool throughput、更好资源管理**，并支持 **最高 Java 25**；但没有提供 benchmark 数字、数据集或基线比较。
- 安全方面声称默认切换到 **PKCS12 keystore**，并修复关键漏洞；未列出 CVE 编号、修复数量或合规指标。
- 总体上，文章的“突破性结果”主要是产品能力与标准认证声明，而**缺少可复现的定量实验结果**。

## Link
- [https://omnifish.ee/eclipse-glassfish-this-isnt-your-fathers-glassfish/](https://omnifish.ee/eclipse-glassfish-this-isnt-your-fathers-glassfish/)
