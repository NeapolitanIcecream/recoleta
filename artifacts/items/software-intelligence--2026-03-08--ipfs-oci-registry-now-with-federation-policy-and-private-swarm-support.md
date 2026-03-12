---
source: hn
url: https://github.com/fbongiovanni29/ipfs-oci-registry
published_at: '2026-03-08T23:45:56'
authors:
- noobernetes
topics:
- container-registry
- ipfs
- oci-images
- p2p-distribution
- federation
relevance_score: 0.36
run_id: materialize-outputs
---

# IPFS OCI Registry – now with federation policy and private swarm support

## Summary
这是一个基于 IPFS 的去中心化 OCI 容器镜像注册表，支持联邦共享、拉取代理缓存、私有 swarm 和按策略共享镜像。项目已归档，其最大价值在于验证了架构可行，但也通过基准测试证明 IPFS 不适合作为大规模容器镜像传输层。

## Problem
- 论文要解决的是**容器注册表中心化带来的瓶颈**：如 Docker Hub 限流、云厂商锁定、跨区域重复传输、隔离环境下复杂镜像同步。
- 它关注的问题之所以重要，是因为容器镜像是现代软件交付的基础设施；如果分发依赖中心服务，成本、可用性与部署灵活性都会受限。
- 还试图解决**跨组织/跨区域自动共享缓存**的问题，希望镜像“拉取一次，到处可用”，减少重复下载与运维协调。

## Approach
- 核心方法很简单：把 OCI registry 做成一个**pull-through proxy + IPFS 缓存层**。第一次从 Docker Hub/GHCR 等上游拉取镜像后，将 blob 存入 IPFS，并记录 digest→CID 映射；之后其他节点可直接从 IPFS 获取。
- 通过 **SHA256 digest 校验内容**，不需要信任来源节点，只需要信任哈希；若字节不匹配就拒绝内容。
- 通过 **联邦机制**在节点间广播和查询 digest→CID 映射：本地查不到时先问 IPFS peers，再决定是否回源到上游 registry。
- 通过 **federation policy + private-by-default** 控制共享范围：专有镜像默认不共享，只有显式标记（如 `public/`）才在联邦中传播；也支持仅企业内部节点互联的私有 IPFS swarm。
- 工程上提供了可部署能力：Helm、DaemonSet 全去中心化模式、健康检查、鉴权、限流、GC、stale-while-revalidate、Prometheus 指标等。

## Results
- 作者声称系统实现完整且可用：支持 **7 个上游 registry** 的 pull-through proxy、**18 个自定义 Prometheus 指标**，并有 **60+ 测试**覆盖存储、处理器、健康检查、鉴权、限流、TTL、指标、配置和上游客户端。
- 关键实验结论是：**对于真实世界镜像，IPFS 比 CDN 慢 3–12 倍**；只有在**很小镜像**场景下，IPFS 才可能因网络往返主导而表现更好。
- 作者明确指出性能瓶颈来自 IPFS Bitswap：以 **256KB block** 交换，并带有逐块协商开销；这种机制适合 DAG 遍历，不适合大文件顺序流式传输。
- 论文没有给出更细粒度的公开 benchmark 表格（如具体吞吐/延迟/数据集明细），但最强定量主张是 **“真实镜像 3–12x slower than a CDN”**。
- 结论上的“突破”不在于性能超过现有方案，而在于**负面结果**：证明“IPFS 作为容器镜像分发传输层”在规模化场景下方向错误，同时保留了可迁移的 registry/federation 架构，作者进一步提出 **BitTorrent + DHT** 可能是更合适的替代方案。

## Link
- [https://github.com/fbongiovanni29/ipfs-oci-registry](https://github.com/fbongiovanni29/ipfs-oci-registry)
