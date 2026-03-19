---
source: hn
url: https://dev.to/dkechag/cloud-vm-benchmarks-2026-performance-price-1i1m
published_at: '2026-03-07T22:36:51'
authors:
- yread
topics:
- cloud-benchmarking
- virtual-machines
- price-performance
- cpu-performance
- cloud-infrastructure
relevance_score: 0.21
run_id: materialize-outputs
language_code: zh-CN
---

# Cloud VM benchmarks 2026: performance / price

## Summary
这是一份跨 7 家云厂商、44 种 VM 类型的 2026 年 CPU 云主机性能/价格基准对比，重点回答“每花 1 美元能买到多少通用 CPU 性能”。核心结论是 AMD EPYC Turin 在顶级性能上显著领先，而不同云与实例在稳定性、SMT 配置和定价模型上会大幅改变性价比。

## Problem
- 采购云 VM 时，用户很难判断不同厂商、不同 CPU 代际、不同区域下的**真实 CPU 性能与性价比**，公开规格往往不足以说明实际表现。
- 同一实例类型在不同区域/节点上可能有**性能波动**，尤其是共享资源、boost 行为和 noisy neighbor 会影响稳定性。
- 对通用计算、Web 服务、批处理等场景，既要看**单线程速度**，也要看**2 vCPU 最小购买单元**下的多线程扩展和每美元产出，这直接影响部署成本与响应时间。

## Approach
- 作者在 2025 年 10 月起，对 **7 家云厂商、44 种 VM 类型**进行测试，统一聚焦 **2 vCPU 配置**，并尽量对齐 **2GB/vCPU 内存 + 30GB SSD** 的价格口径。
- 基准覆盖单线程与双线程，跨多个区域、多次创建实例，记录**最小/最大性能范围**，以反映区域差异和节点不一致性。
- 使用自建 **DKbench** 作为主指标，并辅以 **Geekbench 5、7-zip、NGINX、FFmpeg/libx264、OpenSSL RSA4096** 等公开/常见测试，覆盖通用计算、压缩、Web、视频编码和 AVX512 场景。
- 对比维度不仅包括**绝对性能**，还包括 **on-demand、1 年预留、3 年预留、spot/preemptible** 多种计费模式下的性能/价格。
- 机制上可简单理解为：先把不同云 VM 放到尽量一致的小规格条件下跑一组 CPU 任务，再把性能结果除以价格，比较“速度”和“每美元速度”。

## Results
- **顶级单线程性能**：作者称这是其系列测试中首次出现如此明显的领先者，**AMD EPYC Turin**“明显高出一个档次”；在云实现上，**AWS 的 Turin 配置最快**，而 **GCP C4d** 波动较大，**GCP N4d** 更稳定。
- **多线程/扩展性**：非 SMT 或每 vCPU 对应完整核心的实例接近 **100% scalability**；文中点名 **AWS C7a、AWS C8a、GCP t2d** 可达到这种“2 个 vCPU≈2 个完整核心”的效果。一个异常点是 **Akamai 的 AMD Turin 扩展率达 71.9%**，高于常见 SMT 预期，但单线程又偏低。
- **DKbench 双线程绝对性能**：给最快 CPU 再配上“2 个完整核心”后，**AWS C8a（Turin）完全统治图表**；作者还称其在 **NGINX 100 连接**测试中，**几乎是第二名的 2 倍、C7a 的 3 倍**。
- **ARM 表现**：**Google Axion** 被描述为 ARM 阵营的高性能代表，单线程约达 **EPYC Genoa 级别**；多线程上它“至少与上一年领先者 Genoa C7a 相当”，**Graviton4** 很接近，**Azure Cobalt 100** 略落后但在若干性价比图中表现很强。
- **专项测试**：在 **7-zip 解压**中，**Axion、Graviton4 甚至可超过 Turin**，而 **Cobalt 100 是解压项第一**；在 **OpenSSL RSA4096/AVX512** 中，作者称 **Turin 和 Genoa 都领先 Intel**，且 **Granite Rapids 相比 Ice Lake 提升不大**。
- **性能/价格**：按需计费下，作者称 **Hetzner 与 Oracle** 继续领跑单线程性价比，而在多线程按需图中 **OCI ARM（尤其 AmpereOne M）居首**；**1 年预留**下 **GCP Turin** 可追平 Oracle 顶部价值；**3 年预留多线程**下 **Azure Cobalt 100 登顶**；**Spot** 下单线程最佳价值来自 **GCP/Azure 深折扣与 OCI 固定 50% 折扣**，而**多线程 Spot 第一是 Azure Cobalt 100**。文中未提供完整结构化表格数字，但给出了这些明确的排名与相对倍数结论。

## Link
- [https://dev.to/dkechag/cloud-vm-benchmarks-2026-performance-price-1i1m](https://dev.to/dkechag/cloud-vm-benchmarks-2026-performance-price-1i1m)
