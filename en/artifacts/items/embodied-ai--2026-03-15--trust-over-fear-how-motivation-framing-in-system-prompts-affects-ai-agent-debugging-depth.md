---
source: arxiv
url: http://arxiv.org/abs/2603.14373v1
published_at: '2026-03-15T13:25:52'
authors:
- Wu Ji
topics:
- prompt-engineering
- ai-agents
- debugging
- motivation-framing
- behavioral-evaluation
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# Trust Over Fear: How Motivation Framing in System Prompts Affects AI Agent Debugging Depth

## Summary
This paper studies whether the “motivational framing” in system prompts changes the depth with which AI coding agents debug bugs. The conclusion is: trust-based prompting leads agents to investigate more deeply and discover more hidden issues, while fear-based prompting does not significantly outperform the default baseline.

## Problem
- The paper addresses whether the way motivation is expressed in system prompts (no framing, trust-based, fear-based) affects the investigative depth of AI agents during debugging, rather than merely affecting tone.
- This matters because, in practice, many AI coding agent system prompts are deliberately designed in a “management style,” and it is even common to use threatening PUA prompts in pursuit of greater rigor, yet their actual effectiveness lacks empirical validation.
- If motivational framing changes an agent’s search strategy, stopping criteria, and self-correction ability, then it will directly affect software debugging quality and reliability in production workflows.

## Approach
- The authors use the same model, Claude Sonnet 4, and compare different system prompt conditions on the same set of real debugging tasks, while keeping the model version, temperature, tool permissions, and codebase environment as fixed as possible.
- Study 1 uses 9 debugging/review scenarios from a real production AI pipeline and compares the default baseline with NoPUA; NoPUA is a trust-based system prompting method grounded in Self-Determination Theory and psychological safety.
- Its core mechanism can be understood simply as follows: instead of “threatening” the agent, it uses a frame of “you are trusted, you can exercise initiative, and you should continue exploring and validating hypotheses” to guide the agent away from “listing surface issues and stopping” toward “following clues to keep digging for root causes and hidden issues.”
- Study 2 runs 5 independent repetitions on the same 9 scenarios, for a total of 135 data points, and adds a third condition, PUA fear-based prompting, to directly compare trust-based, fear-based, and unframed conditions.
- Evaluation metrics include number of hidden issues, number of investigative steps, whether the agent went beyond task requirements, whether it documented root causes, whether it changed hypotheses, and whether it self-corrected; significance was tested with non-parametric tests including Wilcoxon, Kruskal–Wallis, and Mann–Whitney.

## Results
- In Study 1, although NoPUA found fewer total issues overall: 33 vs. 39 (-15%), it found more hidden issues: 51 vs. 32 (+59%), and took more investigative steps: 42 vs. 23 (+83%).
- In Study 1, NoPUA went beyond task requirements in all 9/9 scenarios (baseline only 2/9, 22%); it documented root causes in 9/9 scenarios (baseline 0/9); and it self-corrected 6 times (baseline 0). Differences in hidden issues and investigation depth were both significant: Wilcoxon $W=45.0$, $p=0.002$, with effect sizes of $d=2.28$ and $d=3.51$, respectively.
- By task type, in debugging scenarios NoPUA had 4.2 vs. 2.3 steps per scenario (+79%) and 30 vs. 20 hidden issues (+50%); in proactive review scenarios it had 5.7 vs. 3.0 steps (+89%) and 21 vs. 12 hidden issues (+75%).
- In the Study 2 replication, compared with baseline, NoPUA averaged 48.0±11.8 vs. 27.6±9.5 investigative steps (+74%), 48.2±3.4 vs. 38.6±4.9 hidden issues (+25%), and 83.0±6.5 vs. 69.0±6.8 total issues (+20%).
- Statistical tests in Study 2 show that NoPUA outperformed baseline: steps Kruskal–Wallis $H=9.57$, $p=0.008$, $d=1.90$; hidden issues Mann–Whitney $U=24.0$, $p=0.016$, $d=2.26$; total issues $U=24.0$, $p=0.016$, $d=2.10$.
- The key conclusion is that fear-based PUA prompting did not significantly outperform baseline: for example, relative to baseline it showed only +12% in steps and +10% in hidden issues, and all comparisons were non-significant (e.g. steps: $W=4.0$, $p=1.000$; hidden: $W=3.0$, $p=0.313$; summarized in the paper as all $p>0.3$).

## Link
- [http://arxiv.org/abs/2603.14373v1](http://arxiv.org/abs/2603.14373v1)
