---
source: arxiv
url: http://arxiv.org/abs/2603.02491v1
published_at: '2026-03-03T00:47:58'
authors:
- Aran Nayebi
topics:
- agent-theory
- decision-making-under-uncertainty
- pomdp
- world-models
- predictive-state-representations
relevance_score: 0.68
run_id: materialize-outputs
language_code: en
---

# What Capable Agents Must Know: Selection Theorems for Robust Decision-Making under Uncertainty

## Summary
This paper proves that if an agent has low average regret on a class of structured prediction/decision tasks in uncertain environments, then it **must** internally represent some kind of predictive state, rather than merely being something that *could* be implemented with a world model. The core contribution is to turn prediction problems into binary “betting” decisions, and then derive necessity results for world models, belief states, and memory structure from regret bounds.

## Problem
- The paper asks: **What must a highly capable agent internally know in order to consistently make good decisions under uncertainty?**
- Classical control/POMDP results only show that belief states or world models are **sufficient** for optimal control, but not whether such representations are **necessary**; this matters for understanding, auditing, and training agents.
- The authors aim to provide “selection theorems” under weaker, more realistic conditions: requiring only **low average-case regret**, while allowing **stochastic policies**, **partial observability**, and **no explicit model**.

## Approach
- The core mechanism is simple: rewrite “whether the future is predicted correctly” as a binary **betting task**. The agent bets left/right first, then the future is revealed; if average regret is low, it cannot frequently bet wrong on high-confidence tests.
- The authors prove a key decomposition: in binary betting, **normalized regret** directly controls the probability mass assigned to incorrect actions; when the test has sufficient **margin** (far enough from 50/50), low regret forces the agent to distinguish cases that differ predictively.
- In **fully observed** environments, the authors construct a family of composite objectives over transition events \b(s,a,s')\b, and define a soft estimator \(\hat P_{ss'}(a)\) from the policy’s selection probabilities on these objectives, thereby approximately recovering the transition kernel.
- In **partially observed** environments, the authors shift to the PSR/predictive-state perspective: if histories are distinguishable under a distribution over future tests, and the agent still wants to maintain low average regret, then its internal memory must preserve those distinctions in a belief-state / predictive-state-like way, yielding a “no-aliasing”-type necessity result.
- The paper also discusses additional constraints induced by structured task distributions: for example, block-structured tests select for modular information structure, and regime mixtures select for internal states sensitive to different mechanisms/scenarios.

## Results
- **Main theorem for fully observed settings**: if the average normalized regret on a diagnostic objective family satisfies \(\mathbb{E}[\delta]\le \bar\delta\) (Eq. 8), then the transition estimation error satisfies
  \[
  \mathbb{E}_{(s,a,s')}\big[|\hat P_{ss'}(a)-P_{ss'}(a)|\big]
  \le 2t_\gamma\,\mathbb{E}\Big[\sqrt{P_{ss'}(a)(1-P_{ss'}(a))/n}\Big] + \bar\delta/c(\gamma) + O(1/n)
  \]
  where \(c(\gamma)=4\gamma/(1+2\gamma)\) and \(t_\gamma=\sqrt{(1+2\gamma)/(1-2\gamma)}\) (Eq. 10). More coarsely, the error is \(\le t_\gamma/\sqrt n + \bar\delta/c(\gamma)+O(1/n)\). This shows that as test depth \(n\) increases, low regret drives the estimate toward the true transition model.
- **Quantitative bound on wrong-bet probability**: on tests with margin at least \(\gamma\), the mass on incorrect actions satisfies \(w\le \delta/c(\gamma)\) (Eq. 7). Intuitively, the lower the regret and the more “non-50/50” the test, the less the agent can bluff randomly; it must make the correct predictive distinctions.
- **Causal-level conclusion**: if the environment approximately satisfies the causal Markov process assumption, then what is recovered is the **Pearl Level 2 interventional kernel**, whose average error is larger than the above bound by only an added \(\varepsilon_{\mathrm{cMP}}\) term (Eq. 12); the paper explicitly claims that this information generally **cannot** recover **Level 3 counterfactuals**.
- **Theoretical advance in partially observed settings**: the authors claim a quantitative necessity result for belief-like memory / predictive state, addressing an open question in prior world-model recovery work; however, the provided excerpt does not include the final form with complete theorem numbering and exact numerical constants.
- **Advance over prior work**: the results do not require optimality, deterministic policies, or worst-case guarantees, but instead cover **stochastic policies + average regret + POMDPs**. This is more general than prior world-model recovery settings that relied on stronger competence assumptions.
- **Quantitative experiments / empirical results**: the excerpt contains **no experimental data or benchmark numerical results**; the main contributions are mathematical theorems, error bounds, and theoretical claims about what is and is not recoverable.

## Link
- [http://arxiv.org/abs/2603.02491v1](http://arxiv.org/abs/2603.02491v1)
