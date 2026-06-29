---
source: arxiv
url: https://arxiv.org/abs/2605.26820v1
published_at: '2026-05-26T10:39:02'
authors:
- Jiarun Zhu
- Yijun Hong
- Xiaoquan Sun
- Zetian Xu
- Mingqi Yuan
- Zhiyong Wang
- Wenjun Zeng
- Jiayu Chen
topics:
- vision-language-action
- continual-learning
- catastrophic-forgetting
- experience-replay
- real-world-robotics
- manipulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Can VLA Models Learn from Real-World Data Continually without Forgetting?

## Summary
This paper tests whether VLA robot policies can keep old manipulation skills while learning new real-world tasks. It finds severe forgetting under plain sequential fine-tuning, then shows that experience replay works when replay rate and action normalization are set carefully.

## Problem
- Real robots receive new task data over time, but retraining on all past data can be expensive.
- VLA policies can lose earlier skills when fine-tuned on later tasks, which limits long-running robot deployment.
- Prior continual VLA studies used narrow simulation setups, so they may miss failures caused by real objects, cameras, action distributions, and task shifts.

## Approach
- The authors collect a real-world continual learning dataset with 4 sequential manipulation tasks and 500 trajectories per task: Stack Bowl, Hang Cup, Press Button, and Fold Towel.
- They fine-tune a \(\pi_{0.5}\) VLA policy for 4,000 steps per task and evaluate all seen tasks after each stage.
- They measure average score, negative backward transfer (NBT), and forward transfer (FT), using normalized 0-100 task scores.
- They test experience replay with buffer ratios \(B \in \{0.002, 0.02, 0.2\}\) and replay frequencies \(f_r \in \{0.05, 0.1, 0.2, 0.5\}\).
- They compare two action normalization choices: fixed first-task statistics and per-task statistics.

## Results
- Plain sequential fine-tuning drops Stack Bowl from 100.0 to 15.0, Hang Cup from 97.5 to 25.0, and Press Button from 100.0 to 13.3. Final average score is 37.3, with NBT +80.0 and FT -50.0.
- Default replay with \(B=0.2\) and \(f_r=0.2\) reaches 96.3 on Stack Bowl, 97.5 on Hang Cup, 90.0 on Press Button, and 90.0 on Fold Towel. Average score is 93.5, NBT is +5.0, and FT is +11.8.
- Default replay beats joint training on average score: 93.5 versus 70.3. Joint training falls to 13.3 on Press Button, while default replay gets 90.0.
- Smaller replay buffers reduce retention on some tasks: with \(B=0.002\), Hang Cup is 60.0 and average score is 85.5; with \(B=0.02\), average score is 86.3.
- Replay frequency changes the stability and learning tradeoff: \(f_r=0.05\) gives average 85.3, \(f_r=0.1\) gives 83.3, \(f_r=0.2\) gives 93.5, and \(f_r=0.5\) gives 88.0.
- Fixed action normalization gives average 93.5, while per-task normalization collapses to 23.7 average with 0.0 on Hang Cup, Press Button, and Fold Towel. Reusing Stack Bowl statistics at test time raises that setting to 58.0 average, suggesting the learned actions were mis-scaled rather than fully missing task semantics.

## Link
- [https://arxiv.org/abs/2605.26820v1](https://arxiv.org/abs/2605.26820v1)
