---
source: arxiv
url: http://arxiv.org/abs/2604.22601v1
published_at: '2026-04-24T14:28:10'
authors:
- Md Erfan
- Md Kamal Hossain Chowdhury
- Ahmed Ryan
- Md Rayhanur Rahman
topics:
- formal-verification
- dafny
- code-generation
- open-weight-llms
- benchmark-datasets
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# From Natural Language to Verified Code: Toward AI Assisted Problem-to-Code Generation with Dafny-Based Formal Verification

## Summary
This paper studies whether open-weight LLMs can turn natural-language programming problems into **verified Dafny code** instead of plain code that may be wrong. It introduces a 60-problem benchmark and shows that verifier feedback plus method signatures can raise success from near-zero to high verification rates on sampled tasks.

## Problem
- LLMs can write plausible code, but the code often contains logical errors or hallucinations, which matters when software needs correctness guarantees.
- Formal verification can prove code matches a specification, but writing Dafny specifications, loop invariants, and proof annotations is hard and often takes more effort than writing the program.
- Natural-language requirements are ambiguous, and there is little Dafny training data, so mapping NL directly to verified code is a hard synthesis task.

## Approach
- The authors build **NL2VC-60**, a dataset of 60 hand-authored Dafny solutions for complex UVa Online Judge problems, with longer and more detailed natural-language descriptions than prior Dafny benchmarks.
- They evaluate **seven open-weight LLMs** on **11 randomly selected problem sets** using three prompt settings: **contextless prompting**, **signature prompting** with method structure, and **self-healing prompting** that feeds Dafny verifier errors back to the model for iterative repair.
- They use **Dafny** as the verification language, so the model must generate both executable code and the formal annotations needed for proof, such as contracts and loop invariants.
- They add **uDebug** test suites to catch **vacuous verification**, where code passes the verifier with weak or trivial specifications but does not solve the actual problem.
- They also compile a dataset of Dafny-specific compilation and verification errors to study model failure modes.

## Results
- With **contextless prompting**, the paper reports **near-universal failure** across the tested models.
- With structural guidance and repair, performance improves sharply: **Gemma 4-31B** reaches **90.91% verification success** on the sampled evaluation.
- **GPT-OSS 120B** improves from **0%** to **81.82% verification success** when given **signature-guided feedback**.
- The paper claims open-weight LLMs can now synthesize formally verified Dafny programs on complex algorithmic tasks when given verifier-guided iteration and structural anchors.
- The evaluation uses **60 total benchmark problems**, **11 sampled problem sets**, **7 open-weight LLMs**, and dual checking through **formal proof plus uDebug functional tests**.
- The excerpt does not provide a full table of per-model results, dataset-wide averages, or direct numeric comparisons against prior published baselines beyond the reported success rates above.

## Link
- [http://arxiv.org/abs/2604.22601v1](http://arxiv.org/abs/2604.22601v1)
