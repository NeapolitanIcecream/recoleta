---
source: hn
url: https://www.johndcook.com/blog/2026/03/02/small-delay/
published_at: '2026-03-03T23:27:34'
authors:
- ibobev
topics:
- delay-differential-equations
- stability-analysis
- small-delay
- dynamical-systems
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Differential Equation with a Small Delay

## Summary
This article discusses a class of first-order delay differential equations with a small delay, and explains that when the delay is sufficiently small, its qualitative behavior is the same as in the no-delay case. The core conclusion is an explicit criterion for when the delay is “sufficiently small,” and a concrete example shows that a small delay preserves decay while a large delay introduces oscillation.

## Problem
- The research question is: for the equation $x'(t)=ax(t)+bx(t-\tau)$, when does the qualitative behavior remain the same as that of the equation with the delay removed after introducing the delay $\tau$?
- This matters because delay terms often significantly change a system’s stability and dynamical form; if we can state conditions under which a “small delay does not change the essential behavior,” then modeling and analysis can be simplified.
- For delay differential equations, there is an additional difficulty: the solution is not determined only by an initial value at a single point, but also requires an initial history function on the interval $[-\tau,0]$.

## Approach
- The article cites an existing theorem that gives sufficient conditions for a small delay for the specific linear delay differential equation $x'(t)=ax(t)+bx(t-\tau)$.
- Put most simply: if the delay parameter is small enough that certain inequalities involving $a$, $b$, and $\tau$ hold, then the overall dynamical type of the system does not change because of the delay.
- The specific criterion is: $-1/e < b\tau e^{-a\tau} < e$ and $a\tau < 1$; there is also a technical condition on the initial history function that typically holds except on a nowhere-dense set.
- The article then uses the concrete example $x'(t)=-3x(t)+2x(t-\tau)$ for numerical verification, comparing the behavior of solutions under small and large delays.

## Results
- The key theoretical result is: for the equation $x'(t)=ax(t)+bx(t-\tau)$, when $-1/e < b\tau e^{-a\tau} < e$ and $a\tau < 1$, its qualitative behavior is the same as that of the no-delay equation with $\tau=0$.
- In the example $x'(t)=-3x(t)+2x(t-\tau)$, the small-delay condition becomes $-1/e < 2\tau e^{3\tau} < e$, which yields the threshold $\tau < 0.404218$.
- When $\tau=0$, the no-delay solution is $x(t)=e^{1-t}$, whose behavior is monotone decay to 0.
- When $\tau=0.4$, numerical solution shows that although the solution first rises to 1 according to the prescribed initial history, it then still ultimately decays monotonically to 0, consistent with the no-delay case.
- When $\tau=3$, the numerical experiment shows oscillation, indicating that a larger delay changes the qualitative behavior of the system.
- The text does not provide systematic experimental metrics or benchmark datasets; the strongest quantitative claims are the explicit inequality conditions above and the critical value $0.404218$ in the example.

## Link
- [https://www.johndcook.com/blog/2026/03/02/small-delay/](https://www.johndcook.com/blog/2026/03/02/small-delay/)
