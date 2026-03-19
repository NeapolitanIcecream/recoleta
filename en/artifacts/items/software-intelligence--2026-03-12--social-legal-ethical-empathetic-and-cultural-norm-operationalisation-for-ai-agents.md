---
source: arxiv
url: http://arxiv.org/abs/2603.11864v1
published_at: '2026-03-12T12:37:39'
authors:
- Radu Calinescu
- Ana Cavalcanti
- Marsha Chechik
- Lina Marsso
- Beverley Townsend
topics:
- ai-governance
- ai-agents
- formal-verification
- requirements-engineering
- norm-alignment
relevance_score: 0.38
run_id: materialize-outputs
language_code: en
---

# Social, Legal, Ethical, Empathetic and Cultural Norm Operationalisation for AI Agents

## Summary
This paper proposes an engineering process for systematically converting high-level social, legal, ethical, empathetic, and cultural (SLEEC) norms into verifiable requirements for AI agents. It is more of a framework-and-agenda paper, focusing on defining the process, toolchain, and unresolved challenges, rather than reporting new model performance benchmarks.

## Problem
- The paper addresses the problem of how to translate abstract norms from OECD, UNESCO, regulations, and industry guidelines into concrete, implementable, and verifiable requirements for AI agents; this matters because agents in high-risk settings such as healthcare, law enforcement, and care robots make decisions that affect life, safety, privacy, and autonomy.
- Traditional requirements engineering methods are not well suited to this task, because they struggle to handle multiple stakeholders, abstract value principles, norm conflicts, and formal guarantees of “whether compliance holds.”
- If high-level values cannot be grounded in explicit rules and verified, then even if AI agents are functionally useful, they cannot be shown to align with human norms and values.

## Approach
- The core method is a **5-stage SLEEC norm operationalisation process**: first define agent capabilities, then extract executable normative requirements from high-level principles, next check whether the rule set is well-formed, then map the rules to training and runtime mechanisms, and finally verify whether the agent complies with those rules.
- At the simplest level, it turns abstract statements like “should respect privacy/autonomy/safety” into formal rules like: “when X occurs and condition Y holds, the agent must perform Z within time T, unless exception condition D applies.”
- The paper uses the **SLEEC DSL** to express rules, and applies two complementary kinds of formal analysis: one based on process algebra / tock-CSP + FDR to detect conflicts and redundancies; the other based on FOL* + LEGOS to analyze the global sufficiency and over-restrictiveness of the full rule set.
- At the implementation level, validated rules are lowered into observable events, measured variables, states, and actions, while also informing training-data schema design and deployment-time runtime guardrails, in order to constrain agent decisions and support subsequent norm updates.
- The paper uses the ALMI care robot as a running case study to show how normative requirements are derived, debugged, and revised from capabilities to rules.

## Results
- The paper **does not provide quantitative performance results on standard machine learning benchmarks**, nor does it report numbers such as accuracy, F1, win rate, or large-scale comparative experiments.
- The clear structural result is the proposal of a **5-stage** operationalisation process: capability specification, normative requirement elicitation, well-formedness checking, SLEEC-aware implementation, and compliance verification; and it states that failure at any stage should block deployment.
- The paper gives **numerical time constraints** in example ALMI robot rules, such as `MealTime -> InformUser within 10 minutes`, `SmokeDetectorAlarm -> CallEmergencySupport within 2 minutes`, and `HumanOnFloor -> CallEmergencySupport within 4 minutes`.
- The paper shows a specific conflict repair: in the original rules, the prohibition window on emergency calls conflicted with the fire-alarm scenario, so the prohibition duration in the relevant defeater was shortened from **3 minutes to 1 minute** to resolve the conflict.
- The paper also shows an “over-restriction” repair: to avoid the situation where an unresponsive fallen person can never be helped because they cannot consent, it introduces a new `userResponsive` capability and refines the prohibition condition so that calling for help is blocked only when “**not humanAssents and userResponsive**”.
- The paper’s strongest claim is that, through the combination of DSL, FDR, LEGOS, SLEEC-TK, and LLM-guided debugging tools, abstract SLEEC principles can be transformed into AI agent norms that are **checkable, debuggable, implementable, and verifiable**, while also defining a future research and policy agenda.

## Link
- [http://arxiv.org/abs/2603.11864v1](http://arxiv.org/abs/2603.11864v1)
