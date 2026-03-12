---
source: hn
url: https://github.com/terraincognita07/ovumcy
published_at: '2026-03-06T23:17:07'
authors:
- terrain07
topics:
- self-hosted-app
- privacy-first
- menstrual-cycle-tracker
- go-web-service
- health-data
relevance_score: 0.0
run_id: materialize-outputs
---

# Show HN: Ovumcy – self-hosted menstrual cycle tracker

## Summary
Ovumcy 是一个以隐私为优先的自托管月经周期追踪应用，面向希望在不依赖云账户、遥测或第三方基础设施的情况下记录敏感健康数据的用户。它更像一个产品/工程项目说明，而不是研究论文，没有提供实验性基准结果。

## Problem
- 现有经期追踪应用常依赖云账户、分析遥测或第三方服务，导致敏感健康数据控制权不足。
- 用户需要快速的日常记录、基础周期洞察和跨设备访问，但又不希望把数据托管给外部平台。
- 这很重要，因为月经与生育相关数据高度敏感，README 明确将“数据由用户自己控制”作为核心价值主张。

## Approach
- 核心机制很简单：把经期追踪做成**单体 Go 服务 + 服务端渲染 Web UI**，由用户自己部署，而不是注册云端 SaaS。
- 存储层默认使用 SQLite，提供 PostgreSQL 作为更高级的自托管选项；支持 Docker、单个二进制部署，并可放在反向代理之后运行。
- 功能层面提供日常记录（经期天数、流量强度、症状、备注）、预测（下次月经、排卵、易孕窗、周期阶段）、日历与统计视图，以及 CSV/JSON 导出。
- 隐私设计上强调**无分析、无广告跟踪、无核心第三方 API 依赖**，仅使用必要的一方 Cookie，并支持英语/俄语/西班牙语本地化。

## Results
- 文本**没有给出任何定量实验结果、用户研究、准确率评测或与其他追踪器的数值对比**。
- 可确认的具体工程结果包括：当前最新标记版本为 **v0.4.1**；支持 **3** 种一方 UI 语言（English/Russian/Spanish）。
- 部署与架构方面，系统可作为 **1 个 Go 服务**运行，默认数据库为 **SQLite**，并支持 **PostgreSQL** 作为高级路径。
- 安全与工程流程方面，声明集成了 **CodeQL、gosec、Trivy、CycloneDX SBOM** 等自动化检查，但没有提供漏洞减少率、性能提升或可靠性数字。
- 因此，该项目的最强主张不是算法突破，而是：在保持基本周期预测与记录功能的同时，提供**自托管、可导出、无遥测**的隐私优先替代方案。

## Link
- [https://github.com/terraincognita07/ovumcy](https://github.com/terraincognita07/ovumcy)
