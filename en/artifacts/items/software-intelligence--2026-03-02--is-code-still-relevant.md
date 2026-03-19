---
source: hn
url: https://ajchambeaud.com/blog/is-code-still-relevant/
published_at: '2026-03-02T22:58:56'
authors:
- facundo_olano
topics:
- ai-coding-agents
- software-engineering
- code-generation
- human-ai-collaboration
- developer-workflow
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Is Code Still Relevant?

## Summary
This article discusses whether programmers are still important after the rapid progress of AI coding agents, and whether the status of "writing code" itself is declining in software development. The author's core judgment is: code still matters, but the value of programmers is shifting from hand-written implementation toward specification, architecture, review, testing, and system-level judgment.

## Problem
- The article addresses the question: when AI can already generate large amounts of code, **is code still at the core of software engineering**, and **what role do programmers still play**.
- This matters because it directly affects software engineering workflows, talent development, the entry barrier for junior roles, and the industry's view on whether "non-developers can directly use AI to produce software."
- The author also highlights a practical risk: if code is treated entirely as a black box and handed off to agents, it may lead to regressions, architectural degradation, and uncontrolled complexity.

## Approach
- This is not an experimental paper, but an **experience-based analysis grounded in long-term frontline development practice**: the author compares how tools such as Copilot, ChatGPT, Cursor, and Claude Code have changed their role in real development.
- The core mechanism can be summarized as: **humans are responsible for stating requirements, providing context, making architectural decisions, and reviewing; AI is responsible for generating and modifying code; humans then test, correct, and approve the result**.
- The author describes a migration from "hand-written code + AI autocomplete" to "mostly relying on agents to modify code," emphasizing that efficiency still depends on developers understanding implementation details rather than blindly delegating in a YOLO-style way.
- The article further proposes a restructuring of roles: the main value of programmers is shifting toward **systems thinking, debugging, tradeoff analysis, and turning ambiguous requirements into executable specifications**, rather than just manual coding.

## Results
- The clearest quantitative evidence comes from the author's personal practice: **in the past 6 months, they have not written a single line of code entirely by themselves**, suggesting that AI agents can already cover most coding tasks in their daily development work.
- The author claims that after adopting **Claude Code**, they **have almost stopped writing code manually**, and argues that "writing code by hand already feels too slow"; this is a strong efficiency claim, but **the article provides no formal benchmarks, datasets, or controlled experiments**.
- Compared with earlier tools, the author believes **Copilot's autocomplete experience was poor and often failed to match intent**; **Cursor** improved the experience through more natural completion and in-IDE context reading; **Claude Code** further pushed the workflow toward agentic development centered on "prompt-review-test."
- The author's key boundary conclusion is: **current AI agents are still unreliable for non-developer operators**, and are more likely to make mistakes and introduce regressions, because such users typically do not recognize problems like circular dependencies, temporary patches, and architectural drift.
- The strongest claim about the future is: code will not disappear anytime soon, nor can it yet become a complete black box; but in the software industry, **code will become less visible, while programmers will increasingly take on multiple roles such as product, QA, architecture, and specification design**.

## Link
- [https://ajchambeaud.com/blog/is-code-still-relevant/](https://ajchambeaud.com/blog/is-code-still-relevant/)
