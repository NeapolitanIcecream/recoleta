---
source: hn
url: https://dev.to/dkechag/cloud-vm-benchmarks-2026-performance-price-1i1m
published_at: '2026-03-07T22:36:51'
authors:
- yread
topics:
- cloud-benchmarks
- virtual-machines
- cpu-performance
- price-performance
- cloud-instances
relevance_score: 0.02
run_id: materialize-outputs
language_code: zh-CN
---

# Cloud VM benchmarks 2026: performance / price

## Summary
这是一篇针对 2026 年云计算虚拟机的跨厂商 CPU 性能与性价比评测，而非机器人/AI 论文。作者在 7 家云厂商、44 类 VM、多个区域上做了系统基准测试，核心结论是 AMD EPYC Turin 在高端 CPU 性能上明显领先。

## Problem
- 要解决的问题是：不同云厂商、不同 VM 类型、不同区域之间，**CPU 性能与每美元性能**差异很大，用户很难选到最划算的实例。
- 这很重要，因为通用计算、Web 服务、批处理等大量工作负载都受单线程性能、多线程扩展性和价格影响，选错 VM 会出现**花更多钱、拿更差性能**。
- 云厂商实例还存在代际混杂、区域波动、SMT/非 SMT 差异、共享核不确定性等问题，官方规格不足以反映真实表现。

## Approach
- 作者对 **7 家云厂商、44 种 VM 类型**进行对比，重点统一到 **2 vCPU 配置**，以便比较最小可扩展购买单元下的性能和价格。
- 测试覆盖**多个区域**，并记录性能范围（min/max），因为同一实例在不同区域或不同宿主机上可能表现不一致。
- 基准方法以自研 **DKbench** 为主，并辅以 **Geekbench 5、7-zip、NGINX、FFmpeg/libx264、OpenSSL RSA4096**，分别观察单线程、多线程、扩展性和特定负载表现。
- 价格维度同时比较 **按需(on-demand)**、**1 年预留**、**3 年预留**和 **spot/preemptible**，并尽量统一 RAM/磁盘配置，强调**性能/价格**而非仅绝对性能。

## Results
- 定性主结论是 **AMD EPYC Turin 明显领先**：作者称其是该系列比较里“第一次有 CPU 形成如此清晰优势”，并指出 AWS 的 Turin 方案在单线程上最快，AWS **C8a** 在双线程/多线程图中“完全统治”榜单。
- 在扩展性上，作者指出多数 **ARM 和共享核实例接近 100% scalability**；而 x86 的 2 vCPU 若对应 1 个 SMT 核心，扩展性通常低于 100%。文中给出一个异常值：**Akamai 的 AMD Turin 可达 71.9% scalability**。
- 在 NGINX 基准中，作者声称 **AWS C8a（非 SMT 的 Turin）几乎达到第二名的 2 倍，并约为 C7a 的 3 倍**，体现出 Turin + 每 vCPU 给满物理核的组合优势。
- 在 OpenSSL RSA4096（AVX512）中，作者称 **Turin 和 Genoa 都超过所有 Intel**，并特别指出 **Granite Rapids 相比 Ice Lake 提升不大**；但文段未给出具体吞吐数值。
- 在按需性价比上，作者称 **Hetzner 与 Oracle 位居最前列**；在多线程按需性价比中，**OCI ARM（AmpereOne M）领先**，Hetzner 与共享核 Linode 紧随其后。对于大厂，作者认为 **AWS 按需性价比最差**，但最新 **Turin** 是其最佳选择。
- 文章提供了大量图表和原始表格，但本摘录**没有给出完整的逐项数值表**，因此多数结果只能引用相对排名、倍数关系和文中最强定量描述。

## Link
- [https://dev.to/dkechag/cloud-vm-benchmarks-2026-performance-price-1i1m](https://dev.to/dkechag/cloud-vm-benchmarks-2026-performance-price-1i1m)
