---
source: arxiv
url: http://arxiv.org/abs/2604.10800v1
published_at: '2026-04-12T20:22:23'
authors:
- Jugal Gajjar
topics:
- cross-language-code-analysis
- vulnerability-detection
- agentic-validation
- automated-program-repair
- code-llms
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Verify Before You Fix: Agentic Execution Grounding for Trustworthy Cross-Language Code Analysis

## Summary
This paper proposes a cross-language vulnerability analysis pipeline that detects, verifies, and repairs code across Java, Python, and C++. Its main claim is that repair should only happen after execution confirms the bug is exploitable, which cuts false actions in the pipeline.

## Problem
- Vulnerability pipelines often treat model predictions as facts, so false positives flow into later stages and waste repair effort.
- Existing tools usually split detection, validation, and repair into separate systems, and many require a different model per programming language.
- This matters because security repair on unverified findings can produce unnecessary patches, lower trust, and miss the real exploit path.

## Approach
- The system uses a three-stage loop: detect suspicious code, verify exploitability by execution, then repair only the confirmed cases.
- For detection, it converts Java, Python, and C++ code into a shared Universal AST and combines two signals: a GraphSAGE embedding of program structure and a Qwen2.5-Coder-1.5B embedding of source semantics.
- A learned two-way gate weights the structural and semantic branches per sample, which also gives a direct explanation of which branch drove the prediction.
- For validation, an LLM agent builds exploit hypotheses and test harnesses, runs them in sandboxed Docker environments, and requires confirming execution evidence before a case is marked exploitable.
- For repair, a LoRA-tuned Qwen2.5-Coder-1.5B-Instruct model generates minimal patches, reruns detection, and iterates up to five times; failed cases are handed to humans with diagnostic traces.

## Results
- Intra-language detection reached **89.84% to 92.02% accuracy** and **0.8837 to 0.9109 F1** across Java, Python, and C++.
- Zero-shot cross-language detection reached **74.43% to 80.12% F1** across six train-test language pairs, with **0.7631 average F1** for the hybrid model versus **0.6981** for semantic-only and **0.5426** for structural-only.
- The validation stage confirmed exploitability for flagged samples in **66.84% to 71.49%** of cases, rejected detector false positives in **58.72% to 62.37%** of cases, and recovered **11.76% to 16.21%** missed vulnerabilities at **2.67% to 3.98%** spurious rate.
- Repair success was **81.37% to 87.27%** within five iterations, averaging **2.3 to 3.4** iterations; post-repair pass rates were **90.44% to 93.15%**.
- End to end, the full pipeline resolved **69.74%** of vulnerabilities, eliminated **61.24%** of false positives, avoided **73.13%** of unnecessary repairs, and had **12.27%** total pipeline failure.
- Ablations show the two key components matter: removing uAST cut average cross-language F1 by **23.42%**, and disabling execution-grounded validation increased unnecessary repairs by **131.7%** and reduced end-to-end success by **9.56 percentage points**.

## Link
- [http://arxiv.org/abs/2604.10800v1](http://arxiv.org/abs/2604.10800v1)
