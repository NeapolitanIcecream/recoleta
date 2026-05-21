---
source: arxiv
url: https://arxiv.org/abs/2605.00742v2
published_at: '2026-05-01T15:43:43'
authors:
- Theodore Papamarkou
- Pierre Alquier
- Matthias Bauer
- Wray Buntine
- Andrew Davison
- Gintare Karolina Dziugaite
- Maurizio Filippone
- Andrew Y. K. Foong
- Vincent Fortuin
- Dimitris Fouskakis
- Jes Frellsen
- "Eyke H\xFCllermeier"
- Theofanis Karaletsos
- Mohammad Emtiyaz Khan
- Nikita Kotelevskii
- Salem Lahlou
- Yingzhen Li
- Fang Liu
- Clare Lyle
- "Thomas M\xF6llenhoff"
- Konstantina Palla
- Maxim Panov
- Yusuf Sale
- Kajetan Schweighofer
- Artem Shelmanov
- Siddharth Swaroop
- Martin Trapp
- Willem Waegeman
- Andrew Gordon Wilson
- Alexey Zaytsev
topics:
- agent-orchestration
- bayesian-decision-theory
- multi-agent-systems
- code-intelligence
- human-ai-interaction
- tool-routing
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# Position: agentic AI orchestration should be Bayes-consistent

## Summary
The paper argues that agentic AI systems should put Bayesian decision rules in the orchestration layer, while leaving LLMs and tools as black-box predictors. It targets routing, stopping, escalation, and budget choices where uncertainty, cost, and risk shape the best action.

## Problem
- LLM agents often must choose which tool or expert to call, whether to ask the user, when to stop, and how much compute to spend; token probabilities do not map cleanly to task-level uncertainty.
- This matters in multi-step or high-stakes systems because bad routing, weak stopping rules, and repeated tool calls can waste budget, add latency, or raise safety risk.
- Making the LLM itself a full Bayesian updater is expensive and may still miss the uncertainty that matters for action selection.

## Approach
- Add a Bayesian controller above LLMs and tools. It tracks a posterior over latent task variables such as whether code will pass tests, which hypothesis is best supported, or which agent is reliable.
- Treat each agent message or tool output as noisy evidence. In the code example, the controller updates `r_t(y) ∝ r_{t-1}(y) p_i(z_t|y)^{α_i}`, where `α_i` tempers the evidence from agent `i`.
- Choose the next action by posterior expected utility or value of information. The controller calls another agent only when the expected gain exceeds cost `c_i`; otherwise it can stop, ask, abstain, or escalate.
- Use recalibration, likelihood tempering, dependence-aware evidence pooling, and escalation when observation models are misspecified or repeated calls produce correlated evidence.
- The paper illustrates the idea with multi-agent code generation/testing, multi-agent hypothesis discussion, and cross-task routing based on learned competence parameters.

## Results
- The paper reports 0 experiments, 0 datasets, and 0 empirical benchmark comparisons. It is a position paper, so it does not claim a measured accuracy, pass-rate, cost, or latency gain.
- Its main claimed result is a design argument: Bayesian control can be applied at 1 orchestration layer without making LLM parameters Bayesian.
- It lists 7 desired properties for practical Bayesian control: cost and utility modeling, low-overhead decisions, compact interaction history, human-AI and multi-agent integration, typed software interfaces, multimodal inputs, and simple user controls.
- It gives 3 concrete design examples: code-generation testing, hypothesis deliberation, and cross-task competence routing.
- In the code example, the controller manages `n` agents, a binary task outcome `Y ∈ {0,1}`, per-agent costs `c_i`, reliability weights `α_i`, and the belief update in Equation (1).

## Link
- [https://arxiv.org/abs/2605.00742v2](https://arxiv.org/abs/2605.00742v2)
