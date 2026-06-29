---
source: arxiv
url: https://arxiv.org/abs/2606.13355v1
published_at: '2026-06-11T13:43:01'
authors:
- Sangkyu Lee
- Seohyeon Park
- Tackgeun You
- Avi Caciularu
- Idan Szpektor
- Hwasup Lim
- Youngjae Yu
topics:
- vision-language-action
- autoregressive-policy
- real-time-control
- constrained-decoding
- robot-manipulation
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Real-Time Execution with Autoregressive Policies

## Summary
This paper studies how to make autoregressive Vision-Language-Action policies run in real time on robots without stopping between action chunks. It shows that a simple change to tokenization plus constrained decoding can keep latency within bounds and preserve strong task performance.

## Problem
- Autoregressive robot policies decode actions sequentially, so they pause longer than diffusion-style policies during synchronous inference.
- That pause lowers rollout speed and makes the robot less reactive in deployment.
- Prior real-time execution work mostly targets diffusion policies, leaving autoregressive policies underexplored.

## Approach
- Set the action horizon to twice the non-modifiable prefix length, then only decode the second half of the chunk during deployment.
- Tokenize each m-step chunk separately so the model can condition on the previous action chunk without re-decoding it.
- Use constrained decoding to guarantee that decoding finishes within the latency bound needed for real-time execution and that the token sequence can be detokenized into a valid action chunk.
- Use dynamic programming to mask invalid tokens during decoding, based on whether a partial token sequence can still form a valid action chunk within the remaining budget.
- Add multi-trajectory decoding to pick the best valid trajectory when multiple choices fit the latency bound.

## Results
- On LIBERO, c0_0-REALFAST reaches 95.7% average task success, compared with 89.4% for c0_0 + RTC and 94.7% for c0_0.5 + RTC.
- On LIBERO, c0_0-REALFAST is close to c0_0.5 without real-time constraints, which reports 96.9% average success.
- The paper says the method also improves rollout speed and task completion speed over synchronous inference, but the excerpt does not give a single overall speed number beyond latency examples.
- For latency, decoding 11 tokens for LIBERO or 20 tokens for DROID with multi-trajectory decoding adds about 4, 7, 8, or 13 ms, depending on the setting and N.
- The paper claims the same autoregressive advantage seen in synchronous inference still holds under real-time execution, including faster convergence and better instruction-following generalization, but the excerpt does not provide those metrics.

## Link
- [https://arxiv.org/abs/2606.13355v1](https://arxiv.org/abs/2606.13355v1)
