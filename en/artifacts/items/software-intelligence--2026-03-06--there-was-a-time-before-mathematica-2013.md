---
source: hn
url: https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/
published_at: '2026-03-06T23:19:28'
authors:
- masfuerte
topics:
- symbolic-computation
- programming-language-design
- computer-algebra
- mathematica-history
- software-systems
relevance_score: 0.44
run_id: materialize-outputs
language_code: en
---

# There Was a Time before Mathematica (2013)

## Summary
This is a retrospective article describing the design, implementation, and commercialization journey of SMP, the predecessor system to Mathematica, and how those experiences shaped Mathematica. Its importance lies in revealing how a core set of ideas behind modern symbolic computation and computational language design was gradually formed and validated.

## Problem
- The problem was **how to get computers to reliably handle large-scale symbolic mathematics and general computation**, so that researchers would not have to repeatedly “chase minus signs and coefficients” in complex algebraic derivations.
- Existing systems at the time (such as Reduce, Macsyma, and Schoonschip) were either too specialized, insufficiently interactive, or ran into limits in scale and expressive power, making them hard to use for broader scientific computation and program construction.
- This mattered because theoretical physics, engineering, and scientific research needed not just numerical computation, but an interactive, programmable, and extensible symbolic computation environment; the author further believed that such an environment could become the foundation for long-term scientific research and technology products.

## Approach
- The core mechanism was to **represent computation uniformly as transformations on symbolic expressions**: the user writes an expression of a certain form, and the system uses patterns and rules to rewrite it into another form.
- The author first built the predecessor system **SMP (Symbolic Manipulation Program)** to explore language design, including capabilities such as pattern matching, rule replacement, list/function representation, code generation, and parallel processing.
- In designing Mathematica, he retained the main line that had proven effective in SMP: **symbolic expressions + transformation rules**, while removing designs that were hard to understand or impractical, such as “chameleonic symbols,” overly unified symbolic indexed lists, excessively strong semantic matching, complicated recursion control, and user-defined syntax traps.
- Methodologically, the author emphasized making minimal yet powerful abstractions at the level of language primitives, and forcing interfaces and semantics to remain clear by writing documentation alongside the design.
- From an implementation perspective, SMP began being implemented in C in 1980; Mathematica was restarted from scratch in 1986 to cover a much broader scope—algebra, numerics, graphics, programming, and interface—rather than being only an algebra system.

## Results
- The article **does not provide quantitative results from standard academic experiments or benchmark tests**, so there are no precise metric/dataset/baseline comparison numbers.
- The strongest concrete results given are the timeline and system milestones: SMP began coding in **1980**, Version 1 was running in **June 1981**; the first Mathematica code was written in **October 1986**, and version 1.0 was officially released on **June 23, 1988**.
- The author claims that the design principles have had strong durability: by the time of writing, Mathematica had developed for **25 years**, and “**most Mathematica 1.0 code will still run unchanged today**.”
- SMP was already a “large software system” at the time, yet its executable was still **under 1 MB**; the author says that during development he at times reached a coding speed of about **1000 lines per day**.
- Commercially and in platform support, Mathematica had already secured partnerships with multiple vendors before release, first **NeXT**, followed by **Sun, Silicon Graphics, IBM**, and others; the author presents this as evidence of the system’s market viability and impact.
- The article’s central breakthrough claim is not a point improvement in performance, but that through the trial and error of the predecessor system SMP, Mathematica’s general computational paradigm was ultimately established, enabling it to support later products and research over the long term (including **A New Kind of Science** and **Wolfram|Alpha** mentioned by the author).

## Link
- [https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/](https://writings.stephenwolfram.com/2013/06/there-was-a-time-before-mathematica/)
