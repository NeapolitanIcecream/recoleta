---
source: arxiv
url: https://arxiv.org/abs/2606.13298v1
published_at: '2026-06-11T12:50:36'
authors:
- Oliver Aleksander Larsen
- Mahyar T. Moghaddam
topics:
- architectural-smells
- difference-in-differences
- ai-code-adoption
- software-maintainability
- java-repositories
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Mining Architectural Quality Under Agentic AI Adoption: A Causal Study of Java Repositories

## Summary
This paper tests whether agentic AI coding adoption changes architectural quality in Java repositories. It finds that adoption is linked to lower architectural smell density, but the drop comes from faster code growth rather than fewer smells.

## Problem
- Prior causal studies on AI coding tools measured code-level outcomes, not architecture-level effects.
- Architectural smells matter because they signal erosion in the dependency graph and hurt maintainability and evolution.
- The paper asks whether agentic AI use changes architectural smell density, which smell types move, and whether any change comes from smell counts or code volume.

## Approach
- The study tracks 151 open-source Java repositories over a 13-month window, with 74 treated repositories and 77 propensity-matched controls.
- It detects agentic AI adoption through repository artifacts such as tool configuration files and Co-Authored-By commit trailers.
- The main design is staggered difference-in-differences with the Borusyak imputation estimator and repository/time fixed effects.
- The outcome is architectural smell density, defined as total smells per KLOC, with separate models for raw smell counts and KLOC to split numerator and denominator effects.
- It also runs event studies, per-smell-type models, and robustness checks including wild cluster bootstrap and Lee bounds.

## Results
- Main effect on architectural smell density: -6.7% with Borusyak imputation (b2 = -0.0698, SE 0.0239, 95% CI [-0.117, -0.023], p = 0.004) over 1,811 monthly observations.
- TWFE-Sun-Abraham confirms the result at -6.6% (p = 0.005).
- Pre-trends are flat: Wald test p = 0.896.
- Raw smell counts do not change: +1.1% (p = 0.82).
- Code volume increases: +12.8% in log KLOC (p = 0.0027), which explains the ASD drop as a denominator effect.
- By smell type, hub-like dependency falls by 5.0% (Holm-adjusted p = 0.003); cyclic dependency is similar at -5.0% but does not survive Holm correction; unstable dependency and god component show no significant density change.
- Tool-stratified estimates are negative for Claude Code (-5.1%, p = 0.039), Copilot (-4.0%, p = 0.005), and Cursor (-13.5%, p < 0.001).

## Link
- [https://arxiv.org/abs/2606.13298v1](https://arxiv.org/abs/2606.13298v1)
