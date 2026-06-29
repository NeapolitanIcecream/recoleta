---
source: arxiv
url: http://arxiv.org/abs/2604.19400v1
published_at: '2026-04-21T12:26:54'
authors:
- Tobias Kiecker
- Jan Arne Sparka
- Martin Reuter
- Albert Ziegler
- Lars Grunske
topics:
- code-documentation-consistency
- llm-test-generation
- automatic-program-analysis
- software-testing
- api-documentation
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# CASCADE: Detecting Inconsistencies between Code and Documentation with Automatic Test Generation

## Summary
Cascade detects mismatches between method documentation and code by turning documentation into executable tests, then checking those tests against both the original code and a code version regenerated from the same documentation. The paper targets high precision, with the main guard against false alarms coming from this two-step execution check.

## Problem
- The paper solves code-documentation inconsistency detection at the method level, where docs say one thing and the implementation does another.
- This matters because wrong API documentation misleads users, can cause downstream bugs, and adds maintenance cost.
- A practical detector must keep false positives low, since developers still need to inspect each report by hand.

## Approach
- Cascade uses an LLM to read natural-language documentation and generate unit tests that encode the documented behavior.
- It runs those tests on the existing implementation. If all tests pass, Cascade reports no evidence of inconsistency.
- If some generated tests fail, Cascade does a second check: it asks the LLM to generate a fresh implementation from the same documentation.
- Cascade reports an inconsistency only when at least one test changes from **fail on original code** to **pass on regenerated code** (`f2p > 0`), and no test changes from **pass on original code** to **fail on regenerated code** (`p2f = 0`).
- The tool also includes a repair loop for generated tests that do not compile, with up to 3 repair attempts.

## Results
- Evaluation uses a new dataset with **71 inconsistent** and **814 consistent** code-documentation pairs from open-source **Java** projects.
- The paper claims this dataset is the first one built from **real, developer-confirmed semantic inconsistencies** in executable Java projects.
- On additional **Java, C#, and Rust** repositories, Cascade found **13 previously unknown inconsistencies**.
- Of those **13** findings, **10** were later fixed by developers.
- The excerpt does **not provide standard quantitative metrics** such as precision, recall, F1, or accuracy, and it does **not include baseline comparison numbers**.

## Link
- [http://arxiv.org/abs/2604.19400v1](http://arxiv.org/abs/2604.19400v1)
