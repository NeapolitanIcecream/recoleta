---
source: hn
url: https://footbeen.com/blog/i-built-a-production-app-with-ai-no-developers
published_at: '2026-05-10T22:24:17'
authors:
- dmgmyza
topics:
- ai-coding
- automated-software-production
- human-ai-interaction
- code-intelligence
- software-teams
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# I run a company with 30 engineers. Built this app with AI and none of them

## Summary
## 摘要
一家软件公司创始人称，他在 8 周内使用 Claude 构建了 Footbeen，一个已上线的足球比赛记录应用，没有使用工程师、设计师或 QA 人员。这个案例对自动化软件生产有参考价值，因为它来自一个真实应用的构建过程，提供了具体的交付说法、失败模式和工作流变化。

## 问题
- 作者想测试 AI 编码工具能否在真实上线应用中替代一个小型产品团队，因为客户已经开始询问为什么还需要五人团队。
- 产品问题来自个人需求：会记录观赛比赛和到访球场的足球球迷常用笔记或电子表格，而现有应用要么收费，要么界面陈旧，要么数据质量差。
- 商业问题是人员配置：一个懂领域的资深人员配合 AI，能否比一个产品背景较弱的大团队更有效地交付。

## 做法
- 作者把 Claude 作为主要编码助手，用普通英语提出功能请求，方式类似给资深开发者写简报。
- 应用技术栈是 React Native with Expo、Supabase for Postgres and Auth、Mapbox、React Query、Vercel 和 EAS。
- 人类负责产品判断：流程设计、错误状态、性能检查、功能取舍，以及反复审查生成的代码。
- 早期失败后，提示词写法有所改进：作者把请求写得更具体，设置约束，在接受代码前先阅读生成代码，并在行为不对时重新提示。
- 工作流仍然需要人工诊断生产崩溃、糟糕的 React 状态模式、缓慢的数据库查询，以及技术上可运行但用户体验差的功能。

## 结果
- 第 1 周产出了一个可运行应用，包含 Google 和 Apple 登录、Supabase schema、联赛、俱乐部、球场、比赛、可搜索的比赛目录、已到访球场地图和基础统计。
- Travel Planner 功能在 1 天内上线；作者估计，如果在他的公司完成同样功能，需要一个 2 周 sprint。该功能包含城市和日期搜索、100 km 范围内的比赛发现、地理位置查询、比赛卡片和响应式设计。
- 8 周后，该应用声称收录 25,000+ 个球场、1,300+ 个联赛、200+ 个国家，并拥有可追溯到 2010 年的 1,000,000+ 场赛程。
- 该应用用一个代码库上线 iOS、Android 和 web，并提供 650+ 个 SEO 页面和 7 种语言版本的落地页。
- 作者称 CI 中有 600+ 个自动化测试、Sentry 监控，以及超过 99% 的无崩溃率。
- 构建过程中在开发者、设计师或 QA 上花费 $0，但证据来自单位创始人的陈述，没有独立基准或受控对比。

## Problem

## Approach

## Results

## Link
- [https://footbeen.com/blog/i-built-a-production-app-with-ai-no-developers](https://footbeen.com/blog/i-built-a-production-app-with-ai-no-developers)
