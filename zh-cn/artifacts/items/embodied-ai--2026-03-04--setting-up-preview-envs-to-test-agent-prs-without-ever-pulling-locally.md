---
source: hn
url: https://www.piersonmarks.com/posts/testing-agent-written-prs-in-the-cloud
published_at: '2026-03-04T23:59:50'
authors:
- PiersonMarks
topics:
- preview-environments
- github-actions
- supabase
- third-party-auth
- agentic-software-engineering
relevance_score: 0.08
run_id: materialize-outputs
language_code: zh-CN
---

# Setting Up Preview Envs to Test Agent PRs Without Ever Pulling Locally

## Summary
这篇文章介绍了一个用于测试 AI 代理生成 PR 的云端预览环境工作流，让团队无需本地拉代码即可在浏览器中完成功能与 UX 验证。核心贡献是补上 Supabase 预览分支不会自动继承第三方认证配置这一缺口，从而让每个 PR 都拥有可登录、可操作的隔离环境。

## Problem
- 代理能够并行写代码并提交 PR，但测试这些 PR 往往仍依赖本地拉分支、配置环境、跑迁移，成为整体开发流程的瓶颈。
- 虽然 Vercel + Supabase 可以为每个 PR 创建预览部署和隔离数据库，但使用 WorkOS 这类第三方认证时，Supabase 预览分支不会自动复制认证配置，导致用户无法登录，预览环境不可用。
- 这很重要，因为没有可交互的预览环境，团队就无法高效验证 agent-written PR 的真实功能、UX 和数据库变更，异步并行开发优势会被测试环节抵消。

## Approach
- 构建端到端异步工作流：Linear 发任务，AI coding agent 写代码并开 PR，GitHub Actions 触发 Vercel 预览部署与 Supabase 数据库预览分支创建，审阅者直接点击预览链接测试。
- 通过 GitHub Action 调用 Supabase Management API，在每个 PR 对应的 Supabase preview branch 上自动同步第三方认证配置。
- 工作流先轮询查询预览分支是否已创建；由于 Supabase 分支创建有延迟，因此采用最多 5 次、每次间隔 10 秒的重试机制。
- 为避免重复配置，脚本先检查该 preview branch 是否已存在 WorkOS 配置；若存在则退出，实现幂等。
- 该机制可推广到任意 OIDC 兼容认证提供商，不限于 WorkOS，只需替换 provider type 和 issuer URL。

## Results
- 文章未提供正式基准测试或实验数据，没有给出吞吐、成功率、故障率等量化评估。
- 给出的最具体时延数字是认证同步流程对 Supabase preview branch 最多重试 **5 次**，每次等待 **10 秒**，即最多约 **50 秒** 的分支就绪等待。
- 作者声称引入该 API 调用后，每个 PR 都能获得“fully functional, isolated preview environment”，支持真实登录和完整交互测试，而不是只能查看静态部署页面。
- 作者声称该流程将 reviewer 的反馈循环从“hours”缩短到“minutes”，但未提供对比实验、样本规模或统计数据。
- 系统层面的具体收益主张包括：每个 PR 独立数据库分支、多个 agent 可并行开发、避免共享 staging 冲突、避免本地环境漂移，但这些均为工程经验性结论而非论文式量化结果。

## Link
- [https://www.piersonmarks.com/posts/testing-agent-written-prs-in-the-cloud](https://www.piersonmarks.com/posts/testing-agent-written-prs-in-the-cloud)
