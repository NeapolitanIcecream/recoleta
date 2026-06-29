---
source: hn
url: https://www.obsidiansecurity.com/blog/litellm-privilege-escalation-rce
published_at: '2026-06-11T23:54:00'
authors:
- 13ph03nix
topics:
- llm-security
- ai-gateway
- privilege-escalation
- remote-code-execution
- route-authorization
- agent-security
relevance_score: 0.94
run_id: materialize-outputs
language_code: zh-CN
---

# Breaking LiteLLM: From Low-Privilege User to Admin and RCE

## Summary
## 摘要
Obsidian Security 报告了 LiteLLM 中一条 CVSS 9.9 的利用链：默认低权限用户可以进入管理员路由，随后拿到服务器端代码执行。这个问题很重要，因为 LiteLLM 位于代理和模型提供方之间，攻陷后可以改写代理行为、泄露密钥，并把动作推进到下游工具中。

## 问题
- LiteLLM 对调用方提供的路由权限和角色检查方式存在问题，导致一个密钥可以获得超出调用方自身角色的访问权限。
- 一些管理员处理程序只信任路由检查，然后接受危险字段或可执行代码，没有再做第二次授权检查。
- 网关被攻陷后，可能泄露管理员凭据、解密密钥，并控制代理与其模型之间的流量。

## 方法
- 研究人员梳理了 LiteLLM 在密钥生成、路由检查、用户更新和 guardrail 端点上的授权流程。
- 他们发现 `allowed_routes` 的值会按原样存储，而且可以扩大访问范围，而不是只收窄访问范围。
- 他们证明，`/key/generate` 和相关的密钥写入端点允许内部用户创建一个带有 `allowed_routes: ["/*"]` 的密钥，然后访问仅管理员可用的路由。
- 在进入管理员路由后，他们把链路接到 `/guardrails` 或 `/guardrails/test_custom_code` 做代码执行，再接到 `/user/update` 或 `/user/bulk_update` 做权限提升。
- 他们还指出，LiteLLM 对 MCP stdio 的支持让 proxy admin 可以通过子进程启动直接进入执行路径。

## 结果
- 这条完整利用链的评分是 CVSS 9.9，可以拿到管理员访问权限，并在 LiteLLM 服务器上执行任意代码。
- CVE-2026-47101 覆盖了通过 `allowed_routes` 绕过路由授权的问题。
- CVE-2026-47102 覆盖了通过自我更新路径写入 `user_role: "proxy_admin"` 的权限提升问题。
- CVE-2026-40217 覆盖了在 `exec()` 且 `__builtins__` 可用时的 guardrail 代码执行问题。
- BerriAI 在后续版本中发布了修复，完整链路在 2026-04-25 发布的 LiteLLM v1.83.14-stable 中被关闭。
- 摘要没有给出基准测试式性能数据；它的量化信息是 CVSS 分数、CVE ID、端点名称和发布版本。

## Problem

## Approach

## Results

## Link
- [https://www.obsidiansecurity.com/blog/litellm-privilege-escalation-rce](https://www.obsidiansecurity.com/blog/litellm-privilege-escalation-rce)
