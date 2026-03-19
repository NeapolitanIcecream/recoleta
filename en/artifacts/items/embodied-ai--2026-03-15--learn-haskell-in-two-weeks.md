---
source: hn
url: https://mercury.com/blog/learn-haskell-in-two-weeks
published_at: '2026-03-15T22:28:07'
authors:
- cosmic_quanta
topics:
- haskell
- programming-pedagogy
- exercise-driven-learning
- feedback-loops
- developer-onboarding
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Learn Haskell in Two Weeks

## Summary
This article introduces LHbE, Mercury’s two-week Haskell onboarding training program for new engineers. Its core claim is that “practice matters more than explanation, and feedback density determines learning speed.” It is not a research paper, but a summary of a teaching method based on internal company practice.

## Problem
- The problem the article addresses is: **how to bring new hires with no Haskell background to a level where they can work effectively in a real backend codebase in just 10 business days**.
- This matters because Mercury’s backend depends on Haskell; if the learning curve for new hires is too steep, it slows ramp-up, affects code quality, and increases mentor burden.
- The author also emphasizes that traditional approaches (reading books, attending lectures, long-form explanations) tend to leave learners at the stage of “I understand it when I see it, but I can’t do it,” so a more efficient and more actionable training process is needed.

## Approach
- The core mechanism is a **fully exercise-driven** two-week course: 10 sets of sequential exercises covering everything from type signatures, Maybe/Either, IO, and type classes to Functor/Applicative/Monad and then monad transformer stacks.
- Methodologically, it emphasizes **using almost no long-form teaching materials or lectures**, instead relying on worked examples plus many progressive exercises so learners build mental models through real coding.
- The training includes **daily one-on-one mentoring**, where mentors try not to give direct answers and instead use Socratic questioning to avoid “stealing learning,” forcing learners to reason things out themselves.
- The article proposes a **layered feedback system**: immediate type checking, type error feedback within 15 seconds, Hoogle queries within 1 minute, LLM/search within 5 minutes, mentor help within 15 minutes, plus tests, PR review, and daily calls to form a closed loop.
- At the cognitive level, the course especially emphasizes **reasoning through types**, actively surfacing uncertainty, continuous self-checking, and using tools (Hoogle, GHCi, typed holes) to shorten feedback loops.

## Results
- In the past **6 months**, the program has been used with **50+ learners**, including **interns, managers, and senior engineers**, showing that the method has been adopted fairly broadly internally.
- The standard course pace is **10 business days to complete 10 sets of exercises**; the author says learners can usually reach **monad transformer stacks within 10 business days**.
- The article gives one concrete case: **an intern completed** the entire LHbE in **8 days**.
- The author says they designed a Haskell placement test that takes **under 10 minutes** for quickly routing employees who already have some background.
- It does not provide rigorous experimental metrics, control groups, pass rates, test scores, or quantitative measures of productivity improvement; the strongest specific claims are that **learning outcomes improved after removing the companion book**, and that abundant rapid feedback can significantly increase learning speed.

## Link
- [https://mercury.com/blog/learn-haskell-in-two-weeks](https://mercury.com/blog/learn-haskell-in-two-weeks)
