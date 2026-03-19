---
source: arxiv
url: http://arxiv.org/abs/2603.07065v1
published_at: '2026-03-07T06:46:16'
authors:
- Alperen Keles
topics:
- mutation-testing
- fuzzing-evaluation
- property-based-testing
- program-analysis
- developer-tools
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# A Declarative Framework for Hand-Crafted Mutation Analysis and Management

## Summary
This paper proposes a declarative framework for **hand-crafted mutants** that uniformly describes, transforms, and manages multiple mutation representations, and implements a prototype tool, Marauder. Its core value is reducing the fragmented trade-offs in existing hand-crafted mutation tools among readability, preservation, and execution efficiency.

## Problem
- Existing hand-crafted mutation analysis tools are fragmented and are often forced to trade off among **readability, whether mutation structure is preserved, and execution/compilation cost**.
- Hand-crafted mutations are becoming increasingly important in evaluations of fuzzing and property-based testing because they are closer to real defects, controllable, and reproducible.
- Traditional comment-based approaches often require **recompiling each mutation**, and some implementations are not mutation-preserving: after activation, mutation boundaries are lost, which affects subsequent analysis and management.

## Approach
- The paper categorizes hand-crafted mutation systems into five representations: **comment-based, preprocessor-based, patch-based, match-and-replace, in-ast**, and analyzes the strengths and weaknesses of each.
- It proposes a **mutation algebra**: using `+` to denote sequential testing and `*` to denote combined activation, supporting tag-based expansion and higher-order combinations, making it convenient to select subsets or test multiple mutations simultaneously.
- It designs a **common intermediate representation** and a **lossless conversion pipeline**, enabling cross-representation conversion through the approach of “first extracting into a unified structure, then rendering into the target representation.”
- For in-AST mutations, it proposes an extraction and normalization strategy: finding the **smallest syntactic unit** that can contain all candidate variants, thereby safely converting mutations that originally crossed syntactic boundaries into embedded AST form.
- It implements the prototype system **Marauder**, supporting injection, activation, reset, composition, testing, and cross-representation conversion, and provides CLI and VS Code/ETNA plugin interfaces.

## Results
- The paper’s main contribution is **proposing a unified framework, mutation algebra, and a lossless conversion approach**, and delivering the working prototype Marauder; it is not focused on pursuing new testing accuracy metrics.
- On ETNA Rust workloads, it compares **comment-based vs. in-AST**: **31** mutations in total, with total time of **146.07s** for comment-based and **102.72s** for in-AST, for an overall speedup of about **1.42×**.
- **BST**: `n=8`, total time **37.51s** for comment-based and **20.40s** for in-AST; compilation speedup **1.84×**, execution slowdown **1.30×**.
- **RBT**: `n=13`, total time **41.39s** for comment-based and **22.74s** for in-AST; compilation speedup **1.82×**, execution slowdown **1.12×**.
- **STLC**: `n=10`, total time **67.17s** for comment-based and **59.57s** for in-AST; compilation speedup **1.13×**, execution slowdown **1.07×**.
- In conclusion, the authors claim that the in-AST approach can significantly reduce repeated compilation overhead while incurring only modest runtime overhead (**1.07×–1.30×** slowdown), thereby enabling more efficient hand-crafted mutation experiments.

## Link
- [http://arxiv.org/abs/2603.07065v1](http://arxiv.org/abs/2603.07065v1)
