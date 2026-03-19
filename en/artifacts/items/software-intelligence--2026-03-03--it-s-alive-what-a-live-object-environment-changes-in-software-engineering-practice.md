---
source: arxiv
url: http://arxiv.org/abs/2603.02987v1
published_at: '2026-03-03T13:41:30'
authors:
- "Juli\xE1n Grigera"
- Steven Costiou
- Juan Cruz Gardey
- "St\xE9phane Ducasse"
topics:
- live-programming
- ide-design
- debugger-driven-development
- software-evolution
- object-centric-tools
relevance_score: 0.71
run_id: materialize-outputs
language_code: en
---

# It's Alive! What a Live Object Environment Changes in Software Engineering Practice

## Summary
This article discusses how a live object environment (using Pharo/Smalltalk as the example) changes software engineering practice: it turns development from a staged pipeline of “edit-build-run-debug” into a process of continuously dialoguing with a running system. The core of the article is to demonstrate, through several concrete IDE features, that when code, objects, debuggers, and evolution tools share the same live runtime, the development process becomes more direct, malleable, and exploratory.

## Problem
- Traditional IDEs mostly inherit file- and compiler-driven workflows, where development is split into edit > build > run > debug, with poor continuity of state.
- Developers often can only “imagine what objects should look like” at an abstract level, rather than interact directly with running objects, which increases the cost of understanding, debugging, and evolution.
- This matters because tools shape developers’ ways of thinking and collaboration workflows; if IDE design is constrained, software engineering practice itself is also constrained.

## Approach
- Rather than proposing a new algorithm, the article uses Pharo’s live object environment to illustrate a different mechanism: the IDE itself is part of the running system, and both code and objects exist in the same live object space.
- It presents the core method through 3 types of scenarios: **writing code directly in the debugger and resuming execution** (Debugger-Driven Development / Xtreme TDD), **providing domain-specific inspector views for objects**, and **performing rollbackable and automatically rewritable API evolution in a live system**.
- For debugging, developers can create methods directly from the debugger when a missing method triggers an exception, implement code within a paused frame, use runtime values to automatically generate assertions, and write custom stepping/debugging scripts via the Sindarin API.
- For IDE extensibility, objects can define custom inspector presentations (such as the graphical shape of a geographic object), allowing understanding and analysis to revolve around “live objects” rather than file formats.
- For evolution, microcommits, usage tracking, and on-the-fly rewriting of deprecated calls are combined to progressively migrate APIs during execution, rather than through one-shot static replacement.

## Results
- This paper **does not provide systematic quantitative experimental results**; it does not report metrics such as accuracy, percentage time savings, user-study sample sizes, or benchmark comparison numbers.
- Its most concrete and strongest claim is that Pharo supports **creating missing methods, implementing methods directly in the debugger, and resuming original execution**, thereby turning the debugger into the main development interface rather than a post hoc troubleshooting tool.
- The paper claims that the `try` assertion can use **real runtime values** to automatically turn incomplete tests into concrete assertions, for example converting `self try: RoutePlan new defaultSchedulePlan` into a real assertion like `self assert: ... equals: 'success'`.
- The article shows that, through custom inspector tabs, domain objects such as `EarthMapCountry` can be presented directly as **graphical shape views**, emphasizing that object visualization and navigation become first-class IDE capabilities.
- For evolution, the paper argues that **microcommit rollback** and **automatic rewriting of deprecated calls** enable safer API renaming and migration in a live environment, but it does not provide quantified benefits.
- Overall, the main contribution is not numerical SOTA, but a shift in engineering practice that is instructive for mainstream IDEs: from file-centered, staged development toward object-centered, continuous interactive development.

## Link
- [http://arxiv.org/abs/2603.02987v1](http://arxiv.org/abs/2603.02987v1)
