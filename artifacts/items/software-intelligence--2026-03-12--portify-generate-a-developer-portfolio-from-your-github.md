---
source: hn
url: https://www.portify.ca/
published_at: '2026-03-12T23:06:55'
authors:
- lucasadilla
topics:
- developer-portfolio
- github-mining
- career-narrative
- repo-summarization
- automation
relevance_score: 0.77
run_id: materialize-outputs
---

# Portify: Generate a developer portfolio from your GitHub

## Summary
Portify 是一个把开发者 GitHub 活动自动整理成可分享作品集的网站工具。它将仓库、提交、技术栈和时间线转成更适合求职与展示的个人叙事页面。

## Problem
- 原始 GitHub 主页对招聘方或协作者不够友好，信息分散，难以快速理解开发者做过什么、如何成长。
- 开发者需要把提交记录、仓库说明、技术栈和项目演化手动整理成作品集，成本高且不易持续更新。
- 这很重要，因为求职、社交和合作场景需要一个清晰、可信、持续同步的个人技术展示入口。

## Approach
- 用户用 GitHub 登录后，选择最能代表自己的若干仓库，系统读取 commits、languages 和 repository metadata。
- Portify 自动为仓库生成可读摘要，识别技术栈，构建贡献/语言/演化图表，并串联为单页个人叙事。
- 生成一个固定可分享的个人 URL，并保持与 GitHub 活动同步更新。
- 用户还能手动编辑内容，并补充截图和 Mermaid 图，使页面更像产品展示而不是简历列表。

## Results
- 文本未提供正式论文式实验、基准或量化指标，因此**没有可报告的定量结果**。
- 明确声明的产出包括：从 GitHub 历史生成 **1 个可分享 portfolio URL**（例如 `/yourname`）。
- 系统声称可自动生成多类内容：项目摘要、技术栈徽章、贡献随时间变化图、语言分布、公开时间线。
- 给出的流程是 **3 个步骤**：选仓库、自动生成叙事、分享并持续同步。
- 其最强具体主张是把“原始 GitHub 活动”转成“适合求职分享的单页作品集”，并支持持续更新而非一次性静态简历。

## Link
- [https://www.portify.ca/](https://www.portify.ca/)
