---
source: hn
url: https://www.piersonmarks.com/posts/testing-agent-written-prs-in-the-cloud
published_at: '2026-03-04T23:59:50'
authors:
- PiersonMarks
topics:
- ai-coding-agents
- preview-environments
- github-actions
- supabase
- oidc-auth
- developer-workflow
relevance_score: 0.89
run_id: materialize-outputs
---

# Setting Up Preview Envs to Test Agent PRs Without Ever Pulling Locally

## Summary
这篇文章介绍了一个面向 AI 编码代理 PR 的云端预览测试工作流：每个 PR 自动获得独立的 Vercel 预览站点和 Supabase 数据库分支，评审者直接在浏览器里验证功能与 UX，无需本地拉代码。核心补丁是用 GitHub Action 在每个 Supabase 预览分支上自动补齐 WorkOS 第三方认证配置，解决“预览环境能部署但无法登录”的关键阻塞。

## Problem
- 当多个 AI 代理并行提交 PR 时，**测试**而不是写代码，成为主要瓶颈；逐个本地拉分支、配环境、跑迁移会拖慢整个异步开发流程。
- 仅看 GitHub diff 无法验证功能是否真的可用，尤其无法检查完整 UX 和登录后的受保护路径。
- Supabase 预览分支会复制数据库与策略，但**不会自动复制第三方认证配置**；使用 WorkOS 等外部 OIDC 提供方时，预览环境会因无法登录而失去测试价值。

## Approach
- 搭建端到端 PR 预览链路：Linear 派单给 AI 代理，代理提交 PR 后，GitHub Actions 触发 Vercel 预览部署与 Supabase 独立数据库分支创建。
- 将“预览环境”直接作为“测试环境”：每个 PR 拥有唯一 URL 和隔离数据库，避免共享 staging 冲突，也无需本地环境准备。
- 通过 GitHub Action 调用 **Supabase Management API**：在 PR 打开/更新/重开时，轮询查找对应的 Supabase preview branch，然后向 `/v1/projects/{ref}/config/auth/third-party-auth` 写入 WorkOS OIDC 配置。
- 工作流做成**幂等**：先检查目标预览分支是否已存在 WorkOS 配置，已配置则退出，避免重复写入；同时支持 `workflow_dispatch` 手动重试。
- 由于 Supabase 预览分支创建存在延迟，脚本采用最多 **5 次重试、每次间隔 10 秒** 的轮询方式等待分支可见。

## Results
- 文章声称实现了“**完全异步**”的代理 PR 测试流程：从分配工单、代理提交 PR，到评审者点击预览链接验证功能，全程**无需本地拉代码**。
- 每个 PR 获得**独立数据库分支**与**独立预览 URL**，作者强调这带来三点直接收益：并行测试、多代理无资源争用、以及避免污染 staging 数据库。
- 反馈回路被描述为“**minutes, not hours**（分钟级而不是小时级）”，但文中**没有提供正式实验数据、基准数据集或可复现指标**。
- 给出的最具体技术结果是：使用 Supabase Management API 的第三方认证配置接口，加上 **5×10 秒** 的轮询和幂等检查，就能把原本“部署成功但无法登录”的预览环境修复为“可完整登录和交互测试”的环境。
- 方法被宣称可推广到其他 **OIDC** 提供方，如 Auth0、Clerk 等；不过作者也明确表示**未亲自验证所有替代提供方**。

## Link
- [https://www.piersonmarks.com/posts/testing-agent-written-prs-in-the-cloud](https://www.piersonmarks.com/posts/testing-agent-written-prs-in-the-cloud)
