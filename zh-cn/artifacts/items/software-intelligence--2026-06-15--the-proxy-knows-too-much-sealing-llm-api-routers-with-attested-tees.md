---
source: arxiv
url: https://arxiv.org/abs/2606.16358v1
published_at: '2026-06-15T07:55:13'
authors:
- Sipeng Xie
- Qianhong Wu
- Hengrun Lu
- Ziliang Sun
- Qi Wu
- Bo Qin
- Qin Wang
topics:
- llm-api-router
- agent-security
- trusted-execution-environments
- remote-attestation
- code-agent-security
- api-gateway-security
relevance_score: 0.74
run_id: materialize-outputs
language_code: zh-CN
---

# The Proxy Knows Too Much: Sealing LLM API Routers with Attested TEEs

## Summary
## 摘要
Aegis 是一种基于已认证 TEE 的 LLM API 路由器，可让提示、工具调用、响应和密钥不进入路由器主机的明文内存。客户端在发送请求正文前验证 enclave，因此主机可以路由请求并计费，但不能读取或更改交互内容。

## 问题
- LLM API 路由器会终止客户端 TLS，并打开新的上游 TLS 会话，这使路由器能以明文访问提示、工具定义、工具输出、提供方响应和密钥。
- 恶意路由器可以改写编码代理的工具调用，将依赖替换为仿冒拼写的软件包，只在选定条件下触发攻击，或扫描流量以获取凭据。
- 这很重要，因为编码代理可能在开发者机器上执行 shell 命令并安装软件包，所以一次被篡改的工具调用就可能导致代码执行或供应链受损。

## 方法
- Aegis 只把请求/响应数据路径移入硬件 enclave。认证、调度、账户选择、计费和管理仍留在不可信主机上。
- 客户端 sidecar 在释放明文正文前检查 enclave 认证和度量值。
- 面向客户端的 TLS 在 enclave 内终止，enclave 会向固定且已度量的目标打开提供方 HTTPS 会话。
- 主机传递账户选择和提供方凭据等控制数据，但控制通道不能携带正文字节或主机选择的网络目标。
- enclave 转发提供方原生 API 字节，不转换请求或响应格式。

## 结果
- 在可访问明文的基线中，全部 4 类恶意路由器攻击都成功：工具调用改写、仿冒拼写的软件包替换、触发条件门控攻击和被动密钥外泄。
- Aegis 在作者的测试中阻止了全部 4 类攻击，包括针对同一信任边界的自适应测试。
- 受信任数据路径有 851 行代码。
- 该实现承载 3 个提供方原生 API，且不做格式转换。
- 在真实提供方工作负载和并发条件下，每个请求都通过已验证路径完成。
- 报告的本地中继开销约为每个请求 6 ms；在一个植入缺陷的审计试点中，两个通用编码代理分别找到了 8/10 和 10/10 个预置不变量违规。

## Problem

## Approach

## Results

## Link
- [https://arxiv.org/abs/2606.16358v1](https://arxiv.org/abs/2606.16358v1)
