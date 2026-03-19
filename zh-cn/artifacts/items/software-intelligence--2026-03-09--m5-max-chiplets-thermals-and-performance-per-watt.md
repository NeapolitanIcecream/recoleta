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
language_code: zh-CN
---

# M5 Max: Chiplets, Thermals, and Performance per Watt

## Summary
这篇文章认为 M5 Max 通过真正的 chiplet 化设计，在笔记本 SoC 上同时提升了性能、能效、热表现和潜在制造经济性。作者的核心判断是：它可能是当前最强的笔记本 SoC，并且在 AI 与性能功耗比上尤其突出。

## Problem
- 传统大面积单片 SoC 在先进制程下面临良率下降、废片增加、制造成本上升的问题。
- CPU、GPU 等模块共处单一硅片时，热耦合会限制同时高负载下的持续性能与效率。
- 笔记本芯片需要在高性能、低功耗、全天续航和本地 AI 推理之间取得平衡，这很难同时做到。

## Approach
- M5 Pro/Max 采用更“真正”的 chiplet 方案：把 **CPU-dominant tile** 与 **GPU-dominant tile** 分开，再通过更先进封装（SoIC-MH 混合键合）组成单一封装。
- Apple 似乎在 M5 Pro 和 M5 Max 之间复用相同的 CPU tile（18 核 CPU、Neural Engine、媒体模块），主要通过不同 GPU tile 做产品区分，以提升良率、降低研发/验证成本，并改善 GPU 分档灵活性。
- 这种分拆不仅是制造策略，也改善热设计：CPU 与 GPU 分居不同主导 tile，减少彼此热串扰，从而允许二者在同时高负载时跑得更高、更久。
- 在 CPU 架构上，M5 Pro/Max 看起来取消了 efficiency cores，改为 **6 super cores + 12 performance cores**；文章推测 Apple 倾向让大核在低功耗区间运行，以替代传统 e-core 的部分角色。
- 对 AI，作者认为 M5 Max 的提升主要来自 GPU 神经加速路径与略高内存带宽；ANE 则更像一个对“大块、规则、FP16 矩阵计算”特别友好的固定形状张量引擎。

## Results
- 轻桌面空闲时，作者测到 **M5 Max 封装功耗低于 2W**；Apple 报告的整机空闲功耗从 **M4 Max 的 7.6W 降到 7.1W**，并宣称电池续航 **增加 1 小时**。
- CPU/GPU 短时峰值功耗都可到 **约 80W**；CPU 在 Cinebench 多线程中尝试维持 **约 75W**，随后随温度上升稳定到 **约 50W** 左右，但作者称性能仍优于 M4 Max，意味着持续性能功耗比更好。
- Geekbench 6.6.0 成绩约为 **4300 单核**、**28000–30000 多核**，测试中峰值功耗约 **66W**；文中未给出同条件下 M4 Max 的完整对比数字，但明确声称 M5 Max 更快且更省电。
- 在 ANE 相关测试中，经过针对更大 FP16 matmul 的重调优后，测得墙钟峰值约 **19.9 TFLOPS**，相比项目中旧的 **M4 参考值 15.8 TFLOPS** 更高，约提升 **26%**。
- AI 推理方面，作者区分 prefill 与 decode：声称 M5 Max 在 prefill 上因 GPU 神经加速更强而受益，decode 则因内存带宽略增而改善；但与 **DGX Spark** 的直接量化对比尚未完成，因为 **int4/macOS 26.4** 支持仍在 beta。
- 最强的总体结论是定性主张：M5 Max 在笔记本中实现了更好的峰值性能、持续性能、性能每瓦和本地 AI 能力，同时 chiplet 设计还可能带来更优的制造成本与可持续性，但其中制造经济性部分主要是理论推断而非公开量产数据验证。

## Link
- [https://creativestrategies.com/research/m5-max-chiplets-thermals-and-performance-per-watt/](https://creativestrategies.com/research/m5-max-chiplets-thermals-and-performance-per-watt/)
