---
source: arxiv
url: http://arxiv.org/abs/2603.02491v1
published_at: '2026-03-03T00:47:58'
authors:
- Aran Nayebi
topics:
- decision-theory
- pomdp
- world-models
- regret-analysis
- predictive-state-representations
relevance_score: 0.34
run_id: materialize-outputs
language_code: en
---

# What Capable Agents Must Know: Selection Theorems for Robust Decision-Making under Uncertainty

## Summary
This paper proves that if an agent achieves sufficiently low average regret on a class of prediction/decision tasks with uncertainty, then it **must** internally implement some kind of predictive structured state, rather than merely being something that *can* be implemented using a world model. The core contribution is advancing this necessity claim from the classical notion of “constructibility” to a “representation constraint selected by the task.”

## Problem
- Classical POMDP / control theory shows that optimal control **can** be implemented using a belief state or world model, but does not explain under what conditions these representations are **necessary**.
- If we look only at external performance, an architecture might perform well on a number of tasks without actually learning a predictive internal state; this leaves open the question of whether capability itself forces world modeling.
- This question matters because it concerns whether the internal representations of highly capable agents are constrained by the demands of robust decision-making, especially under stochastic policies, partial observability, and evaluation over task distributions.

## Approach
- The authors propose **selection theorems**: on a family of structured, action-conditioned prediction tasks, if an agent’s **average normalized regret** is low, then its internal memory/state must distinguish the key situations needed to support prediction.
- The technical core is to reduce prediction problems to binary **betting** decisions: the agent first bets between two mutually exclusive branches, and then subsequent trajectories reveal which side was correct.
- They prove a regret decomposition: when the tests have sufficiently large margin, low regret directly limits the probability mass the agent places on incorrect bets; therefore, the agent cannot collapse predictively distinct situations into the same internal state.
- In **fully observed** environments, this argument yields approximate recovery of the interventional transition kernel; in **partially observed** environments, it implies the necessity of belief-like memory / predictive state, and yields no-aliasing-type conclusions.
- The paper also discusses additional selection effects from structured task distributions, for example block-structured tests leading to information modularity, and regime mixtures leading to internal states that are sensitive to changes in environmental mechanisms.

## Results
- **Main theorem for fully observed settings (Theorem 1)**: if the average regret over a family of diagnostic targets satisfies
  \(\mathbb{E}[\delta] \le \bar{\delta}\), then the transition estimator \(\widehat P\) constructed from the policy satisfies the average absolute error bound:
  \(\mathbb{E}[|\widehat P_{ss'}(a)-P_{ss'}(a)|] \le 2 t_\gamma \mathbb{E}[\sqrt{P_{ss'}(a)(1-P_{ss'}(a))/n}] + \bar\delta / c(\gamma) + O(1/n)\).
- The paper also gives a coarser but more direct numerical form:
  \(\mathbb{E}[|\widehat P_{ss'}(a)-P_{ss'}(a)|] \le t_\gamma / \sqrt n + \bar\delta / c(\gamma) + O(1/n)\). This shows that the error shrinks as **1/\sqrt n** with increasing test depth **n**, and worsens linearly with average regret **\bar\delta**.
- **Control of incorrect-bet mass (Lemma 1)**: in the betting setting, normalized regret and the probability mass \(w\) on incorrect actions satisfy \(\delta = w \cdot 4m/(1+2m)\); when the margin \(m \ge \gamma\), \(w \le \delta / c(\gamma)\). This is the key quantitative bridge behind the claim that “low regret forces internal predictive distinctions.”
- **Causal-level result (Corollary 1)**: if the environment approximately satisfies a causal Markov process and \(|P - P^{do}| \le \varepsilon_{\mathrm{cMP}}\), then
  \(\mathbb{E}[|\widehat P_{ss'}(a)-P^{do}_{ss'}(a)|]\) obeys the same error bound as above, with only an additional **\(\varepsilon_{\mathrm{cMP}}\)** term; that is, low average regret is sufficient to select an approximate representation of **Pearl Level 2 interventions**.
- **Negative result (Corollary 2)**: even if the interventional kernel is recovered exactly, one still **cannot generally recover Level 3 counterfactuals**; the authors provide two structural causal models with the same interventional kernel but different counterfactual couplings as a counterexample.
- The paper includes no experimental datasets, benchmark scores, or empirical SOTA comparisons; its main “breakthrough result” is instead a **new theoretical necessity result**, covering settings involving **stochastic policies, average-case regret, and partial observability**, where prior results were weaker or absent.

## Link
- [http://arxiv.org/abs/2603.02491v1](http://arxiv.org/abs/2603.02491v1)
