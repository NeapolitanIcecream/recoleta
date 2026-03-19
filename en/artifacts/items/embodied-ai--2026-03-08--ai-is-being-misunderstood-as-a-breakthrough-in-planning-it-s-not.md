---
source: hn
url: https://warontherocks.com/2026/02/ai-is-being-misunderstood-as-a-breakthrough-in-planning-its-not/
published_at: '2026-03-08T23:51:23'
authors:
- skoocda
topics:
- military-planning
- large-language-models
- decision-making
- operational-art
- human-in-the-loop
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# AI Is Being Misunderstood as a Breakthrough in Planning. It's Not

## Summary
This article argues that AI has not delivered a “planning breakthrough” in military campaign planning; it has only dramatically reduced the cost of organizing, drafting, and restructuring plans. The truly non-automatable core remains the commander’s judgment about priorities, risk, and trade-offs.

## Problem
- The problem the article addresses is how to correctly understand AI’s role in military planning and avoid mistaking “the ability to quickly generate plans that appear complete, balanced, and reasonable” for “having solved the planning problem.”
- This matters because failure at the campaign level usually does not stem from insufficient information, but from the absence of clear prioritization under conditions of conflicting objectives, limited resources, and adaptive adversaries.
- If AI-generated structured, comprehensive outputs are treated as the decision itself, the places that truly require human judgment and accountability will be obscured by a “polished structure.”

## Approach
- The core method is not a new algorithm, but a reflection on AI’s real value and boundaries based on the author’s and his team’s experience using large language models in an embedded way within **real planning workflows at U.S. Forces Japan**.
- Put simply, the author argues that AI should be treated as a **tool for rapidly generating multiple internally coherent frameworks**, not as an “optimizer that provides the best planning answer.”
- The specific mechanism is to have AI generate multiple task frameworks, objective organizations, and narrative structures that all appear reasonable, then compare where each framework distorts, omits, or incorrectly downplays certain responsibilities, thereby exposing the conflicts that genuinely require command judgment.
- The author believes AI is most useful not for proving which plan is “correct,” but for more quickly revealing **which plans cannot withstand constraints, competing demands, and multiple responsibilities**.
- From this perspective, planners should present commanders not only with recommended plans, but also with clear identification of each AI-generated framework’s failure points, trade-offs, and risks that must be accepted.

## Results
- The article **does not provide formal experiments, benchmark datasets, or quantitative metrics**, so there are no reportable numerical results such as accuracy, win rate, or percentage efficiency gains.
- The strongest experiential conclusion offered by the author is that AI does indeed “**raise the floor**,” significantly reducing the time and labor required to generate and revise internally consistent planning concepts, but it also “**collapses the median**,” making genuine insight relatively scarcer.
- In the U.S. Forces Japan case, the team used **Maven Smart Systems (Anthropic Claude Sonnet)** on classified networks and also tested **Ask Sage (including OpenAI and other models)**; these models could all reliably generate planning frameworks that were “analytically defensible but conceptually fragile.”
- The common pattern across these AI frameworks was that **each framework failed in a different place**, usually by overemphasizing one role while downplaying another, showing that the headquarters’ mission could not be coherently explained through a single logic.
- The key claim the author draws from this is that AI’s breakthrough lies not in replacing judgment, but in **more quickly locating where judgment must intervene**; that is, using multiple “seemingly reasonable” plans to diagnose structural tension rather than pursuing one “complete optimal” plan.
- In the end, the command recommendation in the case did not converge on a single framework, but instead **accepted the structural inconsistency of three core roles coexisting** in order to preserve their independently ranked priorities; this is the article’s most concrete practical conclusion, though it remains a qualitative claim rather than a quantitatively validated one.

## Link
- [https://warontherocks.com/2026/02/ai-is-being-misunderstood-as-a-breakthrough-in-planning-its-not/](https://warontherocks.com/2026/02/ai-is-being-misunderstood-as-a-breakthrough-in-planning-its-not/)
