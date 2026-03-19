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
language_code: en
---

# Cloud VM benchmarks 2026: performance / price

## Summary
This is a 2026 CPU cloud VM performance/price benchmark comparison spanning 7 cloud providers and 44 VM types, focused on answering: “How much general-purpose CPU performance can you buy for every $1 spent?” The core conclusion is that AMD EPYC Turin has a clear lead in top-end performance, while differences in cloud platforms, instance stability, SMT configuration, and pricing models can significantly change value for money.

## Problem
- When purchasing cloud VMs, users find it difficult to judge the **real CPU performance and price/performance** across different providers, CPU generations, and regions; published specs are often insufficient to explain actual results.
- The same instance type may show **performance variance** across regions or nodes, especially because shared resources, boost behavior, and noisy neighbors can affect consistency.
- For workloads such as general computing, web services, and batch processing, it is necessary to look at both **single-thread speed** and multi-thread scaling and output per dollar under the **2 vCPU minimum purchase unit**, which directly affects deployment cost and response time.

## Approach
- Starting in October 2025, the author tested **44 VM types across 7 cloud providers**, consistently focusing on **2 vCPU configurations** and aligning prices as much as possible to **2GB/vCPU memory + 30GB SSD**.
- The benchmarks cover single-thread and dual-thread performance, with repeated instance creation across multiple regions, recording the **minimum/maximum performance range** to reflect regional differences and node inconsistency.
- A custom **DKbench** is used as the main metric, supplemented by public/common tests such as **Geekbench 5, 7-zip, NGINX, FFmpeg/libx264, OpenSSL RSA4096**, covering general compute, compression, web, video encoding, and AVX512 scenarios.
- The comparison dimensions include not only **absolute performance**, but also performance/price under multiple billing models: **on-demand, 1-year reserved, 3-year reserved, and spot/preemptible**.
- In simple terms, the method is: run a set of CPU tasks on different cloud VMs under as similar a small-instance configuration as possible, then divide the performance results by price to compare both “speed” and “speed per dollar.”

## Results
- **Top single-thread performance**: The author says this is the first time in the series that there is such a clear leader, with **AMD EPYC Turin** “clearly in a higher tier”; among cloud implementations, **AWS’s Turin configuration is the fastest**, while **GCP C4d** shows larger variance and **GCP N4d** is more stable.
- **Multi-threading/scalability**: Instances without SMT, or where each vCPU maps to a full core, come close to **100% scalability**; the article specifically highlights **AWS C7a, AWS C8a, and GCP t2d** as achieving the effect that “2 vCPUs ≈ 2 full cores.” One outlier is **Akamai’s AMD Turin**, whose scalability reaches **71.9%**, above common SMT expectations, but with relatively low single-thread performance.
- **DKbench dual-thread absolute performance**: Pairing the fastest CPU with “2 full cores,” **AWS C8a (Turin) completely dominates the chart**; the author also says that in the **NGINX 100 connections** test, it is **nearly 2× the second place and 3× C7a**.
- **ARM performance**: **Google Axion** is described as the high-performance representative of the ARM camp, with single-thread performance roughly at the **EPYC Genoa** level; in multi-threading, it is “at least on par with last year’s leader, Genoa C7a,” while **Graviton4** is very close and **Azure Cobalt 100** is slightly behind but performs strongly in several price/performance charts.
- **Specialized tests**: In **7-zip decompression**, **Axion and Graviton4 can even surpass Turin**, while **Cobalt 100 ranks first in decompression**; in **OpenSSL RSA4096/AVX512**, the author says **both Turin and Genoa outperform Intel**, and **Granite Rapids shows limited gains over Ice Lake**.
- **Performance/price**: Under on-demand pricing, the author says **Hetzner and Oracle** continue to lead in single-thread value, while in the multi-thread on-demand chart **OCI ARM (especially AmpereOne M)** ranks first; under **1-year reserved**, **GCP Turin** can match Oracle at the top of the value rankings; under **3-year reserved multi-thread**, **Azure Cobalt 100 takes the top spot**; under **Spot**, the best single-thread value comes from **deep discounts on GCP/Azure and OCI’s fixed 50% discount**, while **the top multi-thread Spot option is Azure Cobalt 100**. The article does not provide a complete structured table of numbers, but it does give these clear ranking and relative-multiple conclusions.

## Link
- [https://dev.to/dkechag/cloud-vm-benchmarks-2026-performance-price-1i1m](https://dev.to/dkechag/cloud-vm-benchmarks-2026-performance-price-1i1m)
