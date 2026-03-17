---
source: hn
url: https://xeolint.com/
published_at: '2026-03-14T23:19:44'
authors:
- antoinelevy27
topics:
- seo
- geo
- nextjs
- cli-linter
- llm-discoverability
relevance_score: 0.72
run_id: materialize-outputs
---

# CLI linter for GEO and SEO discoverability

## Summary
XEOLint 是一个面向 Next.js 站点的开源 CLI 检查工具，用于发现影响被搜索引擎和大模型发现的问题。它聚焦于 GEO/SEO 可发现性这一发布后常被忽视但会直接影响流量与可见性的环节。

## Problem
- 许多快速开发并上线的项目，尤其是“vibecoded”项目，会在可发现性上出问题，导致站点不易被搜索引擎或 LLM 发现。
- 这很重要，因为即使产品功能正常，如果 GEO/SEO 基础配置缺失，用户和智能体也可能根本找不到它。
- 给定文本特别强调 Next.js 站点的 discoverability，而非功能或性能问题。

## Approach
- 核心方法是一个可通过 `pip install xeolint` 安装的 CLI linter，对 Next.js 站点进行检查。
- 它的机制可以简单理解为：自动扫描站点中与 GEO 和 SEO 相关的配置或模式，找出会妨碍被 LLM 与搜索引擎发现的问题。
- 该工具是开源的，版本标注为 `v0.1.0`，说明其定位更像早期实用检查器而非完整平台。
- 从描述看，它专注“确保可发现性”，即在发布流程中增加一层自动化质量门禁。

## Results
- 给定内容**没有提供量化实验结果**，没有数据集、指标、基线或对比数字。
- 最强的具体主张是：XEOLint“ensures your Next.js site is discoverable by LLMs and search engines”。
- 适用对象明确为 **Next.js** 站点。
- 发布形态明确为 **Open Source**、版本 **v0.1.0**、安装方式为 **`pip install xeolint`**。

## Link
- [https://xeolint.com/](https://xeolint.com/)
