---
source: hn
url: https://d-illusion.com/
published_at: '2026-03-07T23:56:48'
authors:
- TimeKeeper
topics:
- mechanism-design
- digital-art
- time-tokenization
- social-referral
- dynamic-pricing
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# D-Illusion

## Summary
D-Illusion proposes an interactive clock system that turns every second of a day into something an individual can "claim," and gamifies the "value of time" through increasing prices, position drift, and an invitation mechanism. It is more like a conceptual mechanism-design / digital art project than a traditional academic research paper.

## Problem
- The problem it attempts to address is: how to transform abstract, non-storable, and non-ownable "time" into an allocable, tradable-perceived, and competitive positional resource.
- This matters because it combines time scarcity, social propagation, and value-growth mechanisms to explore how people assign value to a "share of time."
- From the provided text, the project also frames a core tension: value decays when not shared, and value rises when shared / propagated.

## Approach
- It discretizes a day into **86,400** second-level positions; each participant receives an assigned "next available second," and their name and message appear at that second.
- It uses **incremental pricing**: with each new participant, the price rises by **£0.01**, so joining later costs more.
- It uses a **drift mechanism**: if a participant does nothing, their second gradually moves toward an earlier position over time, representing the loss of time value when it is not shared.
- It uses an **invitation / recruitment mechanism**: when someone joins through you, both your second and theirs move toward a later position, representing time gaining value through sharing.
- The objective function is very simple: get as close as possible to **midnight**; midnight is defined as the most valuable position in the day and cannot be surpassed.

## Results
- The provided text **does not provide standard academic experiments, datasets, baselines, or quantitative performance results**.
- The most specific numerical settings given in the text include: a day contains **86,400 seconds**; the price increases by **£0.01** for each additional user.
- The strongest mechanism-level claim is: later moments are more valuable, and **midnight** is the highest-value position; participants cannot move beyond it.
- Another explicit claim is that the system contains two opposing forces—**drift** makes positions earlier, while **recruitment** makes positions later—thereby creating ongoing competition and incentives for propagation.
- Because experiments and evaluation are absent, its actual effects on user behavior, propagation efficiency, economic stability, or long-term value formation cannot be verified.

## Link
- [https://d-illusion.com/](https://d-illusion.com/)
