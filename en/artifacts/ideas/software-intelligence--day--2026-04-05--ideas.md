---
kind: ideas
granularity: day
period_start: '2026-04-05T00:00:00'
period_end: '2026-04-06T00:00:00'
run_id: e30d1f13-3c1f-4ef7-8316-e547eaa9439c
status: succeeded
topics:
- coding-agents
- software-engineering
- compiler-feedback
- software-architecture
- agent-control
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering
- topic/compiler-feedback
- topic/software-architecture
- topic/agent-control
language_code: en
pass_output_id: 17
pass_kind: trend_ideas
upstream_pass_output_id: 16
upstream_pass_kind: trend_synthesis
---

# Software agent control gates

## Summary
Control surfaces are getting concrete in software-agent work, especially where tickets, compilers, and review gates give the system a hard boundary. The clearest near-term builds are a Jira-linked execution loop for bounded maintenance work, a GnuCOBOL repair service that uses compiler feedback to raise compilation success, and an architecture review gate that catches prompt-driven system changes before they pass as routine code edits.

## Jira ticket execution loop with verifier gates and isolated worktrees
A Jira-linked agent loop is now concrete enough to pilot in teams that already manage compliance, security fixes, and backlog cleanup through tickets. The useful build is narrow: an agent that can ingest structured inputs, map work into a canonical backlog, claim tickets through fixed Jira states, make changes in isolated worktrees, and update Jira only after product and security verification. The reported case uses explicit thresholds for autonomous execution, human review, and re-ingest, plus lock handling, retries, and degraded operation during Jira outages. That matters for teams blocked less by code generation than by auditability and state control across many small maintenance tasks.

A first deployment target is recurring ticket families with clear verification, such as dependency updates, low-risk remediation, or backlog deduplication. The cheap test is operational: run the loop on one bounded queue for two weeks and measure duplicate ticket creation, terminal-state completion, verifier pass rate, and the share of items pushed to human review. The evidence here is better on control and traceability than on broad software delivery coverage, so the product should stay close to existing ticket workflows and avoid open-ended task intake at the start.

### Evidence
- [Closed-Loop Autonomous Software Development via Jira-Integrated Backlog Orchestration: A Case Study in Deterministic Control and Safety-Constrained Automation](../Inbox/2026-04-05--closed-loop-autonomous-software-development-via-jira-integrated-backlog-orchestration-a-case-study-in-deterministic-control-and-safety-constrained-automation.md): Jira-backed deterministic control loop, confidence thresholds, verifier gates, and observed terminal-state results support a concrete ticket automation workflow.
- [Closed-Loop Autonomous Software Development via Jira-Integrated Backlog Orchestration: A Case Study in Deterministic Control and Safety-Constrained Automation](../Inbox/2026-04-05--closed-loop-autonomous-software-development-via-jira-integrated-backlog-orchestration-a-case-study-in-deterministic-control-and-safety-constrained-automation.md): Abstract content confirms bounded AI actions, run counts, adversarial review findings, and continuous-operation artifacts.

## GnuCOBOL repair loop for LLM-generated maintenance patches
Compiler-guided repair for COBOL generation now looks practical enough for internal maintenance tooling. The concrete build is a generation-and-repair service around GnuCOBOL: produce code for a bounded maintenance task, compile it, feed the compiler errors back into the model, and stop only when the program compiles or the retry budget is exhausted. This fits teams that need help with small changes in legacy systems but cannot accept raw model output that fails basic compilation.

The strongest near-term use is not full application generation. It is targeted work such as translating change requests into candidate patches, filling repetitive boilerplate, or drafting isolated batch-job updates that already have test fixtures. The reported gains are large on compilation success, including GPT-4o moving from 41.8% to 95.89%, with pass@1 improvements as well. A useful evaluation plan is simple: sample a fixed set of maintenance tickets, compare one-shot generation against compiler-guided revision, and record compile success, test pass rate, and the error categories that still need human repair. The error taxonomy is also useful product input because incorrect program structure and built-in function misuse are recurrent failure modes.

### Evidence
- [COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation](../Inbox/2026-04-05--cobolassist-analyzing-and-fixing-compilation-errors-for-llm-powered-cobol-code-generation.md): Summary reports the COBOL repair loop, error taxonomy, and large compilation-success gains after compiler feedback.
- [COBOLAssist: Analyzing and Fixing Compilation Errors for LLM-Powered COBOL Code Generation](../Inbox/2026-04-05--cobolassist-analyzing-and-fixing-compilation-errors-for-llm-powered-cobol-code-generation.md): Abstract content confirms GPT-4o-mini and GPT-4o improvements under iterative compilation-guided repair.

## Architecture diff gate for agent-generated pull requests
Architecture review needs a separate check step before teams trust agents on diagram-heavy work. Two pieces of evidence meet here. One shows that prompt wording alone can change the generated system shape, adding components such as schema validators, retry handlers, tool registries, agent loops, and SQLite state. The other shows that current vision-language models are still weak at reading software architecture diagrams, with best reported accuracy at 70.18% and large drops on harder diagram types and relation-heavy questions. A team that asks an agent to implement from diagrams, prompts, and partial specs should assume architecture drift unless it records decisions explicitly and checks them against source artifacts.

The practical build is an architecture diff gate in CI or review tooling. Capture the prompt, generated file graph, dependency additions, infrastructure components, and any referenced diagram or ADR. Then require a structured review when the build introduces state stores, orchestration loops, external tools, or new interface contracts. For diagram inputs, keep the model on extraction and highlighting tasks that a reviewer can verify quickly, not final judgment over behavioral or relation-heavy diagrams. The cheapest validation is to run the gate on a week of agent-generated pull requests and count how often it catches unreviewed architecture changes that would otherwise pass as ordinary code edits.

### Evidence
- [Architecture Without Architects: How AI Coding Agents Shape Software Architecture](../Inbox/2026-04-05--architecture-without-architects-how-ai-coding-agents-shape-software-architecture.md): Summary reports prompt-driven architectural divergence and concrete component additions across variants.
- [Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding](../Inbox/2026-04-05--benchmarking-and-evaluating-vlms-for-software-architecture-diagram-understanding.md): Summary reports SADU benchmark accuracy limits and failure patterns on architecture diagrams.
- [Benchmarking and Evaluating VLMs for Software Architecture Diagram Understanding](../Inbox/2026-04-05--benchmarking-and-evaluating-vlms-for-software-architecture-diagram-understanding.md): Abstract content confirms the gap between current VLM performance and design-stage software engineering needs.
