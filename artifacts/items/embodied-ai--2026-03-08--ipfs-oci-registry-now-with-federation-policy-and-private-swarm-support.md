---
source: hn
url: https://github.com/fbongiovanni29/ipfs-oci-registry
published_at: '2026-03-08T23:45:56'
authors:
- noobernetes
topics:
- decentralized-registry
- ipfs
- container-images
- federation
- content-addressing
relevance_score: 0.03
run_id: materialize-outputs
---

# IPFS OCI Registry – now with federation policy and private swarm support

## Summary
这是一个把 OCI 容器镜像注册表构建在 IPFS 之上的去中心化联邦系统：首次从上游拉取并缓存到 IPFS，之后可由联邦节点复用分发。项目证明了这种架构在功能上可行，但基准测试显示 IPFS 不适合大规模容器镜像传输，因此作者已停止继续开发。

## Problem
- 目标问题是解决中心化容器注册表带来的瓶颈，如 Docker Hub 限流、云厂商锁定、跨区域重复传输，以及离线/隔离环境下复杂的镜像镜像同步。
- 作者关注的核心意义在于：如果镜像能像内容寻址对象一样自分发，企业之间或多区域节点就能减少对单一中心源的依赖。
- 同时它也试图解决跨组织、跨云、私有网络中的镜像共享与验证问题，并用哈希校验替代对来源的信任。

## Approach
- 核心机制很简单：把注册表做成 pull-through proxy，客户端按 tag 或 digest 拉镜像；若本地没有，就先问 IPFS 联邦节点，再从 Docker Hub/GHCR 等上游抓取，并把镜像 blob 存入 IPFS，得到 CID 后广播给其他节点。
- 系统维护 digest→CID 映射，本地用 BoltDB 查询；内容通过 SHA256 digest 验证，字节不匹配就拒绝，因此不必信任提供方，只信任哈希。
- 联邦通过 IPFS pubsub 发现“谁有这个镜像”，并支持 private-by-default 策略：私有镜像默认不共享，只有显式选择的内容才进入联邦传播。
- 为企业内部场景加入 private swarm 支持，使节点仅与自家节点互联，从而在 AWS/GCP/Azure/on-prem 之间复制镜像而不经过公共互联网。
- 工程上实现了 Helm 部署、DaemonSet 全去中心化模式、健康检查、认证、限流、Tag TTL、GC、18 个 Prometheus 指标，以及 60+ 测试来验证可用性。

## Results
- 作者声称实现了一个**完整可运行**的系统：支持 **7 个上游注册表** 的 pull-through proxy、IPFS pubsub 联邦、私有 swarm、策略控制、Web UI 和监控等功能。
- 测试覆盖方面，项目给出 **60+ tests**，覆盖 storage、handlers、health、auth、rate limiting、tag TTL、metrics、config 和 upstream client。
- 关键定量结论是性能：基准测试表明，**对真实世界规模镜像，IPFS 比 CDN 慢 3-12 倍**；只有在**很小镜像**上，网络往返时延主导时 IPFS 才占优。
- 作者给出的原因是 IPFS Bitswap 采用 **256KB blocks**，并且存在逐块协商开销；这种机制适合 DAG 遍历，不适合大文件顺序流式传输。
- 论文/项目最强的“负结果”是：尽管理论上多节点做种可带来网络效应，但当只有 **1 个 seeder** 时，本质上只有“一条管道”，效果与 HTTP 类似，难以形成正反馈规模效应。
- 最终结论不是 IPFS 方案胜出，而是架构层面（OCI handler、federation policy、digest→content-ID mapping）有效，但**传输层应替换为 BitTorrent+DHT** 这类更适合大文件分发的协议。

## Link
- [https://github.com/fbongiovanni29/ipfs-oci-registry](https://github.com/fbongiovanni29/ipfs-oci-registry)
