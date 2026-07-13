---
source: arxiv
url: https://arxiv.org/abs/2607.09553v1
published_at: '2026-07-10T16:00:57'
authors:
- Vincenzo Luigi Bruno
- Alessandro Giagnorio
- Daniele Bifolco
- Leon Wienges
- Massimiliano Di Penta
- Gabriele Bavota
topics:
- software-repair-agents
- code-intelligence
- bug-reporting
- automated-software-production
- agentic-workflows
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# Writing Bug Reports for Software Repair Agents: What Information Matters Most?

## Summary
The paper studies which bug-report information helps software repair agents generate patches that pass tests. It finds that repair guidance, especially affected-code locations and suggested fixes, is more useful to agents than longer human-oriented descriptions.

## Problem
- In agentic-first development, a bug report becomes the agent's task specification, so poorly targeted information can reduce the chance of a correct repair.
- Existing bug-report guidance emphasizes human understanding, reproduction, and behavioral context, while evidence about information that helps automated repair remains limited.

## Approach
- The authors annotate all 500 issues in SWE-bench Verified with nine information types, then retain 441 defect reports after excluding 41 feature requests and 18 refactoring tasks.
- They run mini-SWE-agent with GPT-5-mini, MiniMax M2.5, and Gemini 3 Flash, using test-suite passage as the repair-success measure.
- A mixed-effect binomial regression estimates associations between information types and agent success while controlling for issue length, code mentions, gold-patch size, difficulty, model, and repository effects.
- An ablation study removes information categories from 65 information-complete reports and evaluates 4,680 mutated-task runs.

## Results
- The study uses 3,969 observational runs: 441 issues, 3 LLM backbones, and 3 repetitions per issue. Exact odds ratios and pass-rate improvements are not included in the provided excerpt.
- Localization cues, especially references to affected lines and functions, have positive associations with successful repairs.
- Suggested fixes in code or natural language show some of the strongest positive associations with test-suite passage probability.
- Removing reproduction steps or expected behavior does not significantly reduce agent effectiveness when localization or repair suggestions remain.
- The largest degradation occurs when both localization cues and suggested fixes are removed, supporting the claim that agents benefit from information that narrows where to inspect or how to change the code.
- Annotation covered 3,752 spans across 500 issues, with 78.6% character-level agreement and issue-level Cohen's kappa of 0.57; the ablation editing process reached kappa 0.96.

## Link
- [https://arxiv.org/abs/2607.09553v1](https://arxiv.org/abs/2607.09553v1)
