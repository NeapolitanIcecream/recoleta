---
source: arxiv
url: http://arxiv.org/abs/2603.01896v2
published_at: '2026-03-02T09:17:06'
authors:
- Shubham Ugare
- Satish Chandra
topics:
- agentic-reasoning
- code-intelligence
- patch-verification
- fault-localization
- static-code-analysis
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Agentic Code Reasoning

## Summary
This paper studies the ability to understand program semantics without executing code, relying only on an agent exploring and reasoning over a codebase, and proposes **semi-formal reasoning** as a structured evidence template. The method outperforms conventional unstructured agent reasoning on three tasks: patch equivalence verification, fault localization, and code question answering.

## Problem
- The paper aims to solve the following: **Can LLM agents reliably analyze code semantics, determine whether patches are equivalent, localize faults, and answer code-understanding questions without running the code?**
- This matters because executing code in real repositories is often expensive, dependency-heavy, and hard to scale; if high-quality semantic judgments can be made statically, they could be used for **RL reward signals, code review, static analysis, and defect investigation**.
- Existing unstructured reasoning tends to “guess the answer” or skip steps, while fully formal verification requires building strict semantics for real repositories and multi-language frameworks, which is too costly in practice.

## Approach
- The core method is **semi-formal reasoning**: rather than letting the model think in a free-form, scattered way, it is required to follow a fixed template and write out **premises, code-path tracing, itemized evidence, and formal conclusions**, like submitting a “reasoning proof sheet.”
- This template is designed as a **certificate**: if the agent has not first found code-based evidence or has not covered key tests/paths, it becomes difficult to jump directly to a conclusion, thereby reducing unsupported assertions.
- The method is a **general mechanism at the prompt-engineering level**, not a specially trained model, nor does it translate code into fully formal systems like Lean or Coq; therefore it is easier to transfer across tasks such as patch equivalence, fault localization, and code QA.
- In the agent setting, the model can use tools to browse the repository, follow call chains, inspect tests and related files, but **cannot execute repository code or tests**; it relies mainly on static-analysis-style code exploration and reasoning.

## Results
- **Patch equivalence verification (170 carefully constructed samples)**: Opus-4.5 improves from **78.2%** under standard reasoning to **88.8%** under semi-formal reasoning, a gain of **10.6 percentage points**; among these, accuracy on non-equivalent samples improves from **78.6% → 82.9%**, and on equivalent samples from **78.0% → 93.0%**. The tradeoff is that the average number of steps increases from **10.08 → 28.17** (about **2.8x**).
- **Verification of real agent-generated patches (200 samples, including test specifications)**: the best result is Opus-4.5 + agentic semi-formal, with **93.0%** accuracy; compared with **difflib 73%**, single-shot **86.0%**, single-shot + file context **87.5%**, and agentic standard **87.0%**. Sonnet-4.5 also reaches **91.5%** under the same setting.
- **Code question answering (RubberDuckBench)**: the abstract states that semi-formal reasoning reaches **87%** accuracy, a gain of **9 percentage points** over standard agentic reasoning; the contributions section also reports gains of **10.8 percentage points** over single-shot **76%**, and **8.7 percentage points** over standard agentic.
- **Fault localization (Defects4J, smaller-scale 43 evaluable bugs)**: with Opus-4.5 in agentic mode, Top-5 (All) improves from **60.5%** to **72.1%**, a gain of **11.6 percentage points**; Top-5 (Any) improves from **81.4%** to **88.4%**, a gain of **7.0 percentage points**. Under single-shot, Top-5 (All) goes from **55.6% → 63.9%**.
- **Fault localization (larger-scale 90 evaluable bugs)**: the paper claims that semi-formal reasoning with Opus-4.5 further improves Top-5 (All) by about **5 percentage points** over the standard mode; in the truncated table provided, the standard value is **43.3%**, but the full semi-formal value is not completely visible in the excerpt.
- The paper’s strongest conclusion is: **through structured agentic reasoning, LLMs can perform meaningful semantic-level code analysis without executing code**, approaching the reliability threshold needed for execution-free / low-execution-dependence verification and RL feedback.

## Link
- [http://arxiv.org/abs/2603.01896v2](http://arxiv.org/abs/2603.01896v2)
