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
## 总结
一家软件公司的创始人表示，他在 8 周内用 Claude 在没有工程师、设计师或 QA 人员的情况下，做出了 Footbeen 这款可上线的足球比赛追踪应用。本文对自动化软件生产有参考价值，因为它给出了具体的交付结果、失败模式和工作流程变化，这些都来自一个真实应用的构建过程。

## 问题
- 作者想测试 AI 编程工具能否替代一个小型产品团队，完成一款真正上线的应用，因为客户已经在问，为什么他们还需要五人团队。
- 产品问题带有个人动机：记录看过比赛和球场的足球迷，常常用笔记或表格来整理，而现有应用要么收费，要么过时，要么数据质量差。
- 业务问题是人员配置：一个懂领域的资深个人加上 AI，是否能比一个产品背景更弱、人数更多的团队更高效地交付。

## 方法
- 作者把 Claude 作为主要编码助手，用接近给资深开发者写需求说明的方式，直接用自然语言提出功能需求。
- 应用技术栈是 React Native 加 Expo，Supabase 负责 Postgres 和 Auth，另外还用了 Mapbox、React Query、Vercel 和 EAS。
- 人工部分负责产品判断：流程设计、错误状态、性能检查、功能取舍，以及对生成代码的反复审核。
- 前几次失败后，提示方式有所改进：作者把需求写得更具体，加入约束，在接受生成代码前先阅读，并在行为不对时重新提问。
- 这个流程仍然需要人工排查生产环境崩溃、React 状态模式不佳、数据库查询慢，以及那些技术上能跑但用户体验很差的功能。

## 结果
- 第 1 周做出了一个可运行的应用，包含 Google 和 Apple 登录、Supabase 数据库结构、联赛、俱乐部、球场、比赛、可搜索的比赛目录、已访问球场地图和基础统计。
- Travel Planner 功能 1 天就上线了；作者估计这在自己的公司里要一个 2 周冲刺。这个功能包括城市和日期搜索、100 公里内的比赛发现、地理位置查询、比赛卡片和响应式设计。
- 经过 8 周后，应用宣称收录了 25,000+ 个球场、1,300+ 个联赛、200+ 个国家，以及从 2010 年起的 1,000,000+ 场赛程。
- 这款应用用同一套代码库发布到了 iOS、Android 和网页端，并带有 650+ 个 SEO 页面和 7 个语言版本的落地页。
- 作者表示，CI 中有 600+ 个自动化测试，使用了 Sentry 监控，崩溃率高于 99%。
- 这次构建没有花开发、设计或 QA 的钱，但证据只来自单一创始人陈述，没有独立基准或受控对比。

## Problem

## Approach

## Results

## Link
- [https://footbeen.com/blog/i-built-a-production-app-with-ai-no-developers](https://footbeen.com/blog/i-built-a-production-app-with-ai-no-developers)
