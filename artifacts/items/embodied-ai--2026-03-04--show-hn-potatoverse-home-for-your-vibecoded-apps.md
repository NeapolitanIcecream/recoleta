---
source: hn
url: https://github.com/blue-monads/potatoverse
published_at: '2026-03-04T23:20:39'
authors:
- born-jre
topics:
- web-app-platform
- cms-paas
- go
- sqlite
- sandboxing
relevance_score: 0.01
run_id: materialize-outputs
---

# Show HN: Potatoverse, home for your vibecoded apps

## Summary
PotatoVerse 是一个将 CMS 与轻量级 PaaS 融合的应用托管平台，目标是用单个静态 Go 二进制和 SQLite 承载带服务端代码的 Web 应用。它强调应用隔离、可扩展执行器/能力接口，以及简化的安装、打包和托管流程。

## Problem
- 该项目试图解决“小型 Web 应用部署与托管过重、平台碎片化、扩展机制不统一”的问题，让开发者更容易发布带后端逻辑的应用。
- 它关注多应用共存时的隔离与权限边界，例如子源隔离、每应用独立数据访问，以及能力注册机制。
- 这很重要，因为很多轻量应用场景不需要完整云平台或复杂 CMS/PaaS 栈，但仍需要可部署性、扩展性和一定的安全隔离。

## Approach
- 核心机制是把整个平台做成一个静态 Go 可执行文件，内置 UI 资源和 SQLite，使部署尽量接近“下载即运行”。
- 应用被称为 spaces，运行在隔离环境中，默认通过 suborigin 提供隔离；后端代码当前在 Lua VM 中执行，未来计划支持 WASM，也允许原生 Go 或自定义执行器。
- 平台通过 **capabilities** 向应用暴露平台服务，应用以统一调用接口访问这些能力；同时支持事件驱动的异步 app-to-app 扩展。
- 数据层提供简单 KV 或 SQLite，并限制每个应用只能访问自己的隔离表；安装与升级支持仓库、zip 上传或 URL，且仓库可自托管，避免单一中心化商店。

## Results
- 文本未提供正式实验、基准测试或量化评测结果，因此没有可报告的准确数值指标。
- 最强的具体声明是：平台可作为**单个静态 Go 二进制**运行，并内置 **SQLite** 与打包后的 UI 资源，降低部署复杂度。
- 系统当前已支持 **Lua** 执行器，并明确规划 **WASM** 执行器、**Postgres** 支持、备份与 HTTP 隧道等后续能力。
- 应用隔离方面，声明支持基于 **suborigin** 的空间隔离，以及基于 SQL 语句解析的表级访问限制，但未给出安全性验证数据。
- 作者明确标注该项目为 **Alpha Software**，当前存在 bug、破坏性变更和功能不完整问题；隧道系统也已知对 **WebSockets** 和隔离源模式存在限制。

## Link
- [https://github.com/blue-monads/potatoverse](https://github.com/blue-monads/potatoverse)
