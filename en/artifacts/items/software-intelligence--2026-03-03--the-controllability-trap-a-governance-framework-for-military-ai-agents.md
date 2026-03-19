---
source: arxiv
url: http://arxiv.org/abs/2603.03515v1
published_at: '2026-03-03T20:48:01'
authors:
- Subramanyam Sahoo
topics:
- ai-governance
- military-ai
- agent-safety
- control-metrics
- multi-agent-systems
relevance_score: 0.28
run_id: materialize-outputs
language_code: en
---

# The Controllability Trap: A Governance Framework for Military AI Agents

## Summary
This paper proposes AMAGF to govern control failures of autonomous AI agents in military contexts. Its core contribution is to shift the question of “whether there is human control” from a binary judgment to a continuously measurable real-time score, CQS, which then triggers graduated interventions.

## Problem
- The problem the paper addresses is that existing military AI governance frameworks emphasize the principle of “meaningful human control,” but do not answer **how agentic AI loses control in real deployments, how to detect it, and how to restore control**.
- This matters because modern AI agents have capabilities such as natural language understanding, long-horizon planning, tool use, persistent operation, and multi-agent coordination, which create six types of control failures not seen in traditional automated systems: interpretive drift, correction absorption, epistemic resistance, irreversible commitment, state divergence, and cascading loss of control.
- If these failures cannot be quantified and governed, command responsibility, compliance, and safety boundaries in military settings will all be weakened.

## Approach
- The authors propose the **Agentic Military AI Governance Framework (AMAGF)**, organized into three layers: **Preventive** (reducing the probability of loss of control in advance), **Detective** (detecting declines in control quality during operation), and **Corrective** (restoring control or safely degrading after loss of control).
- The core mechanism is the **Control Quality Score (CQS)**: the six control dimensions are standardized and then the minimum value is taken, reflecting that “control quality is only as strong as its weakest link.” The six dimensions correspond to interpretive alignment, correction effectiveness, epistemic consistency, remaining irreversibility budget, synchronization freshness, and swarm coherence.
- Measurable mechanisms are designed for each of the six failure types, such as Interpretive Alignment Score, Correction Impact Ratio, Epistemic Divergence Index, Irreversibility Budget, Synchronisation Freshness, and Swarm Coherence Score, with formalized formulas, thresholds, and responsibility assignments.
- At the simplest level, the method is: **continuously measure whether humans and agents remain aligned and controllable; once any dimension worsens, automatically escalate restrictions on agent authority, from increased checks to allowing only reversible actions, and then entering a safe state.**
- The framework also adds mechanisms such as control probes, belief reset, swarm isolation recovery, and post hoc governance review, and assigns responsibilities across five actor groups: developers, procurers, commanders, regulators, and international organizations.

## Results
- This paper is primarily a **governance framework / conceptual methods paper** and does not provide experimental benchmarks on real datasets or statistically significant results; its quantitative results mainly come from an **illustrative operational scenario**.
- In the case of 8 surveillance drones, all indicators are normal at mission start, with **CQS=0.92**; at **t=23 min**, after encountering spoofed sensor data, epistemic consistency declines and **CQS drops to 0.64**, entering **Elevated**.
- At **t=28 min**, after the commander issues a correction, 1 agent shows partial “correction absorption,” with **CIR=0.4**; meanwhile, the irreversibility budget is consumed, producing an overall **CQS=0.58**, which enters **Restricted**, allowing only reversible actions.
- At **t=33 min**, after triggering partial **belief reset** and a provenance audit, epistemic and correction metrics recover and **CQS rises to 0.71**, returning to **Elevated**.
- At **t=45 min**, after completing synchronization checks, the system recovers to **CQS=0.86**, returning to **Normal**. The paper claims this shows the framework can restore the system from an attack-induced restricted state to normal operation in about **22 minutes** without aborting the mission.
- The paper also provides several governance thresholds: for example, interpretive alignment alert threshold **<0.7**, correction impact **<0.6**, epistemic consistency **<0.6**, remaining irreversibility budget **<0.3**, synchronization freshness **<0.5**, swarm coherence **<0.7**; and five CQS response bands (e.g. **<0.2** enters Safe State).

## Link
- [http://arxiv.org/abs/2603.03515v1](http://arxiv.org/abs/2603.03515v1)
