---
source: arxiv
url: https://arxiv.org/abs/2607.02436v1
published_at: '2026-07-02T17:08:21'
authors:
- Achint Mehta
topics:
- agentic-code-generation
- code-intelligence
- reasoning-effort
- software-evaluation
- human-ai-interaction
- coding-agents
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Reasoning effort, not tool access, buys first-try reliability in agentic code generation: an observational study

## Summary
The study finds that higher reasoning effort improved first-try reliability in agentic code generation more than browser testing tool access did. In 90 repeated builds of the same retrospective board app, Playwright increased cost without improving functional scores, while xHigh reasoning sharply reduced repair prompts.

## Problem
- Teams often add browser testing tools and design-heavy prompts to coding agents, assuming these additions produce better software.
- Single-run coding-agent comparisons hide run-to-run variance and mix model choice with tools, prompts, and reasoning settings.
- The practical issue is cost: teams need to know which agent settings reduce human repair work on the first attempt.

## Approach
- The study ran 90 independent agent sessions on the same detailed OpenSpec task: a React/Vite and Node.js real-time retrospective board with SQLite, WebSockets, Docker deployment, CSV export, and documentation.
- Each output was graded on 14 functional criteria, with a maximum score of 42. A criterion got 3 if it worked first try, 2 if one corrective prompt fixed it, and 1 if it stayed broken.
- The study varied model family, agent harness, Playwright tool access, reasoning effort, and design prompt use while repeating identical configurations.
- Visual quality was rated separately on a 1 to 5 scale from screenshots, then checked by a human evaluator.
- The analysis also tracked first-try failures by criterion, session cost, output tokens, cache-read tokens, model time, and lines added.

## Results
- Frontier model families scored near the 42-point ceiling: Claude Opus 4.7 averaged 41.3, Claude Opus 4.6 averaged 40.7, and Claude Sonnet 4.6 averaged 41.0. Qwen averaged 30.5 across 2 runs, with scores of 24 and 37.
- Raising Claude Opus 4.7 from High to xHigh reasoning raised first-try perfect runs from 5 of 18 (28%) to 16 of 18 (89%). Corrective prompts fell from 16 total prompts to 3, while median cost rose by 9% to 29% depending on condition.
- Docker deployment was the main defect: it failed first try in 40 of 90 runs (44%). Local environment setup failed first try in 15 runs, so the two environment criteria made up 55 of 100 first-try criterion failures.
- Playwright did not improve functional score or reliability in matched comparisons. On Opus 4.7 it raised median cost by 42% at High effort and 68% at xHigh effort; on Opus 4.6 it kept the same mean score of 40.6 while raising median cost by 27%.
- Tool cost came mainly from context re-reading. In the Opus 4.7 grid, cache-read tokens rose from 2.3M to 5.3M at High effort and from 2.3M to 7.0M at xHigh when Playwright was enabled.
- Design prompts improved appearance without improving function. Full design-prompt runs averaged 4.5 of 5 on visual quality, abridged-prompt runs averaged 4.7, and unprompted Claude Code runs were all rated 3.0; drag-and-drop first-try failures appeared in 11 of 40 design-prompted runs versus 5 of 45 unprompted runs.

## Link
- [https://arxiv.org/abs/2607.02436v1](https://arxiv.org/abs/2607.02436v1)
