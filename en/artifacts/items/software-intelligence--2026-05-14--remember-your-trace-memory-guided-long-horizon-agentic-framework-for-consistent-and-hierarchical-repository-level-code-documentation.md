---
source: arxiv
url: https://arxiv.org/abs/2605.14563v1
published_at: '2026-05-14T08:35:20'
authors:
- Suyoung Bae
- Jaehoon Lee
- Changkyu Choi
- YunSeok Choi
- Jee-Hyong Lee
topics:
- code-documentation
- repository-level-code-intelligence
- long-horizon-agents
- agent-memory
- software-engineering-automation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Remember Your Trace: Memory-Guided Long-Horizon Agentic Framework for Consistent and Hierarchical Repository-Level Code Documentation

## Summary
MemDocAgent generates repository documentation as one stateful agent run, so earlier retrievals and written documents guide later documents. The paper claims higher completeness, truthfulness, helpfulness, and information sufficiency than open-source and closed-source documentation baselines.

## Problem
- Repository-level documentation needs consistent descriptions across functions, modules, and the full project because developers and coding agents use it to understand large codebases.
- Existing systems document components independently, which causes repeated source-file retrieval, reported at 50% average overlap, and conflicting descriptions, reported at 13% average cross-document inconsistency.
- Prior outputs often cover only one level of detail, so they miss either implementation details or repository-level architecture.

## Approach
- MemDocAgent builds a dependency graph and fixes a traversal order before generation. Dependencies are documented before dependents, modules after child components and submodules, and the repository after modules.
- A single agent processes all documentation units in one long run instead of resetting for each component.
- RepoMemory stores generated documents, extracted claims, dependency links, source code, verification scores, child units, and cached search results.
- The agent uses four actions: Read retrieves context from RepoMemory or the codebase, Write drafts a document, Verify checks factual quality and cross-document conflicts, and Finish commits the accepted document to memory.
- Verification uses self-scores for factual consistency, completeness, and helpfulness, plus a local NLI-based contradiction check against already verified related documents. The reported verification threshold is 0.9.

## Results
- On 20 Python repositories from DevEval, MemDocAgent with Qwen3-Coder produced 3,323 documents and scored 0.979 completeness, 0.916 truthfulness, and 0.690 helpfulness. The strongest open-source baseline scores in the same Qwen3-Coder group were 0.845 completeness, 0.835 truthfulness, and 0.628 helpfulness.
- With GPT-5-mini, MemDocAgent scored 0.958 completeness, 0.952 truthfulness, and 0.800 helpfulness across 3,323 documents. The strongest open-source baseline scores in that group were 0.860 completeness, 0.850 truthfulness, and 0.708 helpfulness.
- Against closed-source baselines, DeepWiki scored 0.920 completeness, 0.762 truthfulness, and 0.755 helpfulness across 404 documents; Claude-Code /init scored 0.744 completeness, 0.734 truthfulness, and 0.696 helpfulness across 20 documents. GPT-5-mini MemDocAgent exceeded both on all three listed aggregate metrics.
- The paper reports that MemDocAgent eliminates repeated source-file retrieval and reduces cross-document inconsistency by 75.5% compared with existing systems.
- At separate levels, GPT-5-mini MemDocAgent scored 0.952/0.974/0.750 for component completeness/truthfulness/helpfulness, 0.974/0.924/0.858 for modules, and 0.949/0.959/0.791 for repository-level docs.
- For information sufficiency, the paper evaluates 564 DevEval component test cases by regenerating missing function bodies from documentation and signatures. The excerpt states MemDocAgent performs best on this fourth criterion, but it does not provide the Pass@k or CodeBLEU numbers.

## Link
- [https://arxiv.org/abs/2605.14563v1](https://arxiv.org/abs/2605.14563v1)
