---
kind: trend
trend_doc_id: 1738
granularity: day
period_start: '2026-07-03T00:00:00'
period_end: '2026-07-04T00:00:00'
topics:
- agent identity
- OAuth
- LLM agents
- credential security
- mTLS
run_id: materialize-outputs
aliases:
- recoleta-trend-1738
tags:
- recoleta/trend
- topic/agent-identity
- topic/oauth
- topic/llm-agents
- topic/credential-security
- topic/mtls
language_code: zh-CN
---

# 代理身份工作聚焦于让 OAuth token 离开 LLM 运行时

## Overview
这一天有一个强信号：企业 LLM 代理需要委托访问，但不能让可复用的 OAuth token 留在运行时中。`Securing Agentic Identity` 提出了一种用于邮件、日历、GitHub 和 API 访问的 broker、代理服务器和双向 TLS (mTLS) 绑定模式。证据来自架构设计，目前还没有基准测试或部署数据。

## Clusters

### 用于代理 API 访问的 broker 托管 token
该提案在用户登录和代理运行时之间放置一个 broker。用户通过浏览器完成认证后，broker 接收真实的 OAuth token，然后向代理发放一个已签名的 JSON Web Token (JWT)。这个 JWT 只把真实 token 放在一个加密 claim 中。代理可以查看复制过来的非敏感 claim，但远程服务接受的凭据不会进入代理环境。

代理通过代理服务器发送 API 调用。代理服务器验证 broker 签名，解密嵌入的 token，把它替换进 `Authorization` header，然后转发请求。这个设计针对一种实际故障模式：有权访问邮件、日历或源代码控制 API 的代理，可能把 token 写入磁盘、通过工具泄露 token，或把 token 提交到代码仓库。

#### Evidence
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): 摘要描述了 broker、代理服务器、加密的 JWT claim 和目标服务。

### mTLS 绑定限制被盗 token 的复用
更强的版本把 broker 发放的 JWT 绑定到代理环境的客户端证书。代理在请求 token 时出示证书。broker 把该证书记录在新铸造的 JWT 中。之后，代理服务器要求 mTLS，并在解密嵌入的 token 前检查当前客户端证书是否匹配。

这样一来，除非攻击者也控制该环境的私钥，否则窃取 token 的价值会降低。文章建议尽可能使用硬件支持或虚拟机管理程序支持的私钥。文章还指出，即使上游身份提供方不支持 RFC 8705 token 绑定，这种模式也可以工作。

#### Evidence
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): 内容描述了证书嵌入、代理服务器的 mTLS 检查，以及硬件或虚拟机管理程序支持的密钥。

### 无状态运行、供应商摩擦和缺失的测量数据
这个方案的运维吸引力在于，broker 和代理服务器不需要持久化的 token 映射数据库。它们需要签名密钥和加密密钥，并且可以启动新实例来扩展容量或提高可用性。这会降低占位 token 方案演变成分布式密钥存储的可能性。

限制也很明确。第三方服务可能使用不同的登录流程或不透明 token，因此 broker 可能需要按供应商分别处理。文章没有给出延迟、可靠性、事故或部署规模方面的测量数据。它的贡献是一套面向 agentic identity 的具体安全设计，没有给出经过测量的系统结果。

#### Evidence
- [Securing Agentic Identity](../Inbox/2026-07-03--securing-agentic-identity.md): 内容说明了无状态扩展这一主张，并引用了 Fly.io 的类似早期工作。
