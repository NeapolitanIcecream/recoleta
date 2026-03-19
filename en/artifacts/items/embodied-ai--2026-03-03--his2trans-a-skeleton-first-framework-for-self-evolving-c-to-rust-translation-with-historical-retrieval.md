---
source: arxiv
url: http://arxiv.org/abs/2603.02617v1
published_at: '2026-03-03T05:42:08'
authors:
- Shengbo Wang
- Mingwei Liu
- Guangsheng Ou
- Yuwen Chen
- Zike Li
- Yanlin Wang
- Zibin Zheng
topics:
- c-to-rust
- code-translation
- retrieval-augmented-generation
- build-aware-compilation
- self-evolving-system
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# His2Trans: A Skeleton First Framework for Self Evolving C to Rust Translation with Historical Retrieval

## Summary
His2Trans is a framework for industrial-scale C→Rust migration that aims to address the lack of build context and historical migration knowledge in large-project translation. It combines a “compileable skeleton first” strategy with “retrieving rules from historical migrations” to improve compilation stability, reuse of idiomatic Rust practices, and continuous evolution.

## Problem
- Existing C→Rust automated migration in large engineering projects often falls into **dependency hell** due to the **lack of real build context**. LLMs are prone to hallucinating types, dependencies, and interfaces, leading to code that cannot compile.
- General-purpose LLMs alone struggle to infer **project-private APIs and domain-specific migration conventions**, making it difficult to reliably reuse Rust interfaces that have already been migrated historically during incremental migration.
- Incorrect dependencies can trigger **cascading repair loops**, causing the cost of project-level automated migration to spiral out of control. This matters because memory-safety issues in C account for a large share of security vulnerabilities, and migration to Rust is becoming an industry trend.

## Approach
- First, it uses **build tracing** to recover the real compilation environment and constructs a project-level, strictly type-consistent, compilable **Project-Level Skeleton Graph**, fixing type definitions, global variables, function signatures, and cross-module references in advance.
- It then decouples function-body generation from structural verification: starting with a skeleton containing `unimplemented!`, it gradually fills in function bodies according to dependency order via **topological scheduling**, reducing cascading errors.
- It performs **coarse-to-fine pairing and alignment** from historically co-evolved C/Rust repositories: candidate retrieval at the file level, function-level reordering, and then mining two kinds of rules: **API-level rules** and **fragment-level rules**.
- When generating each function, it uses **RAG** to retrieve relevant historical rules, feeding both the “strict compilation context provided by the skeleton” and the “historical migration rules” into the LLM to guide it toward reusing Rust interfaces and code fragments that better match project conventions.
- If the generated result fails to compile, it applies a **compiler-feedback closed-loop repair** process: rule-based repair first, then LLM-based repair. Successfully verified translation samples are fed back into the knowledge base to enable self-evolution.

## Results
- On industrial OpenHarmony modules, His2Trans claims a **99.75% incremental compilation pass rate**, and notes that baseline methods often fail because of missing build context.
- On general-purpose benchmarks, compared with **C2Rust**, it **reduces the unsafe code ratio by 23.6 percentage points** while producing **the fewest warnings**.
- Knowledge accumulation experiments show that by continuously integrating verified migration patterns, it can **reduce repair overhead by about 60%** on **unseen tasks**, supporting its “self-evolving” claim.
- The evaluation covers **5 OpenHarmony industrial submodules** and **10 general-purpose C projects**; the paper provides dataset scale, but the current excerpt does not include a complete metric-by-metric table of all baseline results.
- The experiments use a **zero human intervention** setting: all translation, repair, and result statistics are completed automatically by the framework, with no manual post-editing or cherry-picking of results.

## Link
- [http://arxiv.org/abs/2603.02617v1](http://arxiv.org/abs/2603.02617v1)
