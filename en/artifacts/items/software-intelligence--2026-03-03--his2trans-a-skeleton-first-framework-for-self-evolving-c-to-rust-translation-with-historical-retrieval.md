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
- build-aware
- self-evolving
- code-migration
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# His2Trans: A Skeleton First Framework for Self Evolving C to Rust Translation with Historical Retrieval

## Summary
His2Trans is a framework for industrial-scale C-to-Rust migration. Its core idea is to first build a compilable, strongly typed project skeleton, then gradually generate function logic by combining it with retrieval of historical migration knowledge. It aims to solve problems in large-project migration such as missing build context, missing domain API mappings, and uncontrolled repair loops.

## Problem
- Existing automated C→Rust migration methods often fail on industrial projects because of **missing build context**, making it impossible to recover precise types and dependencies, which leads to “dependency hell” and hallucinated dependencies.
- General-purpose LLMs alone struggle to infer **domain-specific APIs and historical evolution patterns**, so they cannot reuse existing Rust interfaces and are prone to generating non-idiomatic or even non-integrable code.
- Large projects usually require **incremental migration**. If each repair triggers cascading compilation errors, the cost of automation quickly becomes unmanageable; this matters because the paper cites memory-safety issues in C as one source of about **70% of security vulnerabilities**, and migration to Rust is therefore an important industrial direction.

## Approach
- It first performs **build tracing** to recover macros, types, conditional compilation, and dependencies from the real build process, generating a compilable **Project-Level Skeleton Graph**; simply put, it first sets up the entire Rust project’s “empty frame” and ensures the types are correct.
- The skeleton preserves directory structure, module relationships, type definitions, global state, and function signatures, while function bodies are initially filled with `unimplemented!` placeholders, separating **structural verification** from **logic generation**.
- It then automatically mines **API-level rules** and **fragment-level rules** from historical C/Rust migration repositories to form an accumulable knowledge base; during retrieval it uses BM25 + reranker + RAG to feed similar historical examples to the LLM.
- Function-body translation is scheduled **bottom-up topologically** according to the dependency graph: functions with fewer dependencies are translated first, then higher-level functions; at each step, compiler feedback is used for rule repair or LLM repair, and when necessary it falls back to C2Rust unsafe code to preserve compilability.
- Translation results that pass verification are written back into the knowledge base, forming a **self-evolving** closed loop that makes subsequent unseen tasks easier to repair.

## Results
- On industrial **OpenHarmony** modules, His2Trans reports a **99.75% incremental compilation pass rate** and claims it can fix failures in baseline methods caused by missing build context.
- On general benchmarks, compared with **C2Rust**, its **unsafe code ratio is reduced by 23.6 percentage points** while also producing the **fewest warnings**.
- In knowledge accumulation experiments, as verified migration patterns continue to be added, **repair overhead** on unseen tasks **drops by about 60%**, indicating that the system has an evolutionary capability of “getting stronger with use.”
- The evaluation covers **5 OpenHarmony submodules** and **10 general-purpose C projects**; the paper also lists multiple baselines (such as C2Rust, PTRMAPPER, EvoC2Rust, Tymcrat, etc.), but the excerpt does not provide the full itemized comparison table or all numerical details.
- The experimental setup emphasizes **zero-human-intervention**, meaning there was no manual post-editing or cherry-picking during evaluation.

## Link
- [http://arxiv.org/abs/2603.02617v1](http://arxiv.org/abs/2603.02617v1)
