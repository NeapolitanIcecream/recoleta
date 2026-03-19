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
language_code: en
---

# Cloud VM benchmarks 2026: performance / price

## Summary
This is a cross-provider CPU performance and price/performance evaluation of 2026 cloud compute VMs, not a robotics/AI paper. The author conducted systematic benchmark testing across 7 cloud providers, 44 VM types, and multiple regions. The core conclusion is that AMD EPYC Turin is clearly ahead in high-end CPU performance.

## Problem
- The problem being addressed is that **CPU performance and performance per dollar** vary greatly across cloud providers, VM types, and regions, making it difficult for users to choose the most cost-effective instance.
- This matters because many workloads such as general compute, web services, and batch processing are affected by single-thread performance, multi-thread scalability, and price; choosing the wrong VM means **paying more money for worse performance**.
- Cloud instances also have issues such as mixed generations, regional variation, SMT vs. non-SMT differences, and uncertainty from shared cores, so official specifications are insufficient to reflect real-world performance.

## Approach
- The author compares **7 cloud providers and 44 VM types**, standardizing primarily on a **2 vCPU configuration** to compare performance and pricing at the smallest scalable purchasing unit.
- Testing covers **multiple regions** and records performance ranges (min/max), because the same instance may perform inconsistently across regions or host machines.
- The benchmark methodology is centered on the in-house **DKbench**, supplemented by **Geekbench 5, 7-zip, NGINX, FFmpeg/libx264, OpenSSL RSA4096** to observe single-thread performance, multi-thread performance, scalability, and behavior on specific workloads.
- On the pricing side, it compares **on-demand**, **1-year reserved**, **3-year reserved**, and **spot/preemptible** pricing, while trying to standardize RAM/disk configurations and emphasizing **performance/price** rather than just absolute performance.

## Results
- The main qualitative conclusion is that **AMD EPYC Turin is clearly ahead**: the author says this is the “first time a CPU has established such a clear advantage” in this comparison series, and notes that AWS's Turin offering is the fastest in single-thread performance, while AWS **C8a** “completely dominates” the charts in dual-thread/multi-thread results.
- On scalability, the author notes that most **ARM and shared-core instances are close to 100% scalability**; by contrast, when x86 2 vCPU corresponds to 1 SMT core, scalability is usually below 100%. The article gives one standout value: **Akamai's AMD Turin reaches 71.9% scalability**.
- In the NGINX benchmark, the author claims that **AWS C8a (non-SMT Turin) nearly reaches 2x the second-place result and about 3x C7a**, showing the advantage of the Turin + full physical core per vCPU combination.
- In OpenSSL RSA4096 (AVX512), the author says **both Turin and Genoa outperform all Intel CPUs**, and specifically notes that **Granite Rapids shows limited improvement over Ice Lake**; however, the excerpt does not provide specific throughput figures.
- In on-demand price/performance, the author says **Hetzner and Oracle rank at the top**; in multi-thread on-demand price/performance, **OCI ARM (AmpereOne M) leads**, followed by Hetzner and shared-core Linode. Among the major providers, the author considers **AWS to have the worst on-demand price/performance**, though the latest **Turin** is its best option.
- The article provides many charts and raw tables, but this excerpt **does not include a complete per-item numerical table**, so most results can only cite relative rankings, multiplicative comparisons, and the strongest quantitative statements in the text.

## Link
- [https://dev.to/dkechag/cloud-vm-benchmarks-2026-performance-price-1i1m](https://dev.to/dkechag/cloud-vm-benchmarks-2026-performance-price-1i1m)
