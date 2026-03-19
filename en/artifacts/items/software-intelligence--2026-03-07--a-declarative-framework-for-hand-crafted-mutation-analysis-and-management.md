---
source: arxiv
url: http://arxiv.org/abs/2603.07065v1
published_at: '2026-03-07T06:46:16'
authors:
- Alperen Keles
topics:
- mutation-testing
- software-testing
- program-analysis
- declarative-framework
- benchmarking
relevance_score: 0.38
run_id: materialize-outputs
language_code: en
---

# A Declarative Framework for Hand-Crafted Mutation Analysis and Management

## Summary
This paper proposes a declarative framework for **hand-crafted mutants** that unifies the description, management, and conversion of multiple mutation representations, and implements a prototype tool, Marauder. Its core value is to establish a clear design space among readability, preservation of mutation structure, and execution efficiency, making it especially suitable for evaluating real defects in fuzzing and property-based testing.

## Problem
- Existing hand-crafted mutation toolchains are **fragmented**: different projects use different representations such as comments, patches, and preprocessors, making unified management and reuse difficult.
- Common approaches involve **key trade-offs**: source-level representations are more readable, but often require recompiling each mutant separately; some representations also lose the original mutation structure after activation, making further analysis impossible.
- This matters because fuzzing and property-based testing increasingly rely on **manually injected real/expert-crafted defects** for benchmark evaluation, and inefficient or unmaintainable mutation management directly limits experimental scale and credibility.

## Approach
- The paper categorizes hand-crafted mutation systems into 5 representation types: comment-based, preprocessor-based, patch-based, match-and-replace, and in-ast, and analyzes their trade-offs in readability, language awareness, preservation, and compilation cost.
- It defines a **mutation algebra**: `+` denotes sequential testing, `*` denotes combined activation, and `+tag` / `*tag` support tag-based expansion, enabling declarative subset selection, batch experimentation, and higher-order mutant composition.
- It designs a **lossless conversion pipeline**: various representations are first mapped into a unified intermediate form, and then rendered back into other representations to enable cross-representation conversion.
- For the hardest case, in-AST mutations, the paper proposes extraction and normalization strategies: finding the **smallest syntactic unit** that can contain all candidate variants, thereby rewriting mutations that originally crossed syntactic boundaries into a form that can be embedded in the AST.
- It implements the prototype system **Marauder**, supporting injection, activation, deactivation, reset, compositional testing, format conversion, and importing automatically generated mutants from cargo-mutants.

## Results
- The paper presents a complete prototype implementation of **Marauder**: the language-agnostic system can be used for any language; comment-based currently supports Haskell, Rocq, Racket, OCaml, Rust, and Python; in-AST currently supports Rust.
- On Rust workloads from the ETNA benchmark, the authors compare comment-based and in-AST: a total of **31** mutants across three tasks, **BST / RBT / STLC**.
- **BST (n=8)**: Comment Total **37.51s** vs In-AST Total **20.40s**, compilation speedup **1.84×**, execution slowdown **1.30×**.
- **RBT (n=13)**: Comment Total **41.39s** vs In-AST Total **22.74s**, compilation speedup **1.82×**, execution slowdown **1.12×**.
- **STLC (n=10)**: Comment Total **67.17s** vs In-AST Total **59.57s**, compilation speedup **1.13×**, execution slowdown **1.07×**.
- **Overall (31 mutants)**: Comment Total **146.07s**, In-AST Total **102.72s**; overall compilation speedup **1.42×**, with only **1.08×** execution slowdown. Based on this, the paper claims that in-AST can significantly reduce per-mutant recompilation cost while incurring only a small runtime overhead.

## Link
- [http://arxiv.org/abs/2603.07065v1](http://arxiv.org/abs/2603.07065v1)
