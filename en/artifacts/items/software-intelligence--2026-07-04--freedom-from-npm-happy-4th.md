---
source: hn
url: https://www.npmjs.com/package/donobu
published_at: '2026-07-04T22:40:30'
authors:
- vasusen
topics:
- ai-testing
- playwright
- code-intelligence
- autonomous-agents
- test-auto-healing
- developer-tools
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Freedom from NPM. Happy 4th

## Summary
Donobu is a Playwright SDK and CLI that adds AI-driven browser actions, assertions, failure triage, and auto-healing to web tests. The excerpt describes a developer tool, not a research paper, and gives no benchmark evidence.

## Problem
- Web UI tests often break when selectors, layout, or content change, which creates maintenance work for developers and slows release checks.
- Plain Playwright tests require developers to encode low-level actions and assertions; Donobu aims to let tests state user goals such as navigating to a page or checking a map result.
- Failure diagnosis can take time because screenshots, DOM state, model reasoning, and repair steps are often scattered or missing.

## Approach
- Donobu extends Playwright with a typed fixture: `import { test } from 'donobu'` adds `page.ai` helpers, smart selectors, persistence, and prebuilt wrappers such as `page.runAccessibilityTest`.
- A test can call `page.ai()` with natural-language instructions; optional Zod schemas, tool allow-lists, cached tool-call replays, and environment-variable controls constrain the agent.
- Each `page.ai()` call is cached next to the spec in `.cache-lock/<spec-file>.cache.js`, so generated actions or selectors can be reused or regenerated with `--clear-ai-cache`.
- The CLI mirrors Playwright commands and adds Donobu settings for triage directories, cache clearing, and auto-heal retries.
- On failure, Donobu stores evidence, builds a treatment plan, and can rerun an autonomous repair flow that attempts to update selectors or test code.

## Results
- The excerpt provides no quantitative benchmark results: no accuracy, pass-rate, latency, cost, dataset, or baseline comparison is reported.
- The package claims a single dependency for the Playwright fixture, Page.AI orchestration layer, CLI wrapper, failure triage, and plugin system.
- Runtime requirements include Node.js 18+, npm 8+ or pnpm 10+ or yarn, Playwright browsers, and at least 1 LLM credential.
- Supported model paths include Donobu API, OpenAI, Anthropic direct, Google Gemini, Anthropic through AWS Bedrock, and `BASE64_GPT_CONFIG`.
- Failure evidence is written under `test-results/donobu-triage/<timestamp>-<runId>/`, with treatment plans saved beside the evidence and prefixed with `treatment-plan-`.
- With `--auto-heal`, successful repairs attach `fixed-test.ts` and annotate runs with `@self-healed`, but the excerpt gives no success rate.

## Link
- [https://www.npmjs.com/package/donobu](https://www.npmjs.com/package/donobu)
