---
source: hn
url: https://blog.kleisli.io/post/trampolining-nix-with-generic-closure
published_at: '2026-03-05T23:26:26'
authors:
- ret2pop
topics:
- nix
- trampolining
- lazy-evaluation
- tail-call-optimization
- generic-closure
relevance_score: 0.01
run_id: materialize-outputs
---

# Trampolining Nix with GenericClosure

## Summary
这篇文章提出了一种在 Nix 中实现 **O(1) 调用栈深度** 的技巧：把 `builtins.genericClosure` 重新用作 trampoline，并用 `deepSeq` 强制每一步状态求值。它解决了 Nix 缺少尾调用优化、深递归和惰性 thunk 链导致栈溢出的问题。

## Problem
- Nix 没有循环，迭代通常靠递归；参考实现缺少可靠的尾调用优化，默认 `max-call-depth` 约为 **10,000**，较长计算会直接栈溢出。
- 仅把递归改写成 `genericClosure` 还不够：若状态中的某些字段在每步未被访问，惰性求值会累积成很深的 thunk 链，最后在读取结果时触发 **C++ 栈溢出**。
- 这对解释器、验证器、状态机、以及长度随输入增长的 Nix 计算很重要，因为它们会很快碰到递归深度上限或隐藏的延迟爆炸问题。

## Approach
- 核心方法是把 `builtins.genericClosure` 当作一个由 C++ `while` 循环驱动的 worklist/trampoline：每个“节点”代表一次计算步骤，`operator` 产出下一个步骤，返回 `[]` 时停止。
- 这样每一步都由内建循环继续执行，而不是由 Nix 函数递归调用自身，因此 **Nix 调用栈不随步数增长**。
- 关键修复是把 `key = builtins.deepSeq result.state (s.key + 1)` 嵌入节点键中，借助 `genericClosure` 必然强制 `key` 的行为，顺带把整份状态也在每一步完全求值。
- 这个技巧阻止了像 `total = total + 1` 这类未被中间步骤触碰的字段形成 N 层 thunk 链，从而把“计算后读取结果时崩溃”的隐藏问题一起消除。
- 作者还将该模式用于 `nix-effects` 中的 freer monad 解释器，将 effect 处理、恢复/中止和 continuation queue 结合起来，实现常数栈深度的解释执行。

## Results
- 朴素递归计数 `count 10001` 直接失败：`stack overflow; max-call-depth exceeded`，说明默认 Nix 递归在 **10,001** 次左右就会碰到深度限制。
- 使用带 `deepSeq` 的 trampoline，同类计数可跑到 **1,000,000** 次并成功返回；文中命令行实测输出 `1000000`，耗时约 **1.0s**。
- 对比基线 `foldl'`：在已知迭代次数、单值状态下，`foldl'` 完成 **1,000,000** 次仅约 **0.09s**，约比 trampoline **快 11x**；作者将差异归因于 `genericClosure` 的 `std::map` 去重开销和 `deepSeq` 的强制求值成本。
- 朴素 trampoline 在 **65,000** 步时虽然 `genericClosure` 本身能完成，但读取结果会因 thunk 链触发崩溃；加入 `deepSeq` 后，`{ i = 0; total = 0; }` 这类复合状态可稳定跑到 **100,000** 步并返回 `100000`。
- `foldl'` 对复合 attrset 状态并不安全：文中示例在 **100,000** 步时报 `stack overflow (possible infinite recursion)`，因为它只把累加器强制到 WHNF，字段内部 thunk 仍然累积；作者机器上的 C++ 栈大约在 **65,000** 层附近耗尽。
- 在真实应用 `nix-effects` 中，测试套件通过了 **100,000** 个链式操作；对 naive free monad 病例，**左嵌套 bind 深度 1,000** 也能正确处理，同时保持常数栈深度。

## Link
- [https://blog.kleisli.io/post/trampolining-nix-with-generic-closure](https://blog.kleisli.io/post/trampolining-nix-with-generic-closure)
