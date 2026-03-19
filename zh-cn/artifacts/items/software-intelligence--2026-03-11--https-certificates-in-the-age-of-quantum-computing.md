---
source: hn
url: https://lwn.net/SubscriberLink/1060941/4878284e2c9f19ba/
published_at: '2026-03-11T23:11:17'
authors:
- firexcy
topics:
- post-quantum-cryptography
- https-certificates
- pki
- certificate-transparency
- merkle-trees
relevance_score: 0.18
run_id: materialize-outputs
language_code: zh-CN
---

# HTTPS certificates in the age of quantum computing

## Summary
本文讨论了 IETF 新工作组 PLANTS 如何为 HTTPS 认证与证书透明性引入后量子密码，同时避免证书因后量子签名而暴涨到不可接受的大小。核心思路是把证书从“签名链”改为“日志证明 + 观察者签名”，并用 Merkle 树把大部分连接中的证书体积显著压缩。

## Problem
- 现有 HTTPS 后量子化主要先解决密钥交换，但认证与证书透明性同样需要迁移，否则未来量子时代的 Web PKI 仍会受限。
- 后量子签名非常大：文中称 ML-DSA-44 的签名大小约为 Ed25519 的 **37 倍**，直接替换会让证书链大约变成当前的 **40 倍** 级别，增加带宽与连接时延。
- 传统证书链和证书透明日志存在信息重复；若继续沿用当前结构，切换到后量子认证会让小型网站的证书开销甚至超过网页内容本身。

## Approach
- PLANTS 提议让每个 CA 维护自己的**追加式签发日志**，由第三方观察者/镜像方监控其是否真正 append-only，并对日志检查点签名。
- 浏览器不再主要依赖“从站点到根 CA 的签名链”，而是验证：**CA/观察者对日志状态的签名 + 服务器证书被包含在日志中的证明**。
- 为降低单站点传输成本，系统区分两类证书：首次或未同步客户端使用较大的 **full certificate**；已见过某个检查点的客户端只需接收更小的 **signatureless certificate**。
- signatureless certificate 依赖 **Merkle 树包含证明**：CA 将大量证书批量放入树中，只需对树根签名一次；单个站点只发送从叶子到根的少量哈希路径，证明其证书已被签发。
- 由于哈希证明大小随树规模仅**对数增长**，且哈希不受与公钥签名同类的量子膨胀影响，这种设计对后量子证书尤其有利。

## Results
- 当前 LWN 的传统证书链约 **3.5KB**，已经约等于其首页压缩后 HTML 内容的 **1/3**；说明证书体积本就不可忽视。
- 文中称若采用 ML-DSA-44，单个签名约为 Ed25519 的 **37 倍**；直接切换到后量子证书会让整体证书链接近 **40 倍** 膨胀。
- 以 Let's Encrypt **每天约 600 万张证书**、每 **1 分钟** 一个检查点为例，单个站点的 Merkle 包含证明只需 **12 个 SHA-256 哈希**，总计 **384 字节**。
- 这 **384 字节** 仅相当于一枚 ML-DSA-44 签名大小的 **16%**，表明“signatureless certificate”可显著降低后量子认证的平均传输成本。
- 对于未缓存检查点的客户端，full certificate 仍然很大：文中估计使用 ML-DSA-44 时约 **133KB**，明显高于当前证书，但理想情况下只会用于少数连接。
- 该方案尚无公开大规模实测性能结果；当前最强的具体落地信号是 **Google 计划在 2027 年底前**在 Chrome 中实验并部署基于 PLANTS 草案的后量子 CA 系统，而广泛配置更新可能要到 **2029–2030 年**。

## Link
- [https://lwn.net/SubscriberLink/1060941/4878284e2c9f19ba/](https://lwn.net/SubscriberLink/1060941/4878284e2c9f19ba/)
