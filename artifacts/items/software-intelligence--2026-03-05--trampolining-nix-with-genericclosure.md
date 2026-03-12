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
- interpreter-design
relevance_score: 0.57
run_id: materialize-outputs
---

# Trampolining Nix with GenericClosure

## Summary
本文提出一种利用 `builtins.genericClosure` 加 `deepSeq` 的 Nix“蹦床”技巧，把原本会因递归而栈溢出的长计算改写为常数栈深度执行。核心价值是在 Nix 缺少尾调用优化和循环原语时，为解释器、验证器、状态机等输入规模驱动的计算提供可行迭代方案。

## Problem
- Nix 没有循环，迭代依赖递归；参考实现也缺少可靠的尾调用优化，默认 `max-call-depth` 为 10,000，长链计算很容易栈溢出。
- 朴素地把递归改成 `genericClosure` 虽可避免 Nix 求值器调用栈增长，但惰性求值会在未被触碰的状态字段里累积深 thunk 链，最终在读取结果时触发 C++ 栈溢出。
- 这对解释器、验证器、状态机、深层 NixOS/home-manager 配置等尤为重要，因为其计算长度常随输入规模线性增长，无法依赖“小递归深度”侥幸通过。

## Approach
- 把每一步计算编码成 `genericClosure` 的一个节点：`operator` 接收当前状态，返回下一个节点；返回空列表表示停止，相当于用 C++ 内部 `while` 循环驱动执行。
- 关键技巧是在下一步节点的 `key` 中嵌入 `builtins.deepSeq result.state (s.key + 1)`，借助 `genericClosure` 必然强制求值 `key` 的机制，连带把整份状态在每步都完全求值。
- 这样可防止像 `total = total + 1` 这类未即时访问字段形成 N 层 deferred thunk 链，把“栈溢出从计算阶段转移到结果读取阶段”的隐患一并消除。
- 该方法本质上是“滥用”去重键的强制求值副作用：键保持单调递增以避免去重命中，而 `deepSeq` 则负责把惰性状态变严格。
- 作者还将其用于 `nix-effects` 中 freer monad 解释器的求值循环，并结合 FTCQueue 避免左嵌套 bind 带来的二次复杂度问题。

## Results
- 直接递归计数 `count 10001` 在默认 Nix 设置下失败，报错 `stack overflow; max-call-depth exceeded`；而蹦床版本可完成 **1,000,000** 次迭代，并在示例机器上耗时约 **1.0s**。
- 对比基线：`foldl'` 处理已知长度、单值状态的同类 1,000,000 次计数仅约 **0.09s**，约比该蹦床方案快 **11x**；作者将差距归因于 `genericClosure` 的 `std::map` 去重带来的 **O(log n)** 每步开销，以及 `deepSeq` 的强制求值成本。
- 朴素 trampoline（无 `deepSeq`）可“跑完” **65,000** 或 **100,000** 步，但在访问最终 `.total` 时崩溃，因为累积了深 thunk 链；加入 `deepSeq` 后，同样的复合状态 `{ i, total }` 在 **100,000** 步下可正确返回 `100000`。
- `foldl'` 对复合 attrset 状态只强制到弱头范式，作者展示其在 **100,000** 步 attrset 累加时也会报 `stack overflow (possible infinite recursion)`；而 `deepSeq` 版 trampoline 能处理相同工作负载。
- 在实际应用 `nix-effects` 测试中，**100,000** 个链式操作通过；左嵌套 bind 深度 **1,000** 的病理案例也能正确求值。全文未给出更系统的大规模基准表，但这些数字支撑了“常数栈深度可用”的核心主张。
- 新颖性主张上，作者明确表示检索了 Discourse、GitHub、nixpkgs 与博客后，未发现此前公开记录过“把 `deepSeq` 塞进 `genericClosure.key` 以强制每步状态求值”的技巧。

## Link
- [https://blog.kleisli.io/post/trampolining-nix-with-generic-closure](https://blog.kleisli.io/post/trampolining-nix-with-generic-closure)
