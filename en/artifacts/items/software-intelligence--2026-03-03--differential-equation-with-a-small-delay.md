---
source: hn
url: https://www.johndcook.com/blog/2026/03/02/small-delay/
published_at: '2026-03-03T23:27:34'
authors:
- ibobev
topics:
- delay-differential-equations
- dynamical-systems
- stability-analysis
- small-delay
- mathematical-modeling
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# Differential Equation with a Small Delay

## Summary
This article discusses a class of first-order delay differential equations with a small delay, and explains that when the delay is sufficiently small, its long-term qualitative behavior is the same as in the no-delay case. The core value is turning the intuition that “a very small delay will not change the essential behavior of the system” into inequality conditions that can be checked.

## Problem
- The research question is: for the equation $x'(t)=a x(t)+b x(t-\tau)$, over what range can the delay term $\tau$ vary without changing the qualitative behavior of the system.
- This matters because delays are common in real systems such as control and pharmaceutical modeling, and a delay can turn monotone decay into oscillation or other completely different dynamics.
- Unlike ordinary differential equations, the solution of a delay differential equation depends not only on a single initial value, but also on the entire initial history function over the interval $[-\tau,0]$, making the analysis more complex.

## Approach
- The article cites and explains a known theorem: for $x'(t)=a x(t)+b x(t-\tau)$, if the delay is sufficiently small, then its qualitative behavior matches that of the system with the delay removed (that is, setting $\tau=0$).
- “Sufficiently small” is made concrete by two conditions: $-1/e < b\tau \exp(-a\tau) < e$, and $a\tau < 1$.
- A technical condition on the initial history function is also required; the article explains that this condition fails only on a nowhere dense set of initial values, so it can usually be treated as holding in generic cases.
- The author uses the specific example $x'(t)=-3x(t)+2x(t-\tau)$ to demonstrate the idea: first compute the allowable upper bound on the delay from the inequalities, then use Mathematica numerical solving to verify the change in behavior.

## Results
- For the example equation $x'(t)=-3x(t)+2x(t-\tau)$, the no-delay solution is $x(t)=\exp(1-t)$, which exhibits **monotone decay to 0**.
- After substituting into the small-delay condition, one gets that when $2\tau \exp(3\tau)$ satisfies the bounds, the example is guaranteed to be of the same type as the no-delay case; the article further computes that the condition holds when **$\tau < 0.404218$**.
- In the numerical example, **$\tau=0.4$** is used, and the Mathematica solution shows that the solution rises to 1 in the initial stage according to the given history function, and then **ultimately still decays monotonically to 0**, consistent with the no-delay system.
- When the delay is changed to **$\tau=3$**, the numerical solution becomes **oscillatory**, showing that a larger delay can change the qualitative behavior of the system.
- The article does not provide machine-learning-style benchmark metrics; instead, it provides a clear theoretical threshold condition and two concrete numerical cases ($\tau=0.4$ vs. $\tau=3$) to support the conclusion.

## Link
- [https://www.johndcook.com/blog/2026/03/02/small-delay/](https://www.johndcook.com/blog/2026/03/02/small-delay/)
