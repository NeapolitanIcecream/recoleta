---
source: hn
url: https://www.provos.org/p/finding-zero-days-with-any-model/
published_at: '2026-04-30T23:49:07'
authors:
- dnw
topics:
- code-intelligence
- agentic-security
- vulnerability-discovery
- software-foundation-models
- multi-agent-workflows
- automated-code-audit
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Finding Zero Days with any model?

## Summary
The paper claims that zero-day discovery depends as much on orchestration as on restricted high-end models. IronCurtain pairs commercial or open-weight models with stateful agent workflows that search code, build harnesses, and validate findings.

## Problem
- AI security reports often treat novel vulnerability discovery as a capability limited to restricted models such as Anthropic Mythos Preview.
- Static findings create false positives; defenders need executable proof to decide whether a reported bug is reachable and worth urgent triage.
- Cost and access matter because broad audits only work if teams can run many investigations across large open-source codebases.

## Approach
- IronCurtain defines vulnerability-discovery workflows as finite-state machines in YAML.
- A central Orchestrator agent reads an append-only journal, chooses the next specialist agent, and keeps the investigation state outside the model context.
- Each agent starts with a fresh context window and reloads the journal plus disk artifacts, which lets long investigations continue across many model calls.
- The workflow follows a simple cycle: form a static hypothesis, build a harness, run it, and escalate only when needed.
- Validation uses tiers: single-function fuzzers, multi-component harnesses, and full VM or end-to-end proof-of-concept runs.

## Results
- The workflow reproduced the 27-year-old OpenBSD TCP SACK vulnerability from 1998 that Anthropic cited in its Mythos report; an early Sonnet 4.6 run found the issue by static analysis but needed later workflow changes and manual steering to reach execution.
- Opus 4.6 built a targeted fuzzer that isolated the OpenBSD trigger to a difference of 2 sequence numbers out of 4.3 billion, at the 32-bit signed integer boundary, then a QEMU-based driver reproduced the kernel panic.
- One run on a widely deployed media codebase found a previously unreported vulnerability with Opus 4.6 and produced a multi-component harness; full end-to-end proof needed human guidance because constrained reproduction environments hid the trigger.
- A GLM 5.1 run, routed through LiteLLM with the same IronCurtain workflow, found an 18-year-old integer truncation flaw in a foundational library and generated a proof-of-concept plus sanitizer-validated harness.
- Follow-up manual analysis with Opus 4.7 confirmed controlled out-of-bounds heap read and write primitives; a 7-step exploit plan stopped after 2 accepted steps due to policy refusal, but step 2 showed ASLR could be bypassed by reading base pointers.
- Reported investigation cost was about 10 million tokens per Opus or Sonnet run, costing about $150 with Opus and $30 with Sonnet; 5 hosted GLM 5.1 runs averaged 27 million tokens each and landed in the same cost range as Sonnet under Z.AI pricing.

## Link
- [https://www.provos.org/p/finding-zero-days-with-any-model/](https://www.provos.org/p/finding-zero-days-with-any-model/)
