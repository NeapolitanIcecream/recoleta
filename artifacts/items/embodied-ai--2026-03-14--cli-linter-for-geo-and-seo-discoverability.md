---
source: hn
url: https://xeolint.com/
published_at: '2026-03-14T23:19:44'
authors:
- antoinelevy27
topics:
- seo
- llm-discoverability
- nextjs
- cli-linter
- developer-tools
relevance_score: 0.02
run_id: materialize-outputs
---

# CLI linter for GEO and SEO discoverability

## Summary
XEOLint 是一个面向 Next.js 网站的开源 CLI 检查工具，目标是提升被大语言模型与搜索引擎发现和理解的能力。它强调快速开发项目常忽略“可发现性”问题，并提供自动化检查来弥补这一缺口。

## Problem
- 许多快速迭代的项目虽然上线很快，但在 **LLM 可发现性** 和 **SEO 可发现性** 上存在缺陷。
- 如果网站不能被搜索引擎或 AI 系统正确抓取、解析与理解，就会直接影响流量获取、内容曝光和产品被使用者发现的机会。
- 该问题之所以重要，是因为随着 AI 驱动搜索与代理使用增多，网站不仅要对传统搜索引擎友好，也要对 LLM 友好。

## Approach
- 核心方法是一个 **CLI linter**：像代码静态检查一样，对 Next.js 网站做可发现性检查。
- 它以最简单的方式帮助开发者在发布前发现问题：安装工具后运行检查，找出影响 GEO/SEO 的缺陷。
- 机制上，它面向 **LLMs 和搜索引擎** 两类发现渠道，试图统一检查网站在这两种入口下的可见性问题。
- 从提供的信息看，它当前是 **开源 v0.1.0**，通过 `pip install xeolint` 安装，说明其定位是轻量、可集成到开发流程中的工具。

## Results
- 提供的内容 **没有给出任何定量结果**，没有报告数据集、评测指标、基线方法或性能提升数字。
- 最强的具体主张是：XEOLint “确保” Next.js 网站对 **LLMs 和搜索引擎可发现**。
- 文本明确给出的事实性信息包括：**开源**、版本为 **v0.1.0**、支持通过 **pip install xeolint** 安装。
- 由于缺少实验、对比和基准，无法验证其相对现有 SEO 工具或网站审计工具的实际改进幅度。

## Link
- [https://xeolint.com/](https://xeolint.com/)
