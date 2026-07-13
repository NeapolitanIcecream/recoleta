---
source: hn
url: https://www.iroh.computer/blog/mesh-llm
published_at: '2026-07-11T22:38:57'
authors:
- tionis
topics:
- software-foundation-model
- code-intelligence
- automated-software-production
- agent-network
- multi-agent-software-engineering
- human-ai-interaction
relevance_score: 0.84
run_id: materialize-outputs
language_code: zh-CN
---

# Mesh LLM: distributed AI computing on iroh

## Summary
## 摘要
Mesh LLM 将受信任的 iroh 连接机器上的 GPU 汇集起来，并通过一个兼容 OpenAI 的本地 API 提供服务。它可以在本地运行模型，将请求路由到对等节点，也可以对超过单台机器内存容量的模型进行流水线处理。

## 问题
- 托管式 LLM 限制了团队对模型版本、数据位置、硬件、隐私和运行成本的控制。
- 许多团队拥有分散的 GPU，却无法将它们作为一个系统共同运行更大的模型。

## 方法
- 每台机器运行一个由公钥标识的 iroh 端点，通过经过身份验证的 QUIC 连接通信，并支持 NAT 穿透和中继回退。
- Gossip 层负责管理对等节点准入、信任、版本兼容性、模型发现和路由。
- 请求可以在本地运行，也可以路由到已加载模型的对等节点，或者按层范围拆分模型，在多台机器上的流水线阶段中运行。
- 插件运行时通过 MCP、HTTP、推理和 mesh 事件提供模型与服务能力，同时在 `http://localhost:9337/v1` 提供标准 API。

## 结果
- 模型目录包含 40 多个模型，范围从可在笔记本电脑上运行的 0.5B 参数模型，到 235B 参数的混合专家模型。
- 软件包大小约为 18 MB，支持公共或私有 mesh 部署。
- 位于不同区域的两个 iroh 中继在对等节点无法直接连接时提供回退连接。
- 摘录未提供延迟、吞吐量、成本、可靠性或模型质量的基准测试结果。
- 摘录中得到最充分证明的是功能性结论：多台配置一般的机器可以通过流水线运行单台机器无法容纳的模型，同时标准 OpenAI 客户端仍可使用本地 API。

## Problem

## Approach

## Results

## Link
- [https://www.iroh.computer/blog/mesh-llm](https://www.iroh.computer/blog/mesh-llm)
