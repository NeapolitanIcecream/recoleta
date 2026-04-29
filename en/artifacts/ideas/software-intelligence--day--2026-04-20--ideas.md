---
kind: ideas
granularity: day
period_start: '2026-04-20T00:00:00'
period_end: '2026-04-21T00:00:00'
run_id: f9f4ae89-06b0-46d4-b288-2d12297bfb6b
status: succeeded
topics:
- coding-agents
- execution-verification
- interactive-code-generation
- test-structure
- developer-tools
tags:
- recoleta/ideas
- topic/coding-agents
- topic/execution-verification
- topic/interactive-code-generation
- topic/test-structure
- topic/developer-tools
language_code: en
pass_output_id: 99
pass_kind: trend_ideas
upstream_pass_output_id: 98
upstream_pass_kind: trend_synthesis
---

# Execution-verified coding workflows

## Summary
Execution-backed coding work is getting concrete enough to support specific product and workflow changes. The clearest cases here are front-loaded edge-case capture tied to sandbox regression checks, browser-run acceptance checks for interactive front-end output, and inline test handling to improve whether assistants preserve and pass prompted tests.

## Pre-write edge-case capture with sandboxed regression checks for high-risk code
A code assistant that asks for edge cases before it writes the first line looks newly practical for workflows where wrong answers are expensive. SolidCoder shows the clearest leverage point: removing the edge-case planning step drops GPT-4o on CodeContests from 77.0% pass@1 to 53.3%, a much larger loss than removing later repair steps. The same paper pairs that front-loaded planning with property-based assertions, sandbox execution, and retention of every failing test found during repair.

The build here is narrow and testable: add a pre-write edge-case pane to an IDE or PR bot for bug-prone functions, then auto-generate property checks and keep a growing regression set through each model revision. Teams maintaining parsers, data transforms, pricing logic, and API adapters would care first because they already pay for hidden boundary-case failures after merge. A cheap validation pass is to run the workflow on a fixed set of production bug tickets and compare first-pass correctness and bug reintroduction rates against a standard prompt-only assistant. The cost is higher token and API usage, so this fits review-critical code paths better than routine boilerplate.

### Evidence
- [SolidCoder: Bridging the Mental-Reality Gap in LLM Code Generation through Concrete Execution](../Inbox/2026-04-20--solidcoder-bridging-the-mental-reality-gap-in-llm-code-generation-through-concrete-execution.md): Reports the execution-backed pipeline, pass@1 gains, and the large ablation drop from removing shift-left edge-case planning.
- [SolidCoder: Bridging the Mental-Reality Gap in LLM Code Generation through Concrete Execution](../Inbox/2026-04-20--solidcoder-bridging-the-mental-reality-gap-in-llm-code-generation-through-concrete-execution.md): Abstract confirms the paper's core claim that sandboxed execution and pre-generation edge-case awareness close model planning and verification failures.

## Headless-browser acceptance checks for agent-built front-end flows
Teams building interactive web products can now evaluate agent output with browser-run health checks instead of relying on compile status and spot review. OpenGame is a useful template because it treats generated software as a running system: it uses reusable project skeletons, a stored debugging protocol, and repeated headless verification, then scores outputs on Build Health, Visual Usability, and Intent Alignment. On 150 prompts, OpenGame with Claude Sonnet 4.6 beats Cursor with the same model by about six points on each metric.

The concrete workflow change is to add a browser-executed scorecard to internal tools that generate dashboards, microsites, onboarding flows, or lightweight educational simulations. A first version does not need full game generation. It needs page load checks, console-error capture, visible-element assertions, and a simple rubric for whether the output matches the request after interaction. The immediate user is any team already demoing agent-built front-end work and struggling with broken wiring across files, assets, and state. A cheap check is to take a backlog of recent front-end tasks, run the assistant three times per task, and compare acceptance rates before and after adding browser execution plus a small repair loop.

### Evidence
- [OpenGame: Open Agentic Coding for Games](../Inbox/2026-04-20--opengame-open-agentic-coding-for-games.md): Summarizes the OpenGame workflow, the headless-browser benchmark, and the metric gains over Cursor using the same model.
- [OpenGame: Open Agentic Coding for Games](../Inbox/2026-04-20--opengame-open-agentic-coding-for-games.md): Abstract text states that interactive playability needs runtime verification and describes the evaluation pipeline built around headless browser execution and judged user-visible quality.

## Inline test rewrites before code generation
Prompted tests should sit next to generated code when teams want assistants to keep those tests intact through generation and editing. The doctest study makes this operational, not stylistic. Across 830-plus generated files and 12 models, inline Python doctests were preserved almost perfectly and kept high correctness, while separated Rust test blocks produced large model-to-model swings, including several Claude Opus versions that removed every provided test block. The same study also shows that temperature 0 does not guarantee repeatable outputs.

A practical build is a repo helper that rewrites generation prompts and temporary work files into inline test form before model calls, then expands them back into the team's preferred test layout after acceptance. This is most relevant for scaffold generation, utility functions, and migration scripts where teams already ask models for implementation plus tests in one pass. The cheap check is simple: pick one task family, run the same prompts with inline and separated tests across the models your team uses, and measure test preservation, pass rate, and output stability over repeated temperature-0 runs. If a model keeps dropping tests, the problem may be prompt structure before it is model quality.

### Evidence
- [Co-Located Tests, Better AI Code: How Test Syntax Structure Affects Foundation Model Code Generation](../Inbox/2026-04-20--co-located-tests-better-ai-code-how-test-syntax-structure-affects-foundation-model-code-generation.md): Gives the main empirical result that inline doctests preserve and pass far more reliably than separated test blocks.
- [Co-Located Tests, Better AI Code: How Test Syntax Structure Affects Foundation Model Code Generation](../Inbox/2026-04-20--co-located-tests-better-ai-code-how-test-syntax-structure-affects-foundation-model-code-generation.md): Abstract content states the 830-plus file study, the preservation and correctness gap, and the lack of determinism even at temperature 0.
