---
source: hn
url: https://blog.postman.com/postman-passport-secure-api-access-for-the-agentic-era/
published_at: '2026-06-23T23:23:22'
authors:
- paidsandserape
topics:
- api-security
- agentic-sdlc
- secret-management
- credential-broker
- secure-proxy
relevance_score: 0.66
run_id: materialize-outputs
language_code: zh-CN
---

# Postman launches passport for securing API secret access

## Summary
## 摘要
Postman Passport 是一种产品设计，让人、机器和代理在调用 API 时无需接收原始 API 密钥。它的重要性在于，编码代理和 CI 工作负载会放大 API 调用量，并让密钥暴露扩散到开发者机器和工具中。

## 问题
- API 密钥会被复制到 `.env` 文件、shell 配置文件、IDE 配置、构建输出、Slack、Google Docs 和工具缓存中；Postman 称，每个仍在使用的密钥平均会出现在同一台机器的大约 8 个位置。
- SDLC 中的代理可以调用 API，也可以生成其他代理，因此直接访问密钥会带来泄露和权限过大的风险。
- 现有密钥库通常保护生产系统，而开发者和代理访问往往在本地机器或应用运行时解析密钥。

## 方法
- Passport 向调用方提供凭证引用，而不是 API 密钥；每个引用都通过加密令牌和私钥绑定到持有者。
- 访问请求经过 Postman API Network，后者连接到客户的密钥库；真实密钥保留在密钥库中。
- API 请求通过客户 VPC 内的 Secure Access Proxy 路由；代理检查作用域、解析密钥、将密钥注入请求，并让密钥不进入应用、日志和 Postman。
- 持久身份跟踪寿命较长的使用方，临时身份让代理把短期的子集访问权限委托给生成的代理。
- Secure Access Proxy 可以在原始 API 权限集之外执行端点级作用域控制。

## 结果
- 摘录没有提供基准测试、用户研究、事件减少数据、延迟数据或生产部署数量。
- 声称的需求驱动因素：预计代理消耗 API 的速率将达到当前人类的 1000 倍。
- 密钥扩散测量：每个仍在使用的密钥平均会出现在同一台机器的大约 8 个位置。
- 安全声明：被盗的凭证引用如果没有匹配的持有者私钥，就无法使用。
- 部署声明：信任根是客户的证书颁发机构，密钥解析在客户的 VPC 内运行。
- 控制声明：代理在每个请求到达密钥库之前检查作用域，并可执行端点级访问控制。

## Problem

## Approach

## Results

## Link
- [https://blog.postman.com/postman-passport-secure-api-access-for-the-agentic-era/](https://blog.postman.com/postman-passport-secure-api-access-for-the-agentic-era/)
