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
language_code: en
---

# Trampolining Nix with GenericClosure

## Summary
This article proposes a Nix “trampoline” technique using `builtins.genericClosure` plus `deepSeq` to rewrite long-running computations that would otherwise overflow the stack due to recursion into execution with constant stack depth. Its core value is providing a practical iterative strategy for input-size-driven computations such as interpreters, validators, and state machines when Nix lacks tail-call optimization and loop primitives.

## Problem
- Nix has no loops, so iteration depends on recursion; the reference implementation also lacks reliable tail-call optimization, with a default `max-call-depth` of 10,000, so long computation chains can easily overflow the stack.
- Naively rewriting recursion with `genericClosure` can avoid growth of the Nix evaluator call stack, but lazy evaluation causes deep chains of thunks to accumulate in untouched state fields, eventually triggering a C++ stack overflow when the result is read.
- This is especially important for interpreters, validators, state machines, and deep NixOS/home-manager configurations, because their computation length often grows linearly with input size, so they cannot rely on “small recursion depth” to get by.

## Approach
- Encode each computation step as a node in `genericClosure`: `operator` receives the current state and returns the next node; returning an empty list means stop, effectively using an internal C++ `while` loop to drive execution.
- The key trick is embedding `builtins.deepSeq result.state (s.key + 1)` in the `key` of the next node. Since `genericClosure` necessarily forces evaluation of `key`, this also fully evaluates the entire state at each step.
- This prevents untouched fields such as `total = total + 1` from forming an N-layer deferred thunk chain, eliminating the risk of “moving the stack overflow from the computation phase to the result-reading phase.”
- In essence, this method “abuses” the forced-evaluation side effect of deduplication keys: the key stays monotonically increasing to avoid dedup hits, while `deepSeq` makes the lazy state strict.
- The author also applies it to the evaluation loop of a freer monad interpreter in `nix-effects`, and combines it with FTCQueue to avoid the quadratic complexity caused by left-nested binds.

## Results
- Direct recursive counting with `count 10001` fails under default Nix settings with `stack overflow; max-call-depth exceeded`; the trampoline version, however, completes **1,000,000** iterations and takes about **1.0s** on the example machine.
- Baseline comparison: `foldl'` performing the same 1,000,000-count workload on known-length, single-value state takes only about **0.09s**, roughly **11x** faster than this trampoline approach; the author attributes the gap to the **O(log n)** per-step overhead of `genericClosure`’s `std::map` deduplication and the cost of forced evaluation via `deepSeq`.
- A naive trampoline (without `deepSeq`) can “finish” **65,000** or **100,000** steps, but crashes when accessing the final `.total` because it has accumulated a deep thunk chain; after adding `deepSeq`, the same composite state `{ i, total }` correctly returns `100000` after **100,000** steps.
- `foldl'` only forces composite attrset state to weak head normal form; the author shows that it also throws `stack overflow (possible infinite recursion)` for attrset accumulation over **100,000** steps, while the `deepSeq` trampoline handles the same workload.
- In the real application `nix-effects` tests, **100,000** chained operations pass; even a pathological case with left-nested bind depth **1,000** evaluates correctly. The article does not provide a more systematic large-scale benchmark table, but these figures support the core claim that “constant stack depth is usable.”
- On the novelty claim, the author explicitly says they searched Discourse, GitHub, nixpkgs, and blogs and found no prior public record of the technique of “putting `deepSeq` into `genericClosure.key` to force per-step state evaluation.”

## Link
- [https://blog.kleisli.io/post/trampolining-nix-with-generic-closure](https://blog.kleisli.io/post/trampolining-nix-with-generic-closure)
