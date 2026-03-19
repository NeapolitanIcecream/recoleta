---
source: hn
url: https://dicendo.app/
published_at: '2026-03-15T22:52:58'
authors:
- rafaldot
topics:
- password-generation
- offline-security
- physical-randomness
- deterministic-algorithm
- entropy
relevance_score: 0.09
run_id: materialize-outputs
language_code: en
---

# Offline password generator based on physical dice

## Summary
This work proposes **dicendo**: a fully offline, deterministic password generation method based on physical dice that maps dice outcomes to high-entropy passwords using publicly verifiable rules. Its goal is to avoid relying on the system RNG or external data sources, allowing users to generate strong passwords in a controllable and auditable way.

## Problem
- The problem it aims to solve is how to generate high-strength passwords **without trusting the device random number generator, while staying offline, and with no external dependencies**.
- This matters because password security often depends on the quality of randomness; if the RNG, online services, or black-box implementations are not auditable, users cannot easily verify whether passwords are truly random and untampered with.
- It also needs to balance **verifiability and practicality**: ordinary users should be able to obtain sufficiently high entropy using only standard six-sided dice.

## Approach
- The core mechanism is simple: the user first rolls physical dice to obtain physical randomness, then uses a **publicly documented deterministic algorithm** to convert the results into the final password; the randomness comes from the dice, and the algorithm itself does not introduce any additional random source.
- The method uses three types of dice-derived inputs: **numbers / faces, directions, order**, corresponding to the N, D, and O in the name.
- The entire process runs **fully offline**, does not use the system RNG, and does not rely on any external data sources.
- Because the mapping is **fully deterministic**, anyone can verify it: the same dice input necessarily produces the same password, which improves auditability and transparency.

## Results
- The key security quantification given in the text is that if only dice face results are used, at least **30 dice rolls** are typically required, corresponding to about **6^30 ≈ 2 × 10^23** possible outcomes.
- If numbered dice are used and **face values, directions, and order** are all taken into account, then about **12 dice** are enough to achieve similar or higher entropy, with a state space of about **6^12 × 4^12 × 12! ≈ 1.7 × 10^25**.
- The strongest specific claim is that the method can generate "**very strong random passwords**," and that the generation process is **fully user-controlled, publicly documented, and easy to verify**.
- The provided excerpt **does not provide** a standard benchmark dataset, experimental comparisons with other password generators, success rates, or user study metrics, so there is no benchmark-style quantitative evaluation to report.

## Link
- [https://dicendo.app/](https://dicendo.app/)
