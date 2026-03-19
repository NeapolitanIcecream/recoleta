---
source: arxiv
url: http://arxiv.org/abs/2603.03121v1
published_at: '2026-03-03T15:56:49'
authors:
- Yanqi Su
- Michael Pradel
- Chunyang Chen
topics:
- gui-testing
- change-impact-analysis
- llm-for-testing
- differential-testing
- regression-detection
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# RippleGUItester: Change-Aware Exploratory Testing

## Summary
RippleGUItester is a code-change-oriented GUI exploratory testing system: starting from PRs/Issues and patches, it infers which user scenarios may be affected and performs differential comparison between pre-change and post-change versions to detect regressions. The paper’s core contribution is combining LLM-driven change-impact analysis, scenario expansion, and multimodal GUI differential detection to uncover change-induced defects missed by traditional testing and code review.

## Problem
- As software evolves frequently, a single code modification often introduces new user-visible defects; the authors’ analysis of **97,347** Firefox PRs found that **11,910** PRs introduced new bugs, accounting for **12.2%**.
- Existing regression testing/CI mostly relies on predefined paths, while exploratory testing lacks systematic guidance on “what should be tested around this code change,” making it easy to miss defects triggered by **cross-scenario side effects**, rare event sequences, and special test data.
- The criteria for identifying such defects are also hard to encode manually: GUI changes may be intended updates or regressions, and must be understood in the context of change intent.

## Approach
- Starting from a given PR, the system gathers **change intent** (PR description, linked Issues) and **code changes** (patches, modified files), and uses historical traceability to identify **preceding change intents** in the same code regions to cover potential cross-scenario impacts.
- It uses an LLM for **change-impact analysis** to generate initial end-user-oriented test scenarios: simply put, the model infers “which user interaction paths may be affected” based on “what changed this time and why.”
- It builds a **Scenario Knowledge Base** from historical issues/PRs, retrieves and injects alternative event sequences, and then uses an LLM to complete/instantiate the required **test data**, turning abstract scenarios into executable ones.
- During execution, the LLM translates high-level scenario steps into GUI action commands (such as click/input/scroll), which are run in isolated containers on the **pre-change** and **post-change** versions respectively.
- During detection, it performs **differential analysis**: comparing visual differences in screenshots between the two versions and interpreting those differences in combination with natural-language change intent to distinguish **intended behavioral updates** from **unintended bugs**.

## Results
- Evaluated on **4** real software systems: **Firefox, Zettlr, JabRef, Godot**; the test subjects were **hundreds of real-world code changes** (the abstract/introduction gives only a qualitative scale, and the excerpt does not provide a finer-grained count).
- RippleGUItester found **26** previously unknown bugs that still existed in the latest versions; these issues had previously been missed by **existing test suites, CI pipelines, code review**.
- Post-reporting outcomes: **16** fixed, **2** confirmed, **6** still under discussion, and **2** marked as intended behavior.
- In terms of runtime cost, each PR required an average of **54.8 minutes** and **$5.99**.
- The paper also claims it is the **first change-aware GUI testing system**, capable of detecting GUI regressions earlier, before code is merged or shortly after merging.

## Link
- [http://arxiv.org/abs/2603.03121v1](http://arxiv.org/abs/2603.03121v1)
