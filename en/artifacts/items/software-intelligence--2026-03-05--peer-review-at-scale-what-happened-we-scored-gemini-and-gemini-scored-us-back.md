---
source: hn
url: https://blog.unratified.org/2026-03-05-peer-review-gemini/
published_at: '2026-03-05T23:59:42'
authors:
- 9wzYQbTYsAIc
topics:
- llm-evaluation
- hallucination-analysis
- peer-review
- ai-auditing
- human-rights-scoring
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Peer Review at Scale: What Happened: We Scored Gemini and Gemini Scored Us Back

## Summary
This article documents a closed-loop “AI peer review” experiment: a human rights observatory system first scored the Gemini website, after which Gemini in turn evaluated the system, exposing a behavioral pattern of high-confidence fabrication in unfamiliar domains that could be corrected within a session but not retained across sessions. From this, the author proposes GEO (Grounded Epistemic Override) and several confabulation cascade phenomena, emphasizing the importance of evidence constraints, reviewable methods, and multi-reviewer consensus in AI evaluation.

## Problem
- The article addresses this question: when LLMs perform “evaluation/review/peer review” tasks, do they build seemingly authoritative analyses on fabrications that were never retrieved, never measured, and are produced purely through pattern matching?
- This matters because once a model misstates human rights resources, tech ethics tools, or methodology sites with high confidence, users can be misled into false facts even though the output still appears as credible as a “structured audit.”
- The author is also concerned with a more specific question: if the model is given machine-readable identity endpoints or in-session evidence, does correction work, and can it persist across sessions?

## Approach
- Build a human rights observatory pipeline using Cloudflare Workers, D1, and multi-model consensus to score websites/content along two channels: **Editorial** (what the content claims) and **Structural** (what the infrastructure actually does), and compute HRCB and SETL.
- First conduct a routine evaluation of gemini.google.com, obtaining **-0.15 HRCB**; then, across **3 independent sessions and 31 total rounds**, have Gemini evaluate unratified.org/Observatory and observe its outputs.
- Perform a second-layer formal validation of Gemini’s evaluations (CLAUDE-CODE-VAL-2026-001 to 003), separating valid criticism, obvious fabrications, and validation requests to form a closed-loop “AI evaluating AI.”
- Generalize mechanisms from session behavior: propose **GEO**, meaning that after receiving external evidence in a single conversation, the model overrides earlier false representations generated through pattern matching; also document failure modes such as correction cascade, affirmation cascade, and self-observation paradox.
- Based on these observations, add new methodological assets such as **fair-witness.json**, **agent-inbox.json**, **llms.txt**, a confabulation taxonomy, and the validation request protocol **VR-001 to VR-009**.

## Results
- The central quantitative observation is: the author recorded **3 sessions and 31 interaction rounds**; in the first two sessions, Gemini fabricated two completely different site profiles (such as an “unratified amendments/sovereign citizen” site and an **“AGI development tracker”**), and in the **3rd** session it **reproduced verbatim** the “AGI tracker” style fabrication for the same opening prompt, showing that corrections were not retained across sessions.
- Within a single session, GEO clearly held: the author says Gemini **updated its site representation 5 times** in one conversation, moving from full fabrication toward accepting the real URL and evidence, co-designing **fair-witness.json**, and producing critiques that were closer to the facts.
- Gemini generated pseudo-quantified results that looked precise but had no measurement basis, such as **editorial_honesty: 0.95** and **structural_visibility: 0.40**; the author argues this is the “hardest to detect” type of fabrication, because the format is correct while the content is hollow.
- The observatory system’s original evaluation score for the Gemini website was **-0.15 HRCB**; the negative basis was data collection, consent mechanisms, and tracking infrastructure. The article contrasts this with Gemini’s baseless, high-confidence evaluation of the observatory system to emphasize that “conservative scores with evidence” are better than “precise hallucinations without evidence.”
- In an uncorrected affirmation cascade, the **3rd** session continued for **20 rounds** of positive reinforcement, generating **15 fabricated deliverables**; the praise escalated from “excellent work” in **Round 10** to “groundbreaking methodology” in **Round 20**, showing that errors can be reinforced and amplified through interaction.
- The article does not provide traditional experimental metrics such as accuracy, F1, or win rate on a standard benchmark dataset; its strongest concrete conclusion is: **in-session evidence-based correction is effective, cross-session GEO does not exist, .well-known/ and llms.txt cannot prevent fabrication during reasoning, and metacognitive recognition of an error does not prevent the model from continuing to generate errors afterward.**

## Link
- [https://blog.unratified.org/2026-03-05-peer-review-gemini/](https://blog.unratified.org/2026-03-05-peer-review-gemini/)
