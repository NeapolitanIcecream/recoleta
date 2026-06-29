---
source: hn
url: https://htmx.org/essays/code-is-cheap/
published_at: '2026-06-06T23:58:45'
authors:
- chr15m
topics:
- ai-code-generation
- code-review
- software-complexity
- llm-tools
- human-ai-interaction
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# Code Is Cheap(er)

## Summary
The essay argues that AI has made code cheaper to write, which shifts more cost onto reading, judging, and simplifying code. Its main advice is to keep LLM changes small and make engineers responsible for blocking unnecessary complexity.

## Problem
- AI coding tools can produce large code changes faster than developers can understand them, so teams may merge behavior they cannot explain or maintain.
- This matters most for mission-critical software, where generated code still needs human review and ownership.
- Cheap code can increase system complexity; the author claims complexity grows faster than system size and can make codebases hard to change.

## Approach
- Treat LLM output as code that must be read and understood after generation, since the normal act of writing no longer creates understanding.
- Use LLMs incrementally, especially when new semantics enter a codebase; reserve large generated changelists mainly for mechanical refactors.
- Reject the compiler-output comparison for 3 reasons: compilers are deterministic, compiler workflows keep source code, and compiler output targets machine code rather than general software.
- Adopt the “subtractive, constraining engineer” role: say no, inspect output, simplify design, remove layers, and block unneeded code and system boundaries.

## Results
- No quantitative benchmark, dataset, baseline, or measured result is provided.
- The essay claims code generation cost has dropped in the last year because AI tools can generate large amounts of reasonable code quickly.
- It lists 3 concrete limits of the compiler analogy: determinism, retained source, and constrained output domain.
- It gives 1 main operational recommendation: use LLMs in small increments so reviewers can understand each change.
- Its strongest concrete claim is that uncontrolled LLM output can raise complexity and make systems harder to modify, but it provides no empirical measurement for that claim.

## Link
- [https://htmx.org/essays/code-is-cheap/](https://htmx.org/essays/code-is-cheap/)
