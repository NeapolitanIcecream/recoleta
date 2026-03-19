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
language_code: en
---

# Trampolining Nix with GenericClosure

## Summary
This article proposes a technique for achieving **O(1) call-stack depth** in Nix: repurposing `builtins.genericClosure` as a trampoline, and using `deepSeq` to force evaluation of the state at each step. It solves the problem of stack overflows caused by Nix's lack of tail-call optimization, deep recursion, and lazy thunk chains.

## Problem
- Nix has no loops, so iteration usually relies on recursion; the reference implementation lacks reliable tail-call optimization, and the default `max-call-depth` is about **10,000**, so longer computations can overflow the stack directly.
- Simply rewriting recursion into `genericClosure` is not enough: if some fields in the state are not accessed at each step, lazy evaluation accumulates them into a deep thunk chain, eventually triggering a **C++ stack overflow** when the result is read.
- This matters for interpreters, validators, state machines, and Nix computations whose length grows with input size, because they quickly hit the recursion-depth limit or hidden deferred-explosion problems.

## Approach
- The core idea is to treat `builtins.genericClosure` as a worklist/trampoline driven by a C++ `while` loop: each "node" represents one computation step, the `operator` produces the next step, and execution stops when it returns `[]`.
- In this way, each step is continued by the builtin loop rather than by a Nix function recursively calling itself, so the **Nix call stack does not grow with the number of steps**.
- The key fix is embedding `key = builtins.deepSeq result.state (s.key + 1)` into the node key. Because `genericClosure` must force `key`, this also forces the entire state to be fully evaluated at each step.
- This trick prevents fields like `total = total + 1`, which intermediate steps do not touch, from forming an N-layer thunk chain, thereby also eliminating the hidden problem of "crashing when reading the result after computation."
- The author also applies this pattern in the `nix-effects` freer monad interpreter, combining effect handling, resume/abort behavior, and a continuation queue to achieve constant-stack-depth interpretation.

## Results
- Naive recursive counting `count 10001` fails immediately with `stack overflow; max-call-depth exceeded`, showing that default Nix recursion hits the depth limit at around **10,001** calls.
- Using the trampoline with `deepSeq`, the same kind of counting can run to **1,000,000** steps and return successfully; the command-line output in the article shows `1000000`, taking about **1.0s**.
- Compared with the baseline `foldl'`: when the iteration count is known and the state is a single value, `foldl'` completes **1,000,000** iterations in only about **0.09s**, roughly **11x** faster than the trampoline; the author attributes the difference to `genericClosure`'s `std::map` deduplication overhead and the cost of forcing evaluation with `deepSeq`.
- Although naive trampolining can complete **65,000** steps within `genericClosure` itself, reading the result crashes because of the thunk chain; after adding `deepSeq`, composite states like `{ i = 0; total = 0; }` can reliably run to **100,000** steps and return `100000`.
- `foldl'` is not safe for composite attrset state: in the article's example it reports `stack overflow (possible infinite recursion)` at **100,000** steps, because it only forces the accumulator to WHNF, while thunks inside fields still accumulate; on the author's machine, the C++ stack is exhausted at around **65,000** frames.
- In the real application `nix-effects`, the test suite passed **100,000** chained operations; for a pathological naive free monad case, even **left-nested bind depth 1,000** can be handled correctly while maintaining constant stack depth.

## Link
- [https://blog.kleisli.io/post/trampolining-nix-with-generic-closure](https://blog.kleisli.io/post/trampolining-nix-with-generic-closure)
