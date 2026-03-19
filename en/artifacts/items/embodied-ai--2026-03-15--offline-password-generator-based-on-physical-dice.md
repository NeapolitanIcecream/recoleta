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
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Offline password generator based on physical dice

## Summary
This article introduces dicendo: a fully offline method for generating strong passwords, where entropy comes from physical dice and is then processed through public, deterministic algorithms. Its value lies in decoupling password generation from the system RNG and external data sources, allowing users to control and verify the source of randomness themselves.

## Problem
- The core problem is: how to generate sufficiently high-entropy, verifiable strong passwords **without relying on device RNG, the network, or external data sources**.
- This matters because some users want to reduce their trust dependence on software implementations, operating-system randomness sources, or online services, and instead base security on observable physical randomness.
- It also addresses the issue of **auditability**: the mapping from input to output should be public, deterministic, and reproducible, so it can be independently verified.

## Approach
- The core mechanism is simple: first roll standard six-sided dice to obtain physically random input, then use a **publicly documented deterministic algorithm** to map those inputs into the final password; the randomness comes only from the dice, and the algorithm itself introduces no additional random source.
- The method uses three categories of dice-derived input components: **N – numbers (face values)**, **D – directions**, and **O – order**; the name dicendo is also derived from these three parts.
- The entire process runs fully offline, does not call the system random number generator (RNG) to generate passwords, and does not depend on any external data.
- The article gives two typical entropy-source configurations: when using only dice face values, about 30 rolls are typically required; if numbered dice are used and face values, directions, and order are all incorporated, a comparable or even larger state space can be achieved with fewer dice.

## Results
- The article does not provide experimental results on standard academic benchmarks, comparison tables, or quantitative evaluations such as error rates or success rates.
- Its main quantitative security claim is: when generating high-quality passwords using only dice face values, at least **30** rolls are typically required, corresponding to about **6^30 ≈ 2 × 10^23** possible outcomes.
- Another quantitative claim is: if numbered dice are used and **face values, directions, and order** are all counted, then about **12** dice are sufficient to achieve comparable or higher entropy, corresponding to about **6^12 × 4^12 × 12! ≈ 1.7 × 10^25** possible states.
- The strongest practical claim is that the scheme is **fully offline**, **does not use the system RNG**, **derives entropy entirely from physical dice rolls**, and that the mapping from input to password is **fully deterministic and publicly verifiable**.

## Link
- [https://dicendo.app/](https://dicendo.app/)
