---
source: arxiv
url: http://arxiv.org/abs/2604.21965v1
published_at: '2026-04-23T17:59:18'
authors:
- Benjamin Kohler
- David Zollikofer
- Johanna Einsiedler
- Alexander Hoyle
- Elliott Ash
topics:
- llm-agents
- scientific-reproducibility
- paper-to-code
- social-science
- code-generation
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Read the Paper, Write the Code: Agentic Reproduction of Social-Science Results

## Summary
This paper tests whether LLM agents can reproduce published social-science results from the paper’s methods description and original data alone, without access to the authors’ code or reported numbers. On 48 human-verified reproducible papers, the stronger agent setups recover many published coefficients, but success depends heavily on the model, scaffold, and how fully the paper specifies its methods.

## Problem
- The paper studies whether an agent can reimplement an empirical analysis from a paper and its data, without seeing the original code, results, or full PDF during coding.
- This matters because papers, not code repositories, are supposed to communicate the method well enough for independent reproduction.
- Prior social-science benchmarks usually gave agents the original code; this work targets stricter paper-to-code reproduction and uses deterministic evaluation instead of LLM judging.

## Approach
- The authors build a four-step pipeline: extract methods/data/results from the paper package, blind the original result tables, have an agent write fresh Python code to fill those tables, then compare reproduced cells against the originals.
- Method extraction converts the paper into a structured description of datasets, filters, variable construction, and table-specific model specs, while removing numerical results.
- Reimplementation agents run in an isolated workspace with only extracted methods, table templates, and data. They cannot access the original code or paper. The authors audit runs for forbidden file access and hardcoded outputs.
- Evaluation is deterministic and cell-level: they compare signs, percent deviation, and for coefficients the gap scaled by the original standard error. They also assign letter grades based on deviation.
- An error-attribution step traces failures to missing data, paper-versus-code mismatch, extraction errors, or agent mistakes.

## Results
- Dataset: 48 papers from I4Replication, 222 tables, 14,214 table cells, including 5,149 coefficients and 4,253 standard errors.
- Completion rates are high at the paper and table level: agents produce usable results for 92% to 100% of papers and 82% to 97% of tables. Cell completion ranges from 52% to 72% overall; coefficient completion averages 82% and standard-error completion 80%.
- For reproduced coefficients, sign agreement ranges from 78% (SWE-Agent + GPT-5.4) to 91% (OpenCode + GPT-5.4). The paper gives a 68% naive positive-sign baseline.
- The best setup, OpenCode + GPT-5.4, places over 80% of reproduced coefficients within the original 95% confidence interval. The worst-performing setup still exceeds 50%.
- The introduction states that for the three best agents, reproduced and original coefficients agree on sign over 85% of the time and fall within the 95% confidence interval over 70% of the time.
- OpenCode + GPT-5.4 is the top system, outperforming Claude Code with Opus 4.6, Codex CLI with GPT-5.3/5.4, and OpenCode with GLM-5. The authors report that scaffold choice matters a lot, and OpenCode’s edge comes with much higher token use, cost, and runtime.
- Root-cause analysis says many failures come from underspecified papers, with a smaller share due to extraction mistakes or agents failing to follow the extracted method.

## Link
- [http://arxiv.org/abs/2604.21965v1](http://arxiv.org/abs/2604.21965v1)
