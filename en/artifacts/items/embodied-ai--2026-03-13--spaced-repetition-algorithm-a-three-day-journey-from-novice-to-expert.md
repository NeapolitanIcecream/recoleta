---
source: hn
url: https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert
published_at: '2026-03-13T23:53:52'
authors:
- primenumber1
topics:
- spaced-repetition
- memory-modeling
- learning-schedule
- forgetting-curve
- educational-technology
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Spaced Repetition Algorithm: A Three‐Day Journey from Novice to Expert

## Summary
This article systematically reviews the development trajectory of spaced repetition algorithms, from empirical rules to memory theory and data-driven modeling. Its core goal is to automatically schedule review times so that memory can be retained with lower review cost. It is more like a tutorial/review and research guide than a single paper presenting new experimental results.

## Problem
- The problem to solve is: **how to estimate how much a person has already forgotten, how quickly they are forgetting, and based on that arrange the “optimal review interval”** to reduce forgetting while avoiding excessive review.
- This matters because manually tracking large numbers of knowledge items is nearly impossible; each memory has a different forgetting curve and difficulty, and poor scheduling leads either to inefficient learning or rapid forgetting.
- The article also emphasizes that there is a tension between review frequency and forgetting rate: reviewing too little leads to forgetting, but reviewing too often is not necessarily efficient either.

## Approach
- It begins with the earliest **empirical algorithms**: SM-0 used manual experiments to find approximately optimal intervals; SM-2 introduced per-card scheduling and the Ease Factor; SM-4 used the Optimal Interval Matrix so that new cards could benefit from data from similar old cards.
- It proposes a more general **three-state memory model DSR**: Difficulty, Stability, and Retrievability, representing memory as “how difficult it is, how long it can last, and the current probability of recalling it.”
- It uses the **forgetting curve**, approximated as a negative exponential function, to show that stability changes after review; improvements in stability are jointly influenced by current stability, recall probability, and material difficulty.
- Through **memory event data** (who, when, what was reviewed, correct/incorrect response, time spent, historical sequence, etc.), it estimates DSR states, and then uses those states to simulate long-term learning under different scheduling strategies.
- It further builds an **SRS simulator** to compare the long-term efficiency of different schedulers under “total duration constraints + daily study time constraints + a finite card set.”

## Results
- The article cites external research showing that spaced repetition outperforms massed practice: in Rea & Modigliani 1985, the distributed practice group achieved **70%** accuracy on the immediate test, compared with **53%** for the massed practice group.
- It cites the meta-analysis by Donovan & Radosevich 1999: mean weighted effect size **0.46**, 95% CI **[0.42, 0.50]**; the author interprets this as roughly **62%–64%** of spaced repetition users outperforming massed practice users.
- In Wozniak’s early experiments, candidate intervals for the second review of **2/4/6/8/10 days** corresponded to forgetting rates of **0%/0%/0%/1%/17%**, leading to the choice of **7 days**; later, empirical intervals of about **16 days** for the third review and **35 days** for the fourth were obtained.
- The fixed sequence of SM-0 is summarized as **1, 7, 16, 35 days**, after which it grows roughly by **2×** the previous interval, reflecting the empirical pattern that “the more stably something is remembered, the longer the interval.”
- The article presents an important theoretical conclusion: **expected stability gain** is maximized when retention is around **30%–40%**, but the author also clearly points out that this does **not** mean the overall learning rate is optimal.
- It does not provide unified new SOTA numbers from this tutorial/excerpt itself on a standard benchmark dataset; the stronger concrete claim is that the DSR model and subsequent simulation framework can convert event logs into memory states and use them to optimize scheduling.

## Link
- [https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert](https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert)
