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
language_code: en
---

# Updating yes(1) to run at 175GiB/s

## Summary
This is a low-level I/O path optimization for `yes(1)` in GNU coreutils, substantially improving continuous output throughput on Linux by using zero-copy `vmsplice/splice`. It addresses the problem that a seemingly simple but extremely high-frequency system utility is limited by user-space memory copying on modern kernels.

## Problem
- `yes` outputs the same string repeatedly without end. The traditional implementation mainly relies on `write()` and user-space buffer copying, so throughput is limited by memory-copy and system-call overhead.
- For programs like this, where the content is constant and continuously streamed, the extra copying is almost pointless; if the copy path cannot be bypassed, CPU and memory bandwidth are wasted.
- This matters because `yes` is often used in pipelines, benchmarks, stress tests, and shell compositions, and at extremely high throughput its implementation details directly affect system-level performance.

## Approach
- The new implementation first performs a minimal `full_write()` to confirm at low cost that standard output is usable; after success, it switches to a more efficient repeated-output path.
- On Linux with `splice` support, it uses `vmsplice` to “gift” a page-aligned buffer to the kernel, then uses `splice` to forward it directly to the output, achieving zero-copy or reduced-copy transfer.
- It handles two cases separately: when the output is already a pipe and when it is not. If stdout is a pipe, it `vmsplice`s directly to stdout; otherwise, it first creates an intermediate pipe and then `splice`s to stdout.
- It tunes pipe size using empirical parameters, choosing one quarter of the pipe capacity as the transmission sweet spot; at the same time, it uses `repeat_pattern` to efficiently fill the repeated-pattern buffer.
- It adds a robust fallback mechanism: if `vmsplice`, `pipe2`, or related functionality is unavailable or returns an error, it falls back to the normal `write()` path, and new tests cover these exceptional branches.

## Results
- The commit explicitly states in NEWS that after enabling zero-copy I/O for `yes` on Linux, throughput on some systems increased from **12 GiB/s to 175 GiB/s**.
- Based on those numbers, the throughput improvement is about **14.6×** (175 / 12 ≈ 14.58).
- The result is described as “**significantly increase throughput**,” with the applicable condition being that Linux supports the relevant zero-copy mechanisms (`splice/vmsplice`).
- The text does not provide more detailed benchmark settings such as CPU model, kernel version, message size, specific dataset, or error range.
- In addition to performance, it also makes a functional claim: there is a dedicated path for non-pipe output, and it verifies that failures in `vmsplice` or `pipe2` fall back to `write()`, ensuring compatibility and correctness.

## Link
- [https://github.com/coreutils/coreutils/commit/2b1c059e6](https://github.com/coreutils/coreutils/commit/2b1c059e6)
