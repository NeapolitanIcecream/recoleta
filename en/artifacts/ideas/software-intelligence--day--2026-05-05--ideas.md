---
kind: ideas
granularity: day
period_start: '2026-05-05T00:00:00'
period_end: '2026-05-06T00:00:00'
run_id: 842d8137-2ca9-438a-83fe-96abd745f33f
status: succeeded
topics:
- coding agents
- software security
- test generation
- multi-agent systems
- code search
- quantum software
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-security
- topic/test-generation
- topic/multi-agent-systems
- topic/code-search
- topic/quantum-software
language_code: en
pass_output_id: 131
pass_kind: trend_ideas
upstream_pass_output_id: 130
upstream_pass_kind: trend_synthesis
---

# Executable Validation for Agent-Written Java Code

## Summary
Executable tests are becoming the practical control point for agent-written code. The clearest workflow changes are cumulative security review for multi-ticket agent work, generated JUnit proof-of-vulnerability tests for dependency triage, and fail-to-pass reproduction tests before Java issue fixes are accepted.

## Cumulative-diff exploit checks for agent-authored Jira ticket chains
Teams that let coding agents work through ordinary backlog tickets should add a security check over the cumulative diff, not only the latest ticket. MOSAIC-Bench shows why: three harmless-looking tickets can compose into an exploitable application change, and nine production coding agents reached 53.3% to 85.9% attack success on staged chains with only two refusals across the benchmark.

A practical version is a CI job for agent-authored multi-ticket work: deploy the changed service in Docker, run deterministic exploit oracles for the affected surface, and require a second reviewer prompt that reads the full cumulative diff with an adversarial security role. MOSAIC-Bench found that neutral reviewer agents approved 24.8% of oracle-confirmed vulnerable cumulative diffs as routine pull requests, while pentester framing reduced evasion on the evaluated subset. The first adoption point is high-risk web application work where agents touch authentication, authorization, object mapping, deserialization, file handling, or query construction across several tickets.

### Sources
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): MOSAIC-Bench reports staged Jira-style attack chains, deterministic Docker proof-of-concept oracles, high attack success rates across production coding agents, and reviewer-agent miss rates.
- [MOSAIC-Bench: Measuring Compositional Vulnerability Induction in Coding Agents](../Inbox/2026-05-05--mosaic-bench-measuring-compositional-vulnerability-induction-in-coding-agents.md): The paper reports reviewer-agent approval of confirmed vulnerable cumulative diffs and lower evasion under pentester-framed review.

## JUnit proof-of-vulnerability tests for reachable dependency CVEs
Java teams triaging dependency alerts can ask a coding agent for a runnable JUnit proof-of-vulnerability test tied to an application entry point. PoVSmith gives a concrete recipe: find public application methods that reach vulnerable library APIs, generate a JUnit test with the vulnerable API, CVE or issue ID, affected version, call path, and an exemplar exploit test, then repair the test using build and execution logs.

This fits the security engineer’s recurring problem: a scanner says a library version is affected, but the team needs evidence that the vulnerable behavior is reachable through its own code. In PoVSmith’s evaluation across 33 Java application-library pairs, the system found 152 correct call paths, compiled 141 generated tests, and triggered vulnerabilities in 84 cases. A small internal trial could run this workflow on recent dependency alerts and measure three simple outcomes: correct call path, compiling test, and vulnerability-triggering execution.

### Sources
- [Generating Proof-of-Vulnerability Tests to Help Enhance the Security of Complex Software](../Inbox/2026-05-05--generating-proof-of-vulnerability-tests-to-help-enhance-the-security-of-complex-software.md): PoVSmith describes the application-level call-path search, JUnit PoV generation, build-feedback repair loop, and results across 33 Java application-library pairs.
- [Generating Proof-of-Vulnerability Tests to Help Enhance the Security of Complex Software](../Inbox/2026-05-05--generating-proof-of-vulnerability-tests-to-help-enhance-the-security-of-complex-software.md): The paper reports 152 generated tests and 84 tests that demonstrated feasible attacks through vulnerable libraries.

## Fail-to-pass reproduction tests before Java issue fixes
Java maintainers can require an agent-generated reproduction test before work starts on a bug fix. The test has to fail on the current buggy code and pass after the fix, giving the reviewer an executable check that the issue was reproduced and then removed.

TDD-Bench-Java and e-Otter++ show the workflow in enough detail to copy for enterprise Java repositories: localize likely files and functions from the issue report, create one new Java test class in the right package and test directory, run it on the old code, read build or test logs, and revise for up to 10 iterations. On 250 Java issues from 13 open-source repositories, e-Otter++ reached 43.6% fail-to-pass with Claude-Sonnet-4.5 and 46.4% with GPT-5.2. Execution-based refinement added 9.4 and 13.6 percentage points over the initial generator, which points to build-log repair as the useful support layer.

### Sources
- [Reproduction Test Generation for Java SWE Issues](../Inbox/2026-05-05--reproduction-test-generation-for-java-swe-issues.md): TDD-Bench-Java defines fail-to-pass reproduction tests for Java issues and reports e-Otter++ workflow details and benchmark results.
- [Reproduction Test Generation for Java SWE Issues](../Inbox/2026-05-05--reproduction-test-generation-for-java-swe-issues.md): The paper states that reproduction tests fail on the current code base and pass after the issue has been addressed.
