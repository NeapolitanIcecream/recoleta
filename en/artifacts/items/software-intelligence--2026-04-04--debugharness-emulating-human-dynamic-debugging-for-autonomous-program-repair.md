---
source: arxiv
url: http://arxiv.org/abs/2604.03610v1
published_at: '2026-04-04T06:49:30'
authors:
- Maolin Sun
- Yibiao Yang
- Xuanlin Liu
- Yuming Zhou
- Baowen Xu
topics:
- automated-program-repair
- llm-agents
- dynamic-debugging
- software-security
- memory-safety
- c-cpp
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# DebugHarness: Emulating Human Dynamic Debugging for Autonomous Program Repair

## Summary
DebugHarness is an LLM-based program repair system for hard C/C++ security bugs that uses live debugging, not just static code reading. The paper claims that giving the agent access to runtime state, reverse debugging, and patch-validation feedback lifts repair success on real-world memory-safety vulnerabilities.

## Problem
- Existing LLM repair agents treat vulnerability fixing as a static code-generation task, using source code, crash reports, and stack traces without enough runtime context.
- That fails on low-level C/C++ bugs such as use-after-free, heap corruption, and stale-pointer issues, where the crash site and the root cause can be far apart in time and code location.
- This matters because fuzzers can find many security bugs, but patching them still takes expert manual debugging, which slows remediation and leaves systems exposed.

## Approach
- DebugHarness starts from a reproducible PoC crash and sanitizer report, extracts the bug signature, and classifies the error type to load debugging guidance tailored to that class of vulnerability.
- The agent then runs an interactive debugging loop: it inspects source through a language server, queries live execution state through GDB and pwndbg, and uses `rr` record/replay to move backward through execution and trace memory corruption to its origin.
- The system asks the LLM to form a concrete root-cause hypothesis, test it with debugger actions such as breakpoints and watchpoints, and refine the hypothesis from observed runtime evidence.
- To keep debugger output within context limits, it distills raw traces and can run LLM-generated Python scripts in a sandbox to summarize large structures or memory dumps.
- After it identifies a likely cause, it generates a patch, repairs malformed diffs with a deterministic alignment step, recompiles, reruns the PoC and tests, and feeds compiler or crash feedback back into the next iteration.

## Results
- Evaluation uses **SEC-bench**, a benchmark with **200 real-world security vulnerabilities** across **29** open-source **C/C++** projects.
- DebugHarness reports an overall bug resolution rate of about **90%** on this benchmark.
- The paper compares against **PatchAgent** at **57.5%** and **VulnResolver** at **67.5%** resolution rate.
- The claimed gain is **over 30% relative improvement** over state-of-the-art baselines.
- The paper says ablation studies show both core parts, **signature-driven investigation** and **interactive state introspection**, are necessary for the reported performance, but the excerpt does not provide ablation numbers.
- The motivating example is **CVE-2022-1286** in **mruby**, where dynamic watchpoints and reverse tracing let the agent find a missing `mrb_mc_clear_by_class` cache invalidation that static agents miss.

## Link
- [http://arxiv.org/abs/2604.03610v1](http://arxiv.org/abs/2604.03610v1)
