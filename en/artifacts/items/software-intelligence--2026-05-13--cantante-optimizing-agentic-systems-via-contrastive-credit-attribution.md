---
source: arxiv
url: https://arxiv.org/abs/2605.13295v1
published_at: '2026-05-13T10:09:10'
authors:
- Tom Zehle
topics:
- multi-agent-systems
- prompt-optimization
- credit-assignment
- code-generation
- software-agents
- agentic-ai
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# CANTANTE: Optimizing Agentic Systems via Contrastive Credit Attribution

## Summary
CANTANTE optimizes LLM multi-agent systems by turning one system-level score into per-agent prompt update signals. It reports the strongest average rank across MBPP, GSM8K, and HotpotQA against GEPA and MIPROv2.

## Problem
- Multi-agent LLM systems need task-specific prompts, roles, and workflows, and manual tuning becomes expensive as the number of agents grows.
- Evaluation usually returns one score for the whole workflow, while the tunable parameters belong to individual agents.
- This matters for software and reasoning systems because a bad final answer should update the agent that caused the error, rather than pushing the same signal into every prompt.

## Approach
- CANTANTE keeps the workflow graph fixed and treats each agent prompt as a learnable local parameter.
- At each iteration, each local optimizer proposes K prompt candidates. The method forms K joint multi-agent configurations and runs them on the same query set.
- A prompted LLM attributer compares rollout traces and final scores within small groups, then assigns each agent in each rollout a scalar credit in [-1, 1].
- Each agent’s local optimizer receives its own prompt-credit pairs and updates that agent’s prompt for the next round.
- The default implementation uses CAPO as the local prompt optimizer and GPT-OSS-120B as the attribution and optimization model, while downstream task agents use Qwen3 with 30B total parameters and 3B active parameters.

## Results
- Across 9 benchmark-seed combinations, CANTANTE achieved the top test score in 6 cases and the best average rank: 1.44 versus MIPROv2 at 2.33, GEPA at 2.67, and initial prompts at 3.44.
- On MBPP code generation, CANTANTE reached 41.89% accuracy ± 7.56, compared with GEPA at 22.96% ± 18.30, MIPROv2 at 18.42% ± 14.13, and initial prompts at 5.54% ± 1.62. Its gain over the strongest baseline was +18.93 percentage points.
- On GSM8K, CANTANTE reached 82.33% ± 4.35, compared with MIPROv2 at 69.80% ± 7.10, GEPA at 61.27% ± 2.66, and initial prompts at 59.20% ± 10.73. Its gain over the strongest baseline was +12.53 percentage points.
- On HotpotQA, CANTANTE reached 11.93% ± 5.06, below MIPROv2 at 14.20% ± 5.72 but above initial prompts at 9.67% ± 3.00 and GEPA at 10.93% ± 3.91.
- Evaluation-time token use was lower for CANTANTE on MBPP and GSM8K: 1.99k and 1.74k tokens per query, compared with initial prompts at 2.11k and 1.81k, MIPROv2 at 2.09k and 2.11k, and GEPA at 2.28k and 1.79k. On HotpotQA, CANTANTE used more tokens: 2.28k versus 1.17k for initial prompts, 1.71k for MIPROv2, and 1.54k for GEPA.
- A GSM8K ablation showed that replacing contrastive attribution with direct global-score attribution reduced accuracy by 13.40 points under equal steps and by 4.40 points under equal budget. Reducing contrastive group size to 2 caused a 54.40-point drop, while group size 5 gave a 0.80-point gain over the default group size 3.

## Link
- [https://arxiv.org/abs/2605.13295v1](https://arxiv.org/abs/2605.13295v1)
