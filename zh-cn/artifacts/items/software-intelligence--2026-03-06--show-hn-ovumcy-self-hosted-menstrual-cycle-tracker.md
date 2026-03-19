---
source: hn
url: https://github.com/terraincognita07/ovumcy
published_at: '2026-03-06T23:17:07'
authors:
- terrain07
topics:
- self-hosted-app
- privacy-first
- health-tracking
- go-web-app
- sqlite-postgres
relevance_score: 0.13
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Ovumcy – self-hosted menstrual cycle tracker

## Summary
Ovumcy 是一个以隐私和自托管为核心的经期追踪应用，目标是在不依赖云账户、遥测或第三方基础设施的前提下，提供快速日常记录与周期洞察。它更像是一个工程化的软件产品说明，而不是一篇提出新算法或新模型的研究论文。

## Problem
- 现有经期追踪应用常依赖云端账户、分析埋点或第三方服务，使敏感健康数据暴露给外部基础设施。
- 用户需要一种既能方便记录经期、症状和周期信息，又能完全掌控数据存储、导出与部署方式的替代方案。
- 这很重要，因为经期与生育相关数据高度敏感，隐私、可移植性和无追踪能力直接影响用户信任与安全。

## Approach
- 核心方法很简单：把经期追踪做成**单一 Go 服务的自托管 Web 应用**，用户把服务部署在自己控制的服务器上，而不是把数据交给厂商云端。
- 前端采用**服务器渲染 HTML + HTMX + 少量原生 JavaScript**，支持浏览器访问和手机主屏安装，减少复杂客户端与外部依赖。
- 存储层默认使用**SQLite**，并提供 **PostgreSQL** 作为更高级的自托管选项；同时支持 **CSV/JSON 导出**，保证数据可迁移。
- 产品功能包含**日常记录**（经期天数、流量、症状、备注）、**可自定义症状管理**、以及基于历史记录的**下次经期、排卵期、易孕窗和周期阶段预测**。
- 隐私机制上强调**无遥测、无广告追踪、无核心第三方 API 依赖**，仅使用必要的一方 cookie，并辅以 CodeQL、gosec、Trivy、CycloneDX SBOM 等安全检查流程。

## Results
- 文本**没有提供标准研究型定量实验结果**，没有公开的准确率、F1、AUC、用户研究样本量，或与其他经期追踪器的数值对比。
- 给出的最具体成果是产品与工程状态：最新标记版本为 **v0.4.1**，支持 **3 种界面语言**（English、Russian、Spanish）。
- 部署形态上，系统以 **1 个 Go 服务**运行，默认数据库为 **SQLite**，也支持 **PostgreSQL**；可通过 **Docker Compose** 或单二进制部署。
- 功能性声明包括：支持**每日追踪**、**周期预测**、**日历与统计视图**、**CSV/JSON 导出**、**手机主屏安装**，以及**自定义症状的创建/重命名/隐藏/恢复**且保留历史记录。
- 隐私与安全方面的强主张是：**无 analytics、无 ad trackers、无第三方 API 依赖**，并在 CI 中运行 **CodeQL、gosec、Trivy 扫描与 CycloneDX SBOM 生成**。
- 因此，其“突破”主要不是算法性能，而是把**隐私优先、自托管、低依赖、可移植**的产品理念落到一个可部署的实际系统中。

## Link
- [https://github.com/terraincognita07/ovumcy](https://github.com/terraincognita07/ovumcy)
