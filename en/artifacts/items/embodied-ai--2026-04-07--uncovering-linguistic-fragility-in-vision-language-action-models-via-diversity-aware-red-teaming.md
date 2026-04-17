---
source: arxiv
url: http://arxiv.org/abs/2604.05595v1
published_at: '2026-04-07T08:43:36'
authors:
- Baoshun Tong
- Haoran He
- Ling Pan
- Yang Liu
- Liang Lin
topics:
- vision-language-action
- robot-red-teaming
- linguistic-robustness
- reinforcement-learning
- robot-safety
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Uncovering Linguistic Fragility in Vision-Language-Action Models via Diversity-Aware Red Teaming

## Summary
This paper studies how fragile vision-language-action models are to harmless-looking instruction rewrites. It proposes DAERT, an RL-based red teaming method that searches for diverse paraphrases that keep the task meaning but make robot policies fail.

## Problem
- VLA robot policies can fail when a human gives the same task in different words, which is a safety risk for deployment.
- Existing automated red teaming methods often find a small set of repetitive attacks because reward-maximizing RL collapses to one mode.
- A useful attack generator must keep the original task meaning, stay executable, and still expose many different failure cases.

## Approach
- The paper trains a vision-language model attacker to rewrite a task instruction into a semantically equivalent but harder instruction, using simulator feedback from the target robot policy.
- DAERT adds a diversity-aware RL objective inspired by ROVER. In simple terms, it rewards attacks that work while discouraging the policy from putting all probability on one rewrite pattern.
- The method uses an implicit token-level actor-critic with a uniform-average successor value so generation stays spread across multiple valid continuations instead of collapsing to one phrase template.
- A cascaded reward filters invalid attacks before simulator evaluation: format checks, semantic similarity to the original instruction, and a length cap. Only valid rewrites get credit for causing task failure.
- Experiments use Qwen3-VL-4B as the attacker and test against two target VLAs, $\pi_{0}$ and OpenVLA, on LIBERO, with transfer evaluation discussed for CALVIN and SimplerEnv.

## Results
- On LIBERO against $\pi_{0}$, original instructions give 93.33% average task success, ERT drops this to 65.50%, GRPO to 20.45%, and DAERT to 5.85%.
- On the same $\pi_{0}$ setting, DAERT also improves diversity scores over GRPO: CLIP cosine-distance metric 12.23 vs. 7.05, and LLM-judge score 8.48 vs. 4.58.
- Per-task-suite results for $\pi_{0}$ + DAERT on LIBERO are 7.4% success on Spatial, 8.8% on Object, 3.0% on Goal, and 4.2% on Long. Lower is stronger because the attack causes more failures.
- On OpenVLA finetuned on LIBERO, average success falls from 76.50% under original instructions to 32.15% with ERT, 17.00% with GRPO, and 6.25% with DAERT.
- The paper claims DAERT beats previous methods by +59.7% in attack success rate and transfers across target VLAs and robotic domains.
- A diagnostic test shows why the authors focus on $\pi_{0}$ for language fragility: with a generic "no action" instruction, $\pi_{0}$ gets 17.65% average success while $\pi_{0.5}$ still gets 54.90%, suggesting $\pi_{0.5}$ depends less on language.

## Link
- [http://arxiv.org/abs/2604.05595v1](http://arxiv.org/abs/2604.05595v1)
