---
source: hn
url: https://github.com/coreutils/coreutils/commit/2b1c059e6
published_at: '2026-03-10T23:44:38'
authors:
- pixelbeat__
topics:
- systems-performance
- linux-io
- zero-copy
- coreutils
- cli-tools
relevance_score: 0.42
run_id: materialize-outputs
---

# Updating yes(1) to run at 175GiB/s

## Summary
这是一项对 GNU coreutils 中 `yes(1)` 的底层 I/O 路径优化，通过在 Linux 上使用零拷贝 `vmsplice/splice` 大幅提升连续输出吞吐。它解决了一个看似简单但极端高频的系统工具在现代内核上被用户态内存拷贝限制的问题。

## Problem
- `yes` 会无限重复输出相同字符串，传统实现主要依赖 `write()` 和用户态缓冲区复制，吞吐会受内存拷贝与系统调用开销限制。
- 对这类“内容恒定、持续流式输出”的程序，额外复制几乎没有价值；若不能绕过复制路径，就浪费 CPU/内存带宽。
- 这很重要，因为 `yes` 常被用于管道、基准测试、压力测试和 shell 组合中，极高吞吐下其实现细节会直接影响系统级性能。

## Approach
- 新实现先做一次最小 `full_write()`，低成本确认标准输出可用；成功后再切换到更高效的重复输出路径。
- 在 Linux 且支持 `splice` 时，使用 `vmsplice` 把页对齐缓冲区“赠送”给内核，再用 `splice` 直接转发到输出，实现零拷贝/少拷贝传输。
- 针对输出已经是 pipe 与输出不是 pipe 两种场景分别处理：若 stdout 是 pipe，则直接 `vmsplice` 到 stdout；否则先建中间 pipe，再 `splice` 到 stdout。
- 通过经验参数调优 pipe 大小，选择 pipe 容量的 1/4 作为传输甜点；同时用 `repeat_pattern` 高效填充重复模式缓冲区。
- 加入健壮回退机制：若 `vmsplice`、`pipe2` 等不可用或报错，则退回普通 `write()` 路径，并新增测试覆盖这些异常分支。

## Results
- 提交在 NEWS 中明确声称：`yes` 在 Linux 上启用零拷贝 I/O 后，某些系统上的吞吐从 **12 GiB/s 提升到 175 GiB/s**。
- 按该数字计算，吞吐提升约 **14.6×**（175 / 12 ≈ 14.58）。
- 结果描述为“**significantly increase throughput**”，适用条件是 Linux 支持相关零拷贝机制（`splice/vmsplice`）。
- 文本未提供更细的基准设置，如 CPU 型号、内核版本、消息大小、具体数据集或误差范围。
- 除性能外，还给出功能性主张：对非 pipe 输出做了专门路径支持，并在 `vmsplice` 或 `pipe2` 失败时验证会回退到 `write()`，保证兼容性与正确性。

## Link
- [https://github.com/coreutils/coreutils/commit/2b1c059e6](https://github.com/coreutils/coreutils/commit/2b1c059e6)
