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
- software-engineering
- debugger-driven-development
- ide-design
- pharo
- program-evolution
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# It's Alive! What a Live Object Environment Changes in Software Engineering Practice

## Summary
This paper discusses how a “live object environment” like Pharo changes software engineering practice: developers program, inspect, and evolve systems directly in running objects and debugging contexts, rather than following the traditional edit-build-run-debug pipeline. Through multiple scenarios, the paper shows how this IDE design enables a more continuous and interactive development workflow.

## Problem
- Traditional IDEs mostly inherit a file-driven, phased **edit > build > run > debug** model, creating a split between development and runtime state.
- This abstract, offline workflow makes it harder for developers to understand programs based on real running objects, quickly validate changes, or debug and evolve code in context.
- This matters because IDE design directly shapes how developers think, how efficiently they debug, how APIs evolve, and overall engineering practice.

## Approach
- Using Pharo as a case study, the paper argues that the IDE and the language/runtime should be designed as a single “live system”: code exists as in-memory objects, and tools and applications share the same object space.
- It presents the core mechanism through **Debugger-Driven Development / Xtreme TDD**: first write a failing test, then when a method is missing, create and implement the code directly in the debugger, and continue execution without restarting.
- It shows “generating code/assertions from live values”: for example, using `try:` in a test to observe runtime values, then automatically converting them into concrete assertions, reducing guesswork about expected values.
- It demonstrates moldable debugging and object-centric tools: extending the debugger with Sindarin scripts and custom stepping; using the Inspector to define custom domain views and directly visualize objects such as country shapes.
- It presents support for system evolution: using microcommits for rollback, on-the-fly rewriting when methods are deprecated, and object-/instance-level breakpoints to enable smoother API migration and problem localization.

## Results
- This paper is primarily a **position-and-scenarios** paper; the excerpt **does not provide formal quantitative experiments, benchmark data, or statistically significant results**.
- The strongest concrete claim in the paper is that developers can complete the loop of **test failure → automatic creation of a missing method → implementation inside the debugger → resume execution and pass the test** within a **single live debugging session**.
- For test construction, the paper claims that statements like `self try: RoutePlan new defaultSchedulePlan` can be automatically transformed into real assertions based on **runtime values**, such as `equals: 'success'`, thereby reducing manual inspection.
- For debugging, the paper claims that scripts can encapsulate “step until execution reaches `schedulePackage:for:`” as a new debugging command, adapting to scenarios with multiple implementations or multiple dispatch.
- For understanding complex objects, the paper shows that the Inspector can be extended from the default instance-variable view to **domain-specific visualizations** (such as country shapes in an SVG world map), making domain representations a first-class IDE tool.
- For evolution, the paper claims that Pharo can combine **microcommits**, caller tracing, and **runtime automatic rewriting of deprecated calls** to support incremental migration, but the excerpt provides no numbers on error rates, migration success rates, or efficiency gains.

## Link
- [http://arxiv.org/abs/2603.02987v1](http://arxiv.org/abs/2603.02987v1)
