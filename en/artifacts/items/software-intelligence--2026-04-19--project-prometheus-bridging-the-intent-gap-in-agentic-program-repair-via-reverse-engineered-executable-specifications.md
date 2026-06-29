---
source: arxiv
url: http://arxiv.org/abs/2604.17464v1
published_at: '2026-04-19T14:27:27'
authors:
- Yongchao Wang
- Zhiqiu Huang
topics:
- automated-program-repair
- multi-agent-systems
- executable-specifications
- code-intelligence
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Project Prometheus: Bridging the Intent Gap in Agentic Program Repair via Reverse-Engineered Executable Specifications

## Summary
Prometheus is a multi-agent automated program repair system that tries to fix bugs by first inferring an executable requirement in Gherkin, then using that requirement to guide patch generation. The paper claims that this specification-first workflow sharply improves repair accuracy on Defects4J, especially on bugs a strong repair agent could not solve on its own.

## Problem
- Existing agentic program repair systems can generate code, but they often miss the developer's intended behavior; the paper calls this the "Intent Gap."
- Natural-language summaries and generated adversarial tests are too ambiguous to act as strict repair targets, so agents may produce invasive or semantically wrong patches.
- This matters because a patch that passes the immediate failing test can still violate the real requirement, add regressions, or over-edit the codebase.

## Approach
- Prometheus uses three roles: an **Architect** to infer a Gherkin BDD specification from the failure report and relevant code, an **Engineer** to verify that specification, and a **Fixer** to generate the patch.
- The core idea is simple: convert a bug report and failing behavior into an executable requirement, check that the requirement fails on the buggy code and passes on the developer-fixed code, then ask the repair model to satisfy that requirement.
- The verification step is the Requirement Quality Assurance (RQA) Loop, also described as "Sandwich Verification": the inferred spec must fail on \(C_{buggy}\) and pass on \(C_{fixed}\). Only verified specs are used for repair.
- In experiments, the Fixer is restricted to the main suspicious file from Defects4J metadata so the study isolates the value of specification guidance rather than better fault localization.
- The implementation uses Gemini-3.0-Pro as the Architect and Qwen-3.0-Coder as the Fixer.

## Results
- On **680 defects** from **Defects4J v3.0.1** (excluding Closure), the blind Fixer solved **520/680 = 76.5%**, and Prometheus rescued **119** of the remaining **160** failures, for a claimed total of **639/680 = 93.97%** correct patches.
- The paper reports a **Rescue Rate of 74.4%** on the hard set, computed as **119/160** bugs that the blind agent failed to fix.
- On project subsets, reported total repair rates include **Math: 87/106 = 82.1%** with **39 rescues**, **Compress: 43/47 = 91.5%** with **14 rescues**, and **Jsoup: 84/93 = 90.3%** with **25 rescues**.
- Against the paper's comparison table on the same hard-160 setting, **TSAPR** solved **22**, **RepairAgent** solved **27**, and **Prometheus** solved **119**, which the authors describe as a **4.4×** advantage over RepairAgent on hard bugs.
- The paper gives cost numbers from **189 repair sessions**: average total pipeline time **1,261.08 s** per defect, with **5,782,441** average tokens; the Engineer verification stage is the largest share at **671.67 s**, **3,365,986 tokens**, and about **58.2%** of cost.
- Qualitatively, the paper claims the method leads to more minimal, requirement-aligned patches and avoids cases where blind agents hallucinate variables, remove needed logic, or make broad structural edits.

## Link
- [http://arxiv.org/abs/2604.17464v1](http://arxiv.org/abs/2604.17464v1)
