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
这篇文章描述了一种实用的安全设计，用来让 AI SRE 管理家庭实验室，同时不把真实服务凭据暴露给代理。它使用凭据注入 HTTP 代理，并考虑用 gVisor 沙箱做更严格的网络控制。

## 问题
- SRE 代理需要访问 GitHub、Kubernetes、Grafana、Todoist、Matrix 和其他工具，这会带来凭据暴露风险。
- 通过网页或文档进行提示注入，可能让代理读取密钥，并通过正常网络请求把它们发出去。
- 在这个设置里，破坏性命令的风险更低，因为代理运行在无 root 容器中，作者也把重要状态保存在 git 里。

## 方法
- 在代理容器里放入假凭据，例如 `fake-todoist-token`，并把 HTTP 和 HTTPS 流量转到凭据代理。
- 配置代理在特定主机和标头上，把假 token 替换成真实 token，例如 `api.todoist.com` 的 `Authorization` 和 `api.parallel.ai` 的 `x-api-key`。
- 把代理的 CA 证书加入容器信任存储，这样代理可以检查并改写 HTTPS 请求。
- 在基于 gVisor 的沙箱里使用允许或拒绝域名规则，在应用代理层之下拦截外发请求。

## 结果
- 文章没有给出定量基准结果、数据集或准确率指标。
- 文中没有声称有突破性结果；最强的说法是基于代理的 token 注入可以把真实凭据排除在代理容器之外。
- 这套代理设计至少处理了 3 个示例服务的凭据注入：Todoist、Parallel 和 Matrix。
- 作者发现了 2 个具体的代理集成故障：带 Playwright 的 Chrome 没有使用代理 CA，Matrix 客户端路径因为库行为没有遵守 `HTTP_PROXY`。
- 关于 gVisor 沙箱的说法很具体，但没有测量：即使应用忽略 `HTTP_PROXY`，它的 Go 网络栈也可以拦截外发请求。

## Problem

## Approach

## Results

## Link
- [https://www.gouthamve.dev/proxies-sandboxes-and-agent-security/](https://www.gouthamve.dev/proxies-sandboxes-and-agent-security/)
