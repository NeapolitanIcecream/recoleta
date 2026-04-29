---
source: arxiv
url: http://arxiv.org/abs/2604.20938v1
published_at: '2026-04-22T13:45:12'
authors:
- Biswa Sengupta
- Jinhua Wang
topics:
- bayesian-optimization
- llm-agents
- code-intelligence
- agent-harness
- automated-tuning
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# HARBOR: Automated Harness Optimization

## Summary
This paper argues that the agent harness, not the base model, is the main source of complexity in long-horizon coding agents, and that tuning harness flags by hand fails once interactions grow. It proposes Harbor, a Bayesian optimization system for automated harness configuration, and supports the case with a production coding-agent study.

## Problem
- Long-horizon agents depend on many harness features such as caching, memory, compression, tool prediction, and self-evaluation, and these features interact in ways that make manual tuning unreliable.
- In the cited production setting, the harness is most of the system code: an audit of Claude Code is quoted at about 98.4% harness code versus 1.6% AI decision logic, and a 100-tool agent can spend up to 40% of its context window on tool descriptions before the user task.
- This matters because teams ship harness changes through small ablation loops, but the paper's case study shows that stacking published ideas can reduce pass rate instead of improving it.

## Approach
- The paper formulates automated harness optimization as constrained noisy Bayesian optimization over a mixed configuration space of harness flags and evaluation fidelities, with heterogeneous runtime cost.
- Harbor uses a block-additive SAAS surrogate model, a multi-fidelity cost-aware acquisition rule, and TuRBO trust regions to pick which flag combinations to test next.
- It adjusts rewards for cold-start effects so cross-session features are not judged too harshly when benchmark tasks do not let memory warm up.
- It adds a posterior chance-constrained safety check and telemetry-driven silent-flag detection so broken or inactive features can be excluded during search.
- The concrete testbed is a flag-gated codex-py coding agent harness with about 30 enhancement capabilities overall and 9 evaluated flags including semantic cache, cross-session memory, conversation compression, trajectory replay, speculative tool prediction, self-evaluation, ACON compression, Reflexion, and PASTE.

## Results
- In the manual tuning case study on Terminal-Bench 2 with 89 tasks, the all-flags-off baseline passed 15/89 tasks.
- Round B, which enabled 5 native harness flags, reached 17/89, the only clean improvement over baseline in the reported tuning rounds.
- Adding a self-evaluation gate in Round C dropped performance to 13/89, a decrease of 4 tasks versus B.
- Adding ACON, Reflexion, and PASTE in Round D dropped performance to 12/89, a decrease of 5 tasks versus B.
- The oracle union over all tested configurations reached 81/89, which the authors use as evidence that performance is highly configuration-dependent and that no single hand-tuned stack captured most of the available wins.
- The excerpt does not provide final end-to-end quantitative Harbor search results beyond the manual A-D study, so the strongest concrete claim for Harbor in this text is the optimization formulation and reference solver design rather than a reported search win over manual tuning.

## Link
- [http://arxiv.org/abs/2604.20938v1](http://arxiv.org/abs/2604.20938v1)
