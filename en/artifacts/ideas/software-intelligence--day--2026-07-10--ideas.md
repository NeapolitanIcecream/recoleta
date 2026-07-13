---
kind: ideas
granularity: day
period_start: '2026-07-10T00:00:00'
period_end: '2026-07-11T00:00:00'
run_id: f235cefd-d9d2-4d5d-b862-9eb6d448b8e2
status: succeeded
topics:
- coding agents
- software testing
- formal verification
- agent memory
- reusable skills
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-testing
- topic/formal-verification
- topic/agent-memory
- topic/reusable-skills
language_code: en
pass_output_id: 317
pass_kind: trend_ideas
upstream_pass_output_id: 316
upstream_pass_kind: trend_synthesis
---

# Coding Agent Reliability Systems

## Summary
Coding-agent teams can improve reliability by converting bug intake into fail-to-pass tests, encoding recurring correctness claims as shared proof and property-based test templates, and preserving approved repository context across repeated tasks. Each change can be tested on a small set of real maintenance jobs before broader adoption.

## Bug intake that produces validated fail-to-pass tests
Add an automated triage step that turns each new issue into a test that fails on the reported revision and passes after the accepted fix. The workflow should retrieve repository structure, run the candidate test, and return the suspected files or functions alongside a proposed repair direction for maintainer review. ReProAgent reproduced 70.30% of SWT-bench-verified issues at an average cost of $0.14 per issue, while a separate SWE-bench Verified study found that affected-code locations and suggested fixes had the clearest positive associations with agent repair success. A practical trial can use 50 recently closed defects: hide the final patch, generate the test and localization hints, then measure valid reproductions, maintainer review time, and downstream patch pass rate.

### Evidence
- [ReProAgent: Tool-Augmented Multi-Stage Agentic Generation of Bug Reproduction Tests from Issue Reports](../Inbox/2026-07-10--reproagent-tool-augmented-multi-stage-agentic-generation-of-bug-reproduction-tests-from-issue-reports.md): Reports ReProAgent's reproduction rates, per-issue cost, and downstream repair improvement.
- [ReProAgent: Tool-Augmented Multi-Stage Agentic Generation of Bug Reproduction Tests from Issue Reports](../Inbox/2026-07-10--reproagent-tool-augmented-multi-stage-agentic-generation-of-bug-reproduction-tests-from-issue-reports.md): Defines fail-to-pass tests as executable specifications that support patch validation and automated repair.
- [Writing Bug Reports for Software Repair Agents: What Information Matters Most?](../Inbox/2026-07-10--writing-bug-reports-for-software-repair-agents-what-information-matters-most.md): Finds that localization cues and suggested fixes narrow the search and repair space and are positively associated with successful repairs.

## Shared property templates for proofs and runtime tests
Teams maintaining query engines, compilers, data libraries, or optimization rules can store recurring correctness claims as parameterized templates with matching Lean 4 proof obligations and property-based tests. A coding agent fills the property-specific holes, while CI compares the machine-checked model with the live implementation. DualVeri raised proof-synthesis success by 1.6× on average, reduced proof hallucinations by 59%, and cut property-based test intent mismatches from 22 to 1 across 400 candidate properties. Start with one repetitive property family, such as optimizer equivalence or aggregation decomposition, and track template completion, proof failures, runtime counterexamples, and model-to-implementation disagreements over 20 to 30 properties.

### Evidence
- [Agentic Proof and Property-Based Testing via Property-Templates in Data-Intensive Computing](../Inbox/2026-07-10--agentic-proof-and-property-based-testing-via-property-templates-in-data-intensive-computing.md): Describes the shared proof and property-based testing templates, evaluation design, and measured gains across 400 properties.
- [Agentic Proof and Property-Based Testing via Property-Templates in Data-Intensive Computing](../Inbox/2026-07-10--agentic-proof-and-property-based-testing-via-property-templates-in-data-intensive-computing.md): Explains the distinct coverage of formal proof and property-based testing against the real implementation.
- [Agentic Proof and Property-Based Testing via Property-Templates in Data-Intensive Computing](../Inbox/2026-07-10--agentic-proof-and-property-based-testing-via-property-templates-in-data-intensive-computing.md): Shows why recurring property families in data systems can be encoded once and instantiated across APIs.

## Versioned repository context for recurring maintenance tasks
Persist approved task specifications, schemas, tool settings, and output constraints in a versioned workspace for recurring coding-agent jobs such as dependency updates, release preparation, and scheduled report generation. Exclude reasoning traces, failed recovery paths, raw data, and temporary tool logs; refresh compatible inputs through a stable runtime interface. In an evaluation of 24 recurring enterprise tasks, selective memory reached 96% completion, compared with 79% for stateless sessions and 71% for full-history memory. Public software-engineering skill repositories also show a packaging gap: 63.8% of 11,497 skills contain instructions only, and 13.6% include executable code assets. A team can test the approach on one monthly maintenance workflow by measuring completion, corrective turns, token use, and failures caused by stale context across three cycles.

### Evidence
- [Shared Selective Persistent Memory for Agentic LLM Systems](../Inbox/2026-07-10--shared-selective-persistent-memory-for-agentic-llm-systems.md): Specifies the reusable context categories, excluded transient material, completion results, and zero-token refresh mechanism.
- [Shared Selective Persistent Memory for Agentic LLM Systems](../Inbox/2026-07-10--shared-selective-persistent-memory-for-agentic-llm-systems.md): Reports comparative completion results and explains versioned artifacts and compatible data refresh.
- [Inside the Skill Market: From Software Engineering Activities to Reusable Agent Skills](../Inbox/2026-07-10--inside-the-skill-market-from-software-engineering-activities-to-reusable-agent-skills.md): Quantifies the prevalence of instruction-only skills and the limited inclusion of executable assets across 11,497 software-engineering skills.
