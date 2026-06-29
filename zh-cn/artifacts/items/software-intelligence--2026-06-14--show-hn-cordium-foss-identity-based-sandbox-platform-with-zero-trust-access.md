---
source: hn
url: https://github.com/octelium/cordium
published_at: '2026-06-14T22:47:53'
authors:
- geoctl
topics:
- kubernetes-sandbox
- zero-trust-access
- identity-based-auth
- ai-agent-workflows
- remote-development
relevance_score: 0.82
run_id: materialize-outputs
language_code: zh-CN
---

# Show HN: Cordium – FOSS identity-based sandbox platform with zero-trust access

## Summary
## 摘要
Cordium 是一个自托管的 Kubernetes 沙箱平台，面向开发者、AI 代理和 CI 任务。它把隔离工作区和基于身份、无密钥的内部系统访问结合在一起。

## 问题
- 远程开发机和代理沙箱仍然需要把密钥复制进工作区，才能访问 SSH、数据库和 API。
- 这会带来凭据扩散，也让访问控制更难审计。
- 团队还需要同一套环境同时支持交互式编码会话和短时自动化任务。

## 方案
- 在 Kubernetes 上把每个工作区运行成一个无 root 容器沙箱。
- 用 YAML 定义环境，包括镜像、仓库、任务、变量、端口和资源限制。
- 使用 Octelium 的身份感知代理和按请求的 ABAC 策略，在协议层授予访问权限，这样工作区不会接收到上游凭据。
- 支持浏览器终端、SSH、CLI 和 gRPC，也支持持久化或临时工作区。
- 使用预构建的 VolumeSnapshot 模板缩短重环境的启动时间。

## 结果
- 摘要里没有基准表或实测评估结果。
- 文中称，工作区可以访问 SSH 服务器、数据库、内部 HTTP API、Kubernetes 集群和 mTLS 服务，而不用把 API key、密码、SSH 私钥或 kubeconfig 放进沙箱。
- 文中称，预构建模板把冷启动时间从几分钟降到几秒。
- 它支持任何 Kubernetes 集群，从单节点 VM 到多节点生产部署，并为每个请求提供 OpenTelemetry 审计日志。

## Problem

## Approach

## Results

## Link
- [https://github.com/octelium/cordium](https://github.com/octelium/cordium)
