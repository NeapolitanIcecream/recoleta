---
source: hn
url: https://codon.org.uk/~mjg59/blog/p/securing-agentic-identity/
published_at: '2026-07-03T23:38:15'
authors:
- edward
topics:
- agent-identity
- oauth-security
- llm-agents
- mtls
- credential-management
- enterprise-security
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Securing Agentic Identity

## Summary
## 摘要
这篇文章提出了一种令牌代理和代理转发设计，用来让真实的 OAuth 令牌离开 LLM agent 环境。它面向需要访问电子邮件、日历、GitHub 或其他 API 的企业 agent，同时避免把可重复使用的凭据留在磁盘上。

## 问题
- LLM agent 经常会获得敏感服务的访问令牌，这些令牌可能被写入磁盘、提交到代码仓库，或被外泄。
- 常见的设备代码登录让身份提供方很难了解 agent 主机的安全状态。
- 简单的占位令牌代理设计可能需要一个用于令牌映射的密钥存储；如果代理被攻破，被盗的占位令牌可能变成可用的访问权限。

## 方法
- 中央 broker 运行用户登录流程，并在浏览器认证后接收真实令牌。
- broker 向 agent 返回一个新的 JWT，由 broker 签名；真实令牌作为加密声明存储，非机密声明被复制出来，供本地检查。
- agent 通过代理调用 API，并在 `Authorization` 头中携带该 JWT；代理验证 broker 签名，解密真实令牌，然后在转发请求前替换该请求头。
- 该设计加入 mTLS 绑定：agent 出示客户端证书，broker 将该证书记录到新签发的 JWT 中，代理在解密嵌入的令牌前检查实时 mTLS 证书是否匹配。
- 同一模式也适用于不透明访问令牌：把不透明令牌加密后放入 broker 签发的 JWT 中。

## 结果
- 文章没有提供定量评估：没有基准测试、延迟数据、事故数据或部署规模测量。
- 主要的安全主张是，真实访问令牌永远不会进入 agent 环境。
- 主要的运维主张是无状态扩展：broker 和代理需要加密密钥，但不需要持久化的令牌映射数据库或分布式密钥存储。
- mTLS 变体声称通过把令牌使用绑定到 agent 环境的私钥来加强限制；理想情况下，该私钥由硬件或 hypervisor 支持。
- 文章引用 RFC 8705，并称 Fly.io 在约 3 年前有过类似想法，因此作者把这项贡献描述为针对 agentic identity 的实践改造，而不是全新的协议。

## Problem

## Approach

## Results

## Link
- [https://codon.org.uk/~mjg59/blog/p/securing-agentic-identity/](https://codon.org.uk/~mjg59/blog/p/securing-agentic-identity/)
