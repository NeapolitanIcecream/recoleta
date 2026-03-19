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
- normative-reasoning
- formal-verification
- requirements-engineering
- responsible-ai
relevance_score: 0.18
run_id: materialize-outputs
language_code: en
---

# Social, Legal, Ethical, Empathetic and Cultural Norm Operationalisation for AI Agents

## Summary
This paper proposes an engineering process for systematically operationalising high-level social, legal, ethical, empathetic, and cultural (SLEEC) norms in AI agents. Its core contribution is converting abstract principles into verifiable rules, implementation constraints, and verification steps, while also surveying existing tools and unresolved challenges.

## Problem
- High-stakes AI agents (such as those used in healthcare, law enforcement, and care robots) need to comply with social, legal, ethical, empathetic, and cultural norms, but existing frameworks often remain at the abstract level of statements like “should be fair” or “respect privacy.”
- Abstract principles are difficult to translate directly into **specific, unambiguous, implementable, and verifiable** system requirements, making it hard to demonstrate that agents truly align with human norms and values.
- Traditional requirements engineering is insufficient for handling issues such as multi-stakeholder participation, norm conflicts, context dependence, and formal compliance guarantees.

## Approach
- Proposes a **5-stage SLEEC-norm operationalisation process**: capability specification definition, normative requirement elicitation, rule well-formedness checking, SLEEC-aware implementation, and compliance verification; failure at any stage should block deployment.
- Uses stakeholder-participatory methods to map high-level principles into operational “agent indicators/proxies,” then bind them to agent capabilities, and finally encode them as SLEEC DSL rules: `when trigger [and guard] then response [within time]`, with support for `unless` defeaters to express exceptions.
- Performs formal checking on rule sets: one route maps rules to tock-CSP and uses FDR / SLEEC-TK to check conflicts and redundancy; another route encodes the overall rule set into FOL* and uses LEGOS / LEGOS-SLEEC to analyse conflicts, redundancy, **insufficiency**, and **over-restrictiveness**.
- In the implementation stage, validated rules are mapped to observable events, monitored variables, internal states, and controllable actions; they are also incorporated into training data patterns and runtime guardrails so that agents are norm-constrained both during learning and deployment, while supporting later norm updates.

## Results
- This paper is primarily a **framework/process and survey contribution**. In the excerpt provided, there are **no quantitative experimental metrics on standard machine learning benchmarks**, nor any precise overall performance numbers.
- The paper provides concrete example rules for an assistive care robot ALMI/TIAGo, such as `MealTime -> InformUser within 10 minutes`, `SmokeDetectorAlarm -> CallEmergencySupport within 2 minutes`, and `HumanOnFloor -> CallEmergencySupport within 4 minutes`.
- Through formal checking, the authors demonstrate a **temporal conflict** example: after a fall, a rule prohibiting help-seeking due to lack of consent conflicts with a rule requiring emergency support to be called within **2 minutes** after a smoke alarm; one repair is to shorten the duration of the no-call prohibition window from **3 minutes** to **1 minute**.
- Through global rule analysis, the authors also identify an **over-restrictiveness** problem: if the user loses responsiveness, the “no consent” condition may block necessary help-seeking; after repair, the rule prohibits calling within **1 minute** only when both “no consent” and “user is responsive” hold, thereby preserving the ability to seek help for an unresponsive fallen user.
- The paper’s strongest claim is that this process can systematically translate high-level governance principles into agent norms that are **traceable, implementable, and verifiable**, while using existing tools to detect conflicts, redundancy, rule insufficiency, and over-restrictiveness before deployment.

## Link
- [http://arxiv.org/abs/2603.11864v1](http://arxiv.org/abs/2603.11864v1)
