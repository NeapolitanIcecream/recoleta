---
kind: ideas
granularity: day
period_start: '2026-05-12T00:00:00'
period_end: '2026-05-13T00:00:00'
run_id: e98cb69a-9fb9-41ca-aa60-26b8a20e83d2
status: succeeded
topics:
- agent evaluation
- benchmark security
- agent tracing
- MCP governance
- software assurance
- code translation
- LLM testing
tags:
- recoleta/ideas
- topic/agent-evaluation
- topic/benchmark-security
- topic/agent-tracing
- topic/mcp-governance
- topic/software-assurance
- topic/code-translation
- topic/llm-testing
language_code: en
pass_output_id: 149
pass_kind: trend_ideas
upstream_pass_output_id: 148
upstream_pass_kind: trend_synthesis
---

# Inspectable Agent Operations

## Summary
Agent teams now have concrete audit gates to copy: pre-release reward-hacking runs for benchmarks, centrally governed MCP servers with trace requirements, and path-level review for code translation. The common pressure is operational: scores, tool calls, and translated code need retained evidence that another team can inspect after the fact.

## Pre-release reward-hacking audits for agent benchmarks
Benchmark maintainers can add a pre-release red-team pass that tries to earn task credit without doing the task, records the exploit path, and reruns after fixes. BenchJack gives a concrete pattern: map entry points, scoring code, task files, environments, and trust boundaries; scan against a flaw taxonomy; then generate a tested exploit such as a `run.sh` that maximizes score. In its reported audit, BenchJack produced working exploits for all 10 agent benchmarks it tested and found 219 distinct flaws. Its patching loop cut hackable-task ratios below 10% on four fixable benchmarks and fully patched WebArena and OSWorld within three iterations.

The release checklist should also include rollout-card exports for the same benchmark runs. Rollout Cards stores the task, environment state, observations, model outputs, tool calls, tool results, artifacts, timing, terminal status, failures, declared scoring view, reporting rule, and omitted fields. The paper’s audit of 50 repositories found that none reported failed, errored, or skipped rollouts beside headline scores, and re-grading fixed artifacts changed reported scores by up to 20.9 percentage points. A benchmark release can treat an unpublished exploit scan and missing rollout records as release blockers, because both affect whether later users can trust the reported score.

### Sources
- [Do Androids Dream of Breaking the Game? Systematically Auditing AI Agent Benchmarks with BenchJack](../Inbox/2026-05-12--do-androids-dream-of-breaking-the-game-systematically-auditing-ai-agent-benchmarks-with-benchjack.md): BenchJack’s audit design, exploit generation results, flaw count, and patching-loop outcomes support a concrete pre-release benchmark security gate.
- [Rollout Cards: A Reproducibility Standard for Agent Research](../Inbox/2026-05-12--rollout-cards-a-reproducibility-standard-for-agent-research.md): Rollout Cards specifies the rollout evidence bundle and reports repository-audit and re-grading results that justify score-trace publication.

## Centrally approved MCP servers with decision traces for tool access
Enterprise AI owners can move MCP servers off employee laptops and place them behind a managed approval, identity, logging, and policy layer. Cloudflare’s internal deployment gives a concrete operating model: employees expose an internal resource through a template after approval, inherit default-deny write controls, audit logging, CI/CD, and secrets management, and use OAuth through Cloudflare Access with SSO, MFA, IP, location, and device checks. Its portal pattern gives each employee one endpoint that exposes only authorized MCP servers, while traffic scans look for shadow MCP use through `/mcp`, `/mcp/sse`, and JSON-RPC methods such as `tools/call`, `tools/list`, and `resources/read`.

The trace requirement should be explicit at the point of MCP approval. A pilot on agent decision reconstructability found strict governance completeness ranging from 42.9% to 85.7% across six SDK regimes, with reasoning evidence missing or unusable across most surveyed regimes. A useful first rollout is one high-risk internal tool with writes disabled by default, per-user authorization, DLP rules, and a stored decision record for each tool call: actor, policy, tool, arguments, result, authorization source, and available reasoning evidence. Security teams then get an incident record that can answer who authorized a tool action and which policy applied.

### Sources
- [Scaling MCP adoption: Our ref architecture – simpler,safer&cheaper deployments](../Inbox/2026-05-12--scaling-mcp-adoption-our-ref-architecture-simpler-safer-cheaper-deployments.md): Cloudflare’s MCP deployment details provide the concrete controls: remote servers, approvals, OAuth checks, audit logging, DLP, default-deny writes, portal access, and shadow MCP detection.
- [Property-Level Reconstructability of Agent Decisions: An Anchor-Level Pilot Across Vendor SDK Adapter Regimes](../Inbox/2026-05-12--property-level-reconstructability-of-agent-decisions-an-anchor-level-pilot-across-vendor-sdk-adapter-regimes.md): The reconstructability pilot shows that current agent traces often lack decision evidence needed for post-hoc investigation.

## Path-level differential review for LLM-assisted code migration
Teams translating legacy C or C++ into Rust can add a review gate that shows developers only the behavioral differences the tool can prove are reachable. cozy compiles the original and translated programs to binaries, runs both under symbolic execution with the same symbolic inputs, compares compatible terminal states, and uses Z3 to prove selected outputs or generate concrete inputs that expose a difference. The developer then classifies each flagged difference as intended or erroneous, while the unflagged paths are treated as equivalent under the checked bounds.

This is a practical fit for incremental memory-safety migrations where automated translators, manual ports, and bug fixes can all change behavior. The reported cozy experiments are small: insertion sort, a watch update function, and a box blur filter. Even so, the workflow is concrete enough for a pilot on a bounded utility function with clear inputs and outputs. APL-to-C# work in the pack points to the same adoption pattern for other legacy languages: generate typed targets, compile them, run input-output tests, and feed compiler or test failures into repair attempts. The main gap is scale, so the first adoption target should be a small module with existing tests and well-defined state.

### Sources
- [Finding a Crab in the C: Assured Translation via Comparative Symbolic Execution](../Inbox/2026-05-12--finding-a-crab-in-the-c-assured-translation-via-comparative-symbolic-execution.md): cozy provides the comparative symbolic execution workflow, developer review loop, and small C/Rust experiments.
- [Neural Code Translation of Legacy Code: APL to C#](../Inbox/2026-05-12--neural-code-translation-of-legacy-code-apl-to-c.md): The APL-to-C# study supports compile-and-run evaluation, iterative repair with compiler and test feedback, and the legacy-code migration pain point.
