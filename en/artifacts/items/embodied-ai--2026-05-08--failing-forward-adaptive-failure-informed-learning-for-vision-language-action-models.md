---
source: arxiv
url: https://arxiv.org/abs/2605.08434v2
published_at: '2026-05-08T19:57:11'
authors:
- Meng Zheng
- Samhita Marri
- Anwesa Choudhuri
- Benjamin Planche
- Zhongpai Gao
- Van Nguyen Nguyen
- Terrence Chen
- Girish Chowdhary
- Ziyan Wu
topics:
- vision-language-action
- robot-policy-learning
- failure-informed-learning
- diffusion-policy
- flow-matching
- robot-manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Failing Forward: Adaptive Failure-Informed Learning for Vision-Language-Action Models

## Summary
AFIL is a failure-aware training and sampling method for diffusion- and flow-based vision-language-action robot policies. It uses failed rollouts as negative guidance so the policy avoids action regions linked to bad outcomes.

## Problem
- Success-only behavior cloning leaves VLA policies with no training signal for recovery after small execution errors.
- Hand-designed failure categories and human correction do not scale well to new manipulation tasks or robot embodiments.
- The problem matters because deployment errors can push a robot into states outside its demonstration data, causing long-horizon tasks to fail.

## Approach
- A pretrained VLA generates failed rollouts online, so the method collects failure data from the policy's own behavior instead of manually defined failure modes.
- The model uses 2 action generators: one trained on successful trajectories and one trained on failed trajectories.
- Both action generators share 1 vision-language backbone, which limits extra parameter cost compared with training separate full VLA models.
- During diffusion or flow sampling, the failure generator pushes actions away from failure-prone directions while the success generator pulls actions toward successful behavior.
- The guidance weight is adaptive: it uses cosine distance between success and failure predictions, with scale α(1 - cos), so guidance is weaker when both predictions agree and stronger when they diverge.

## Results
- The provided excerpt reports experiments on in-domain and out-of-domain manipulation tasks, including short-horizon and long-horizon settings, but it does not provide task success percentages, dataset sizes, or table values.
- The main claimed result is higher task success rate than existing VLA baselines across the tested manipulation tasks.
- The paper claims better recovery from failure states by using online generated failure trajectories as training data and negative sampling guidance.
- The method applies to 2 VLA generator types named in the excerpt: diffusion-based policies and flow-based policies.
- The concrete architectural claim is that AFIL adds 1 failure action generator while sharing the VLM backbone with the success generator.

## Link
- [https://arxiv.org/abs/2605.08434v2](https://arxiv.org/abs/2605.08434v2)
