---
source: hn
url: https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/
published_at: '2026-03-06T23:19:28'
authors:
- masfuerte
topics:
- symbolic-computation
- programming-languages
- mathematica
- computer-algebra
- software-history
relevance_score: 0.02
run_id: materialize-outputs
language_code: en
---

# There Was a Time before Mathematica (2013)

## Summary
This is not a research paper, but a historical article in which Stephen Wolfram looks back on the prehistory of Mathematica, focusing on the design, commercialization, and lessons learned from its predecessor SMP. The main value of the article lies in showing how the design philosophy of symbolic computation languages and systems gradually evolved into Mathematica.

## Problem
- Early theoretical physics and mathematical computation involved large amounts of tedious and error-prone algebraic derivation; doing it by hand led to inefficient work spent “chasing minus signs and coefficients.”
- Existing algebra systems at the time (such as Reduce and Macsyma) had limited functionality, poor interactivity, and were hard to extend, so they could not satisfy the author’s need for a general-purpose high-level computational system.
- This matters because it explains why modern computational mathematics platforms need to unify **symbolic, numerical, graphical, programming, and interactive** capabilities within a single system.

## Approach
- The author first designed and implemented SMP (Symbolic Manipulation Program) for his own physics research needs, using **symbolic expressions** as the unified representation.
- The core mechanism of SMP/Mathematica is to treat computation as the application of **pattern matching and transformation rules** to symbolic expressions; simply put: “if an expression looks like this, rewrite it into that.”
- On this basis, the author pursued “expressing as much power as possible with as few primitives as possible,” gradually forming the language philosophy that later became Mathematica.
- Mathematica was redesigned from scratch in 1986, absorbing the experience of SMP, retaining symbolic expressions and rule transformation as the main thread, while expanding into numerical computation, graphics, interfaces, and a more understandable language design.
- The article also summarizes several failed design ideas (such as symbolically indexed lists, semantic pattern matching, overly strong recursion control, and user-defined syntax), showing how Mathematica achieved greater usability through simplification.

## Results
- The article **does not provide quantitative results from standard scientific experiments, datasets, or benchmark tests**.
- Explicit time points include: SMP began being written in C in **early 1980**; **June 1981** saw SMP Version 1 running; the first Mathematica code was written in **October 1986**, and version 1.0 was released on **June 23, 1988**.
- The author says that SMP was already a “large software system” at the time, with an executable size of “**just under 1 MB**.”
- Scale-related facts given in the text include: the author states that at one point he wrote SMP at a pace of about “**1000 lines of code per day**”; the early ARPANET had only “**256 hosts**”; and **25 years** had passed between Mathematica’s release and the time of writing.
- The article’s strongest concluding claim is that Mathematica’s foundational design principles have stood the test of time, and even that “**most Mathematica 1.0 code will still run unchanged today**”; at the same time, although SMP’s code was not reused, it provided crucial design priors for Mathematica.

## Link
- [https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/](https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/)
