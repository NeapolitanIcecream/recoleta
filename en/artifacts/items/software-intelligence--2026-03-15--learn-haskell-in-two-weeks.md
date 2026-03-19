---
source: hn
url: https://mercury.com/blog/learn-haskell-in-two-weeks
published_at: '2026-03-15T22:28:07'
authors:
- cosmic_quanta
topics:
- haskell-training
- active-learning
- developer-education
- feedback-loops
- mentorship
relevance_score: 0.48
run_id: materialize-outputs
language_code: en
---

# Learn Haskell in Two Weeks

## Summary
This article introduces Mercury's two-week Haskell training program for new hires, LHbE, whose core is "exercise-only learning, intensive feedback, and daily mentor guidance." The author argues that, compared with books and lectures, this practice-driven approach enables engineers to reach a level of proficiency for working in a real backend codebase more quickly.

## Problem
- Help new hires from different backgrounds acquire enough Haskell in **just two weeks** to handle real backend/web development tasks.
- The author believes traditional approaches such as reading books, long-form explanations, and passive lectures cause learning to stall, especially when the goal is to quickly build the ability to solve practical problems.
- Haskell has a high learning curve, many concepts, and complex error feedback; without frequent, high-quality feedback, learners can easily get stuck or merely "arrive at the answer" without truly understanding it.

## Approach
- Designed a linear training flow of **10 exercise sets over 10 business days**, covering topics from types, Hoogle, and GHCi to Maybe/Either, Monad, and monad transformer stacks, while also incorporating real codebase tasks such as adding routes, JSON Handlers, tests, and database models.
- Uses a **purely exercise-driven** format: no books, no lectures, and almost no long-form materials; each module begins with a worked example, followed by 20–30 progressive exercises to reinforce the concepts.
- Established a **layered feedback system**: immediate type checking, viewing type errors within 15 seconds, using Hoogle within 1 minute, asking an LLM/search within 5 minutes, contacting a mentor within 15 minutes; this is further supplemented by tests, PR review, and a daily 30-minute one-on-one mentor call.
- Mentors rely primarily on **Socratic questioning**, trying to avoid "thinking for the learner" or directly giving answers, with emphasis on training the ability to reason from types, actively find information, check one's own work, and communicate uncertainty.
- The goal of the training is not to stuff learners with fixed knowledge points, but to cultivate transferable skills: especially **reasoning with types**, using the toolchain (Hoogle/GHCi/typechecker), and maintaining learning initiative when facing unknown problems.

## Results
- Over the past **6 months**, the program has been used with **50+ learners**, spanning a wide range from interns to managers and senior engineers.
- Learners typically reach **monad transformer stacks** within **10 business days**; the article explicitly states that "learners routinely reach the topic of monad transformer stacks within 10 business days".
- The program includes a placement test taking **under 10 minutes** to identify existing Haskell ability and provide an accelerated version, reducing wasted time on already-mastered material.
- There are examples showing that progress can be even faster: one intern completed LHbE in **8 days**; the author also mentions that someone who did not even know `Double` on the first day still completed the program.
- The article **does not provide strict controlled experiments, standardized datasets, or formal baseline metrics**, so there are no quantitative results such as accuracy/F1/pass@k to report.
- The strongest concrete claim is that outcomes improved after removing the accompanying book, and the author believes that intense active practice plus rich feedback are key to helping new hires gain Haskell fluency "super quickly," but this is mainly based on internal experience rather than formal experimental validation.

## Link
- [https://mercury.com/blog/learn-haskell-in-two-weeks](https://mercury.com/blog/learn-haskell-in-two-weeks)
