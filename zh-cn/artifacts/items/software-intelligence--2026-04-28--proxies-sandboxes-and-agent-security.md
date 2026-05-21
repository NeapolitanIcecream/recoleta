---
source: hn
url: https://www.gouthamve.dev/proxies-sandboxes-and-agent-security/
published_at: '2026-04-28T23:41:32'
authors:
- gouthamve
topics:
- agent-security
- credential-proxy
- sandboxing
- ai-sre
- prompt-injection
- gvisor
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# Proxies, Sandboxes and Agent Security

## Summary
## 摘要
这篇文章描述了一种实用的安全设计：让 AI SRE 管理家庭实验室，同时不把真实服务凭证暴露给 agent。方案使用凭证注入 HTTP 代理，并考虑用 gVisor 沙箱做更严格的网络控制。

## 问题
- SRE agent 需要访问 GitHub、Kubernetes、Grafana、Todoist、Matrix 和其他工具，这会带来凭证暴露风险。
- 网页或文档中的提示注入可能让 agent 读取密钥，并通过普通网络调用把密钥发出去。
- 在这个设置中，破坏性命令的严重性较低，因为 agent 运行在无 root 容器中，作者也把重要状态保存在 git 中。

## 方法
- 在 agent 容器内放入假凭证，例如 `fake-todoist-token`，并通过凭证代理路由 HTTP 和 HTTPS 流量。
- 配置代理，让它针对特定主机和请求头把假 token 替换为真实 token，例如 `api.todoist.com` 的 `Authorization` 和 `api.parallel.ai` 的 `x-api-key`。
- 将代理 CA 证书加入容器信任存储，使代理能够检查并改写 HTTPS 请求。
- 在基于 gVisor 的沙箱中使用域名允许或拒绝规则，在应用代理层下方拦截出站请求。

## 结果
- 文章没有报告定量基准结果、数据集或准确率指标。
- 文章没有声称取得突破性结果；最强的说法是，基于代理的 token 注入可以让真实凭证不进入 agent 容器。
- 该代理设计至少处理了 3 个示例服务的凭证注入：Todoist、Parallel 和 Matrix。
- 作者发现了 2 个具体的代理集成失败：使用 Playwright 的 Chrome 没有采用代理 CA，Matrix 客户端路径因为库行为没有遵守 `HTTP_PROXY`。
- gVisor 沙箱相关说法具体但未经过测量：它的 Go 网络栈可以拦截出站请求，即使应用忽略 `HTTP_PROXY`。

## Problem

## Approach

## Results

## Link
- [https://www.gouthamve.dev/proxies-sandboxes-and-agent-security/](https://www.gouthamve.dev/proxies-sandboxes-and-agent-security/)
