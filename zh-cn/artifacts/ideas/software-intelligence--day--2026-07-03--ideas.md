---
kind: ideas
granularity: day
period_start: '2026-07-03T00:00:00'
period_end: '2026-07-04T00:00:00'
run_id: materialize-outputs
status: succeeded
topics:
- agent identity
- OAuth
- LLM agents
- credential security
- mTLS
tags:
- recoleta/ideas
- topic/agent-identity
- topic/oauth
- topic/llm-agents
- topic/credential-security
- topic/mtls
language_code: zh-CN
---

# 代理凭据隔离

## 摘要
企业代理安全工作可以围绕 token broker、API proxy 和绑定证书的代理凭据开展小范围试点。最清楚的起点是 broker-and-proxy 流程，用来阻止可复用 OAuth token 进入代理容器。已经发放工作负载证书的团队可以加入 mTLS 检查。SaaS 集成需要尽早测试 adapter，因为登录流程和不透明 token 会随提供方而变化。

## 面向电子邮件、日历和 GitHub 代理的 broker-and-proxy OAuth 流程
安全团队可以为需要访问电子邮件、日历、GitHub 或内部 API 的代理试点一个中心化 OAuth broker。broker 运行浏览器登录流程并接收真实的 OAuth token。它向代理发放一个已签名的 JWT，其中复制非机密 claim，并把真实 token 存为加密 claim。代理通过 proxy 发送 API 调用，proxy 验证 broker 签名，解密嵌入的 token，将其替换到 `Authorization` header 中，然后转发请求。

一个有用的首次测试范围应当很小：把这个流程放到一个高风险代理前面，并检测容器文件系统、工具输出、日志和仓库写入。通过条件是上游 OAuth token 从不出现在代理运行时中，同时代理仍能检查类似 scope 的 claim 并完成正常 API 调用。同一个试点还应记录延迟和失败模式，因为来源方案提供的是架构，而不是部署测量数据。

### 资料来源
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): 概述 broker 和 proxy 设计、目标服务，以及缺少定量部署数据这一点。
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): 描述由 broker 生成的 JWT，其中包含真实 token 的加密副本，以及 proxy 对 header 的替换。
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): 指出运营风险：代理持有的凭据可能被写入磁盘、提交到仓库，或被外泄。

## 面向 broker 发放的代理 token 的 mTLS 证书绑定
已经给代理工作负载发放客户端证书的团队，可以把 broker 发放的 JWT 绑定到代理环境。代理向 broker 请求 token 时出示客户端证书。broker 在 JWT 中嵌入该证书的一种表示。随后 proxy 要求 mTLS，并在解密真实 OAuth token 前检查当前客户端证书是否与嵌入的证书匹配。

实际的安全测试是把 broker 发放的 JWT 从一个代理环境复制出来，并尝试从另一个环境通过 proxy 使用它。预期结果是 proxy 拒绝请求，除非调用方也拥有原始环境的私钥。由硬件或 hypervisor 支持的私钥会让这项检查更有意义。即使上游身份提供方不支持 RFC 8705 token binding，也可以采用这种做法。

### 资料来源
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): 解释向 broker 出示客户端证书、把证书嵌入生成的 token，以及在 proxy 处强制执行 mTLS。
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): 将该设计关联到 SPIFFE 风格的工作负载身份，并指出 broker 和 proxy 可无状态运行。

## 面向第三方登录流程和不透明 access token 的 adapter 测试
把代理接入 GitHub 和其他 SaaS API 的团队，应在采用共享生产路径前测试 broker adapter。如果登录不经过企业身份提供方，broker 可能需要按提供方做专门处理。不透明 access token 也需要覆盖：broker 可以把不透明 token 作为加密 claim 包进新的 JWT，proxy 只有在 mTLS 检查通过后才出示该不透明 token。

一个实际的采用检查是建立提供方矩阵，覆盖登录流程、token 类型、claim 可见性、刷新行为、proxy header 重写和 mTLS 强制执行。GitHub 是很好的首个案例，因为来源指出了按提供方处理登录时的摩擦。让两三个常用 SaaS 服务通过这个矩阵，可以显示 broker 能否保持小规模，还是需要更大的 adapter 层。

### 资料来源
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): 指出第三方服务和 GitHub 风格的登录流程可能要求 broker 具备供应商特定知识。
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): 说明不透明 token 可以作为加密 claim 携带，并且只在 mTLS 绑定验证通过后释放。
