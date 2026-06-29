---
source: arxiv
url: https://arxiv.org/abs/2605.17169v1
published_at: '2026-05-16T21:56:33'
authors:
- Jinwei Hu
- Xinmiao Huang
- Qisong He
- Youcheng Sun
- Yi Dong
- Xiaowei Huang
topics:
- agentic-ai
- ai-provenance
- responsibility-attribution
- multi-agent-systems
- ai-governance
- software-agents
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Responsible Agentic AI Requires Explicit Provenance

## Summary
The paper argues that responsible agentic AI needs explicit provenance across design, execution, deployment, and population monitoring. It proposes causal contribution, epistemic position, and a responsibility tensor to assign responsibility when harms come from multi-step agent behavior.

## Problem
- Agentic AI can call tools, use memory, plan over many steps, and coordinate across agents, so harm can come from the full trajectory rather than one model output or one component.
- Per-component audits cannot show which party caused a harmful outcome when developers, tool authors, platform operators, and deployers all shaped the system.
- This matters for software agents and other delegated systems because users and regulators cannot trust systems that cannot explain who did what, what was foreseeable, and when intervention should have happened.

## Approach
- The paper defines explicit provenance as records that support three properties: quantifiability of causal contribution, traceability across execution records, and interventionability before harm becomes irreversible.
- It defines causal contribution as the change in harm probability when a party's relevant decisions are removed or neutralized in a counterfactual trajectory.
- It adds epistemic position, which records what each party knew or should have known before the harm.
- It defines a responsibility assignment function that gives each party a responsibility weight and assigns leftover responsibility to institutions when individual attribution is incomplete.
- It extends this into a responsibility tensor over parties, harm events, and sociotechnical dimensions, then maps the work into four lifecycle layers: design, engineering, deployment, and population-scale monitoring.

## Results
- The excerpt does not provide detailed experimental metrics for the paper's preliminary experiments; it only states that causal contribution is estimable online from execution prefixes and can support intervention before irreversible harm accumulates.
- The paper cites adoption evidence: McKinsey reports 23% of respondents scaling agentic AI and 39% experimenting; PwC reports 79% of senior executives say AI agents are already being adopted in their companies.
- The paper cites risk evidence for tool and agent settings: indirect prompt injection reached a 47% attack rate against GPT-4 across 17 tool-integrated systems.
- It cites sandbox evidence that over 68% of scenarios show potential real-world agent failures.
- It cites marketplace evidence that over 90% of high-popularity ClawHub skills fail security review.
- The main claimed result is a formal route to computable responsibility: causal contribution plus foreseeability determines party-level responsibility, and unassigned responsibility is allocated to an institutional layer.

## Link
- [https://arxiv.org/abs/2605.17169v1](https://arxiv.org/abs/2605.17169v1)
