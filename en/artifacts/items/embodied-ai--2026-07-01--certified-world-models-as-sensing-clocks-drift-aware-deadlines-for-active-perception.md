---
source: arxiv
url: https://arxiv.org/abs/2607.01537v1
published_at: '2026-07-01T23:36:49'
authors:
- Hongbo Wang
topics:
- world-models
- active-perception
- certified-prediction
- sensing-scheduling
- equivariant-models
- conformal-calibration
relevance_score: 0.61
run_id: materialize-outputs
language_code: en
---

# Certified World Models as Sensing Clocks: Drift-Aware Deadlines for Active Perception

## Summary
The paper turns a certified world model's validity horizon into a re-sensing deadline for agents that coast on open-loop predictions. Its strongest claim is a drift-aware clock that controls interval certificate violations on a frozen 3D VN-JEPA model, with clear limits on spectral-term benefits.

## Problem
- Agents that use a world model need a rule for when to sense again during open-loop coasting; late sensing can break the prediction certificate, and early sensing wastes sensing budget.
- Fixed sensing periods ignore the model's current reliability, while residual monitors fire after error has already grown.
- The target metric is interval-simultaneous certificate violation: the chance that prediction error exceeds a certified tolerance anywhere inside a coasting interval.

## Approach
- The method treats the certified prediction horizon as a sensing deadline: after sensing resets belief, the agent coasts until the certified clock expires, then senses again.
- A naive spectral deadline uses a Lyapunov-style expansion rate, roughly `T ~ log(epsilon/e0) / lambda`, to estimate how long prediction error stays below tolerance.
- The deployed rule adds a calibrated native rollout-drift envelope: `b_h^UCB + C exp(lambda h) e0 + eta_h <= epsilon_cert`. The deadline is the largest horizon `h` satisfying that bound.
- In the full re-sensing VN-JEPA setting, post-sense error is near zero, so the deployed deadline reduces to a drift-envelope clock with horizons around 2 to 3 steps.
- Calibration fixes the certificate tolerance, drift envelope, and slack on a calibration split, then evaluates once on held-out intervals.

## Results
- On frozen 3D VN-JEPA, three held-out tests met the pre-registered interval-ICV upper-bound target of `<= 0.15`: r2 shard 000 to 001 had `epsilon_cert=1.15`, `T_eq=3`, `U95=0.092`; r1 shard 000 to 001 had `epsilon_cert=1.10`, `T_eq=2`, `U95=0.139`; r2 shard 000 to 002 had `epsilon_cert=0.95`, `T_eq=2`, `U95=0.095`.
- On the synthetic oracle deadline bench, interval-ICV upper bounds were `U95=0.040` and `0.073`, both below the `0.15` target.
- With finite-data spectral audits, validity survived estimation error with `U95 <= 0.073` and budget ratio `<= 1.11`, down to about `n=5` audit samples.
- In the cue-conditioned reactive-contrast bench at matched sensing budget around `0.068`, the certified clock had overall ICV `U95=0.042` and eventful-tail ICV `0.163`; MB-EIG had `0.062` overall and `0.364` in the eventful tail; Uniform had `0.131` overall and `0.715` in the tail.
- MB-EIG needed about `3x` more sensing budget to recover the tail protection; risk-sensitive MB-CVaR (`0.165` tail ICV) and MB-WorstCase (`0.169` tail ICV) tracked the certified clock closely.
- The paper reports limits: on VN-JEPA, a non-spectral empirical conformal horizon matched the deployed clock on validity and budget across all 3 confirmed splits, the lead-time bench returned a null result (`0.955` Eq-spec vs `0.957` Uniform), and the spectral term showed no clean budget-matched advantage in partial-reset exploration.

## Link
- [https://arxiv.org/abs/2607.01537v1](https://arxiv.org/abs/2607.01537v1)
