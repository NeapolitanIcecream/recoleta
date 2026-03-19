---
source: hn
url: https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert
published_at: '2026-03-13T23:53:52'
authors:
- primenumber1
topics:
- spaced-repetition
- memory-modeling
- learning-optimization
- review-scheduling
- educational-ai
relevance_score: 0.13
run_id: materialize-outputs
language_code: en
---

# Spaced Repetition Algorithm: A Three‐Day Journey from Novice to Expert

## Summary
This article systematically explains how spaced repetition algorithms evolved from empirical rules to data-driven methods based on modeling memory states, with the goal of automatically scheduling review times to improve long-term memory efficiency. It is more like a research tutorial/review than a single experimental paper, but it clearly presents the core ideas behind SM-0, SM-2, SM-4, and the DSR memory model.

## Problem
- The problem it addresses is: **how to automatically estimate a person’s forgetting state and arrange the optimal review interval for each learning item** so as to forget as little as possible within limited time.
- This is important because manually tracking the forgetting curve of a large number of knowledge items is nearly impossible, and poor review scheduling can lead to **either too much forgetting or an excessive review burden**.
- The article also emphasizes that different materials have different difficulty levels, and different memories have different stability, so a single fixed interval cannot effectively adapt to real learning processes.

## Approach
- It begins with the earliest **empirical algorithms**: SM-0 searched experimentally for review intervals that were “as long as possible while keeping forgetting under control,” producing an approximately doubling interval sequence such as 1, 7, 16, and 35 days.
- SM-2 further breaks material into **independent cards** and introduces the **Ease Factor**, dynamically adjusting the next interval according to the quality of each recall; put simply, “if recall is easy, lengthen the interval; if forgotten, reset or shorten it.”
- SM-4 then introduces the **Optimal Interval Matrix**, no longer looking only at individual cards, but allowing cards with “similar difficulty and similar numbers of reviews” to share statistical information and update optimal intervals from group experience.
- At the theoretical level, the article proposes/emphasizes the **DSR three-component memory model**: Difficulty, Stability, Retrievability. The core mechanism is to describe memory state using “the current probability of recall + the speed of memory decay + the difficulty of the material,” and to use these states to predict review outcomes.
- Based on the above model, user memory event logs can be converted into memory states, and then a simulator can compare the learning efficiency of different schedulers under constraints such as “total duration, daily study time, and item set.”

## Results
- The article cites external research showing that spaced repetition outperforms massed practice: in Rea & Modigliani 1985, the **distributed practice group achieved 70% accuracy, versus 53% for the massed practice group**.
- It cites the Donovan & Radosevich 1999 meta-analysis: an overall weighted effect size of **0.46**, with a 95% confidence interval of **[0.42, 0.50]**, indicating that spaced practice significantly outperforms massed practice; the article explains this as roughly **62%–64%** of users outperforming massed-practice learners.
- In Wozniak’s early experiments, the forgetting rates at the second review test for different intervals were: **2/4/6/8/10 days corresponding to 0%/0%/0%/1%/17%**, from which about **7 days** was selected as a better interval.
- In the third-review experiment, **6/8/11/13/16 days corresponded to forgetting rates of 3%/0%/0%/0%/1%**, leading to the choice of **16 days**; in the fourth review, **20/24/28/33/38 days corresponded to 0%/3%/5%/3%/0%**, leading to a choice of about **35 days**.
- Based on these experiments, SM-0 formed the sequence: **I(1)=1 day, I(2)=7 days, I(3)=16 days, I(4)=35 days, followed by approximate doubling**; the author states that its simulations show: **the total amount of knowledge increases over the long term, while the long-term learning rate remains relatively stable**.
- The theoretical analysis also gives a strong conclusion: **expected stability gain reaches its maximum when retention is around 30%–40%**. However, the article also explicitly states that this is not equivalent to optimal overall learning speed; truly optimal scheduling depends on later, more formal optimization algorithms, and this excerpt does not provide a final SOTA quantitative comparison on a unified benchmark.

## Link
- [https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert](https://github.com/open-spaced-repetition/fsrs4anki/wiki/Spaced-Repetition-Algorithm:-A-Three%E2%80%90Day-Journey-from-Novice-to-Expert)
