---
source: hn
url: https://creativestrategies.com/research/m5-max-chiplets-thermals-and-performance-per-watt/
published_at: '2026-03-09T23:08:58'
authors:
- zdw
topics:
- chiplet-design
- performance-per-watt
- laptop-soc
- thermal-efficiency
- on-device-ai
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# M5 Max: Chiplets, Thermals, and Performance per Watt

## Summary
This article argues that, through a truly chiplet-based design, the M5 Max improves performance, energy efficiency, thermal behavior, and potential manufacturing economics in a laptop SoC at the same time. The author’s core judgment is that it may be the strongest laptop SoC available today, and that it is especially outstanding in AI and performance per watt.

## Problem
- Traditional large monolithic SoCs on advanced process nodes face declining yields, more discarded dies, and rising manufacturing costs.
- When CPU, GPU, and other modules share a single piece of silicon, thermal coupling limits sustained performance and efficiency under simultaneous heavy load.
- Laptop chips need to balance high performance, low power consumption, all-day battery life, and on-device AI inference, which is difficult to achieve simultaneously.

## Approach
- M5 Pro/Max adopts a more “true” chiplet approach: separating the **CPU-dominant tile** and **GPU-dominant tile**, then combining them into a single package through more advanced packaging (SoIC-MH hybrid bonding).
- Apple appears to reuse the same CPU tile across M5 Pro and M5 Max (18-core CPU, Neural Engine, media blocks), and mainly differentiates the products with different GPU tiles, improving yield, reducing R&D/validation costs, and increasing flexibility in GPU binning.
- This split is not only a manufacturing strategy, but also improves thermal design: the CPU and GPU reside on different dominant tiles, reducing thermal crosstalk and allowing both to run higher and longer under simultaneous heavy load.
- In CPU architecture, M5 Pro/Max appears to remove efficiency cores, replacing them with **6 super cores + 12 performance cores**; the article speculates that Apple prefers to run big cores in lower-power ranges to take over part of the traditional e-core role.
- For AI, the author believes the M5 Max’s gains mainly come from the GPU neural acceleration path and slightly higher memory bandwidth; the ANE, by contrast, is more like a fixed-shape tensor engine especially well suited to “large, regular, FP16 matrix computations.”

## Results
- At light desktop idle, the author measured **M5 Max package power below 2W**; Apple reports total system idle power dropping from **7.6W on M4 Max to 7.1W**, and claims **1 additional hour** of battery life.
- Short-term peak CPU/GPU power can both reach **around 80W**; in Cinebench multithreaded testing, the CPU attempts to sustain **around 75W**, then settles to **around 50W** as temperature rises, but the author says performance still exceeds M4 Max, implying better sustained performance per watt.
- Geekbench 6.6.0 scores are approximately **4300 single-core** and **28000–30000 multi-core**, with peak power around **66W** during testing; the article does not provide a full same-condition comparison against M4 Max, but clearly claims the M5 Max is both faster and more power-efficient.
- In ANE-related testing, after retuning for larger FP16 matmul workloads, measured wall-clock peak performance reached about **19.9 TFLOPS**, higher than the project’s older **M4 reference value of 15.8 TFLOPS**, an increase of about **26%**.
- For AI inference, the author distinguishes between prefill and decode: claiming M5 Max benefits in prefill because of stronger GPU neural acceleration, while decode improves due to slightly increased memory bandwidth; however, a direct quantified comparison with **DGX Spark** has not yet been completed because **int4/macOS 26.4** support is still in beta.
- The strongest overall conclusion is a qualitative claim: M5 Max delivers better peak performance, sustained performance, performance per watt, and on-device AI capability in a laptop, while the chiplet design may also bring better manufacturing cost and sustainability, though the manufacturing economics portion is mainly theoretical inference rather than verification from public mass-production data.

## Link
- [https://creativestrategies.com/research/m5-max-chiplets-thermals-and-performance-per-watt/](https://creativestrategies.com/research/m5-max-chiplets-thermals-and-performance-per-watt/)
