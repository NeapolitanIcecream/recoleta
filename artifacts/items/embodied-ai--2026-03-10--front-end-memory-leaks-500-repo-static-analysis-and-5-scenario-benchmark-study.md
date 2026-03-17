---
source: hn
url: https://stackinsight.dev/blog/memory-leak-empirical-study/
published_at: '2026-03-10T22:56:26'
authors:
- nadis
topics:
- frontend-memory-leaks
- static-analysis
- benchmarking
- react-vue-angular
- javascript-gc
relevance_score: 0.01
run_id: materialize-outputs
---

# Front End Memory Leaks: 500-Repo Static Analysis and 5-Scenario Benchmark Study

## Summary
这篇研究用跨 React、Vue、Angular 的 AST 静态分析扫描了 500 个高影响力前端仓库，并用 5 个受控基准量化“缺少清理”导致的前端内存泄漏成本。核心结论是：这类问题在生产代码中非常普遍，而且其内存增长近似线性、可稳定复现。

## Problem
- 论文要解决的问题是：前端单页应用中的“慢性”内存泄漏到底有多常见、以及每次组件挂载/卸载遗漏清理究竟会造成多大 retained heap 增长。
- 这很重要，因为这类泄漏通常不会立刻报错，而是在长会话、频繁导航、移动端或 Electron 场景下逐步引发卡顿、掉帧、冻结甚至标签页被系统杀死。
- 现有 lint/工具对这类问题覆盖不完整，例如 `useEffect` 缺少 cleanup、`.subscribe()` 未退订、`watch()` 未保存 stop handle 等常会漏检。

## Approach
- 作者为 React、Vue、Angular 分别构建了基于 Babel 的 AST 检测器，匹配“资源建立”与“资源释放”是否成对出现，例如 `addEventListener/removeEventListener`、`subscribe/unsubscribe`、`watch/stop`、`requestAnimationFrame/cancelAnimationFrame`。
- 在 500 个公开且成熟的仓库上运行检测，覆盖 714,217 个文件，并按泄漏类型、上下文和严重度分类统计。
- 为了量化真实成本，作者设计了 5 个受控基准场景：React 事件监听、Vue 定时器、Angular 订阅、Vue watcher、RAF；每个场景进行 100 次 mount/unmount、50 次独立重复，并在每次测量前强制 GC。
- 简单说，方法就是：先在大规模真实代码里找“忘记清理”的模式，再在小型可控实验中测它们每漏一次会多占多少内存。

## Results
- 静态分析发现：500 个仓库中有 430 个至少存在 1 个缺少清理模式，普遍率 **86.0%**；总计发现 **55,864** 个潜在泄漏实例，覆盖 **714,217** 个文件。
- 主要模式中，`setTimeout/setInterval` 相关问题最多；仅 `setTimeout` 就占全部发现的 **40%**，事件监听未移除共有 **10,616** 处；Vue `watch` 未保存 stop handle 有 **3,360** 处，`watchEffect` 有 **629** 处；缺少 `cancelAnimationFrame` 有 **1,230** 处。
- 5 个基准场景结果高度一致：缺少清理的 BAD 版本在 **100 cycles** 后 retained heap 约 **804–819 KB**，即约 **~8 KB/cycle**；正确清理的 GOOD 版本仅 **2.4–2.6 KB total**，接近噪声底。
- React `useEffect` 场景：BAD 平均 **807 KB**，GOOD **2.4 KB**，标准差约 **±37 KB**；作者称其 95% CI 与 SEM 表明结果稳定，SEM 为 **5.2 KB**。
- 统计显著性方面，所有场景均报告 **p < 0.001**；效应量极大，例如 React 场景 **Cohen’s d = 21.8**，Angular 订阅场景 **d = 820.3**，说明 BAD 与 GOOD 分布几乎完全分离。
- 作者声称其覆盖的 5 个基准模式对应 **53,313 / 55,864 = 95.4%** 的扫描发现，并总结为：缺少 cleanup 不是边缘问题，而是可预测、线性累积、且通常只需“一行修复”的工程问题。

## Link
- [https://stackinsight.dev/blog/memory-leak-empirical-study/](https://stackinsight.dev/blog/memory-leak-empirical-study/)
