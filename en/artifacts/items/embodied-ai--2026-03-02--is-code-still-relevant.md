---
source: hn
url: https://ajchambeaud.com/blog/is-code-still-relevant/
published_at: '2026-03-02T22:58:56'
authors:
- facundo_olano
topics:
- ai-coding-agents
- software-engineering
- developer-productivity
- code-generation
- human-in-the-loop
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Is Code Still Relevant?

## Summary
This article is not an academic paper, but an industry observation grounded in frontline development experience: the author argues that AI coding agents have already significantly changed the software development process, turning “hand-written code” from a core activity into an execution step that is supervised. The core judgment is that code still matters, but the value of programmers will shift more toward specification definition, architectural judgment, testing, and debugging.

## Problem
- The article discusses this question: when AI can automatically generate and modify large amounts of code, **is code itself still the core asset of software engineering**, and **are programmers still important**.
- This matters because it directly affects software engineering workflows, skill requirements, hiring structures, and the growth path of junior developers.
- The author also points out a practical risk: if the operator does not understand the implementation details, AI is more likely to introduce regressions, temporary patches, and increasing system complexity.

## Approach
- The core method is not to propose a new algorithm, but to compare changes in development patterns before and after AI based on the author's **16 years of programming experience** and **6 months** of continuous practice using Copilot, ChatGPT, Cursor, and Claude Code.
- Mechanistically, the author describes a new simplest workflow: **humans define requirements and constraints, AI writes the code, and humans then review, test, and correct course**.
- The author re-layers development activities: lower-level code writing is becoming increasingly automated, while higher-level tasks such as system structure, file organization, architectural decisions, manual testing, specification writing, and code review are still led by humans.
- The author especially emphasizes that AI agents can automatically read project context and execute changes, which is more powerful than earlier autocomplete-style tools, but they still often “go down rabbit holes” on complex design problems and require experienced developers to explicitly guide them to step back and refactor.

## Results
- The strongest quantitative signal is the author's personal practical conclusion: over the past **6 months**, the author says they **have not written a single line of code entirely by hand**, and after using Claude Code, they “almost stopped writing code manually.”
- The author reports a clear efficiency claim: **writing code manually now feels “too slow”**, indicating that in the author's day-to-day development, AI agents have replaced most coding labor; however, the article **does not provide standard benchmarks, datasets, or formal controlled experiments**.
- A concrete workflow result is that the center of gravity of development time has shifted toward **manual testing, design decisions, and writing specifications/prompts**, rather than implementing code line by line.
- On the reliability side, AI can usually **find bugs quickly and implement features from scratch**, but it can also head in the wrong direction, apply temporary fixes for circular dependencies, and introduce potential regressions, so the author still insists on **reviewing code incrementally** rather than using a fully YOLO mode.
- The article’s bottom-line claim on whether “programmers will disappear” is: programmers will not disappear, but their role will shift toward higher-level capabilities such as **systems thinking, architectural tradeoffs, debugging complex problems, and turning vague requirements into executable specifications**.
- The most concrete judgment for beginners is that in the past **10 years**, going deep on just one popular tool might have been enough to get a job, but the author believes that in the future this path will **most likely no longer be sufficient**, and a broader capability profile will be needed.

## Link
- [https://ajchambeaud.com/blog/is-code-still-relevant/](https://ajchambeaud.com/blog/is-code-still-relevant/)
