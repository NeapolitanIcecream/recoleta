---
source: arxiv
url: http://arxiv.org/abs/2603.03515v1
published_at: '2026-03-03T20:48:01'
authors:
- Subramanyam Sahoo
topics:
- ai-governance
- military-ai
- ai-agents
- human-control
- safety-metrics
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# The Controllability Trap: A Governance Framework for Military AI Agents

## Summary
This paper proposes AMAGF, a governance framework for military agentic AI. Its core idea is to shift “human control” from a binary concept to a continuously measurable and dynamically managed quality of control. It focuses on six types of agentic control failures that traditional safety frameworks struggle to cover, and provides three layers of mechanisms: prevention, detection, and correction.

## Problem
- Existing military AI governance mostly emphasizes that there **should be human control**, but does not answer **how to implement, monitor, and restore control in specific agentic systems**.
- AI systems with natural language understanding, world models, long-horizon planning, tool use, and multi-agent coordination can produce six new failure modes: drift in instruction interpretation, absorbed corrections, belief resistance, accumulation of irreversible commitments, state divergence, and group-level breakdowns in control.
- This matters because in military settings, once humans’ actual control over the system degrades, accountability, compliance, and safety boundaries all break down, while traditional automation governance mechanisms do not have corresponding tools.

## Approach
- The paper proposes the **Agentic Military AI Governance Framework (AMAGF)**, divided into three pillars: **Preventive Governance** (reducing the probability of failure before deployment and during operation), **Detective Governance** (real-time detection of control degradation), and **Corrective Governance** (restoring control or safely degrading operations).
- It uses six quantifiable indicators corresponding to the six failure types, for example: **IAS** measures consistency of instruction interpretation, **CIR** measures whether corrections actually change behavior, **EDI** measures divergence between agent and operator judgment, **Irreversibility Budget** limits the accumulation of irreversible tool use, **SF** tracks the freshness of state synchronization, and **SCS** measures group coherence.
- The core mechanism is the **Control Quality Score (CQS)**: it takes the **minimum** of the six normalized indicators as the real-time control quality score. The simplest interpretation is: **control capability is determined by its weakest link**.
- When CQS declines, the system triggers graded responses: from normal monitoring, to enhanced checks, to allowing only reversible actions, step-by-step authorization, and ultimately entry into a safe state; it also provides corrective procedures such as belief reset, group isolation, and post hoc review.
- The framework also allocates responsibility across five institutional roles: developers, procurers, operational commanders, national regulators, and international institutions, making governance not just a technical property but also an organizational responsibility structure.

## Results
- The paper **does not provide real experimental benchmarks, public datasets, or quantitative comparison results against existing methods**; the main evidence is a designed worked scenario rather than an empirical evaluation.
- In the example mission involving 8 surveillance drones, the initial indicators are **IAS=0.95, CIR=0.92, EDI=0.05**, with overall **CQS=0.92**, placing the system in **Normal**.
- After the sensor deception event at **t=23 min**, cognitive divergence increases, **n3 drops to 0.64**, and **CQS falls from 0.92 to 0.64**, triggering **Elevated Monitoring**.
- At **t=28 min**, after the commander’s correction, one agent produces only **40%** of the expected behavioral change, yielding **CIR=0.4**; at this point **CQS=0.58**, entering **Restricted Autonomy**, and the irreversibility budget is frozen.
- After partial belief reset and evidence-tracing audit at **t=33 min**, **n3 recovers to 0.82**, **CIR recovers to 0.88** in subsequent probes, and **CQS rises back to 0.71**.
- By **t=45 min**, synchronization checks are complete and **CQS recovers to 0.86**; the authors claim the system returns from an attack-induced restricted state to normal operation in about **22 minutes** without requiring mission abort.

## Link
- [http://arxiv.org/abs/2603.03515v1](http://arxiv.org/abs/2603.03515v1)
