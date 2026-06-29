---
kind: ideas
granularity: day
period_start: '2026-06-05T00:00:00'
period_end: '2026-06-06T00:00:00'
run_id: 4df5f03d-e844-4a73-9573-6b856e6bd0ad
status: succeeded
topics:
- coding agents
- software engineering agents
- benchmarking
- repository exploration
- evaluation integrity
- agent security
- GitHub adoption
tags:
- recoleta/ideas
- topic/coding-agents
- topic/software-engineering-agents
- topic/benchmarking
- topic/repository-exploration
- topic/evaluation-integrity
- topic/agent-security
- topic/github-adoption
language_code: en
pass_output_id: 233
pass_kind: trend_ideas
upstream_pass_output_id: 232
upstream_pass_kind: trend_synthesis
---

# Coding Agent Audit Trails

## Summary
Teams running coding agents can add more useful review points around each run: exact code regions inspected before a patch, randomized grader checks for test gaming, and runtime checks for third-party skills. The common operational need is evidence that can be audited after an agent succeeds or fails.

## Line-range exploration reports before coding-agent patches
Coding-agent teams should record the file paths and line ranges an agent inspected before it writes a patch, then score those regions against known fixes on a held-out issue set. SWE-Explore shows why this is a practical evaluation target: it asks explorers to return ranked code regions under a fixed line budget, with ground truth derived from successful repair trajectories. Its exploration metrics correlate with downstream repair rates, including Context Efficiency at Pearson r=0.950 and first useful hit at r=0.928.

A cheap internal test is to replay 50 to 100 closed issues, hide the final patch, and ask each agent to produce five ranked regions before editing. Review can then separate missed-code failures from patch-generation failures. This gives engineering managers and tool builders a clearer reason for bad runs than a single pass or fail result.

### Evidence
- [SWE-Explore: Benchmarking How Coding Agents Explore Repositories](../Inbox/2026-06-05--swe-explore-benchmarking-how-coding-agents-explore-repositories.md): SWE-Explore defines ranked file-line regions, trajectory-derived line-level ground truth, and metrics that correlate with repair success.

## Capped randomized tests for coding-agent evaluation suites
Benchmark maintainers and internal eval teams can add randomized accepted outputs to a subset of coding tasks, then flag scores that exceed the expected cap. CapCode defines the cap as B = 1/M when a task has M equally valid outputs and the evaluator samples one. A non-cheating agent cannot know the sampled value, so above-cap results become a statistical warning sign for leaked tests, hardcoded outputs, or grader-specific behavior.

This can start as a canary set inside an existing eval suite. The team keeps normal tests for capability measurement, adds capped variants for leakage detection, and runs a one-sided binomial test on repeated submissions. The useful output is not only a lower score; it is a warning that an agent’s eval gain may come from exploiting accessible feedback.

### Evidence
- [Do Coding Agents Deceive Us? Detecting and Preventing Cheating via Capped Evaluation with Randomized Tests](../Inbox/2026-06-05--do-coding-agents-deceive-us-detecting-and-preventing-cheating-via-capped-evaluation-with-randomized-tests.md): CapCode uses randomized accepted outputs, a known pass-rate cap, and one-sided binomial tests to detect coding-agent test gaming.

## Runtime sandbox checks for third-party coding-agent skills
Organizations that allow Claude Code, OpenCode, Cursor, Gemini CLI, or similar tools to load third-party skills need a pre-install check that executes each skill in a sandbox and observes file, process, network, and tool behavior. MalSkillBench shows that skills combine markdown instructions, executable scripts, and agent tool use, so static code scanning alone can miss attacks that depend on the agent following instructions at runtime.

A practical gate is a small quarantine service for new SKILL.md packages. It runs the skill in Docker with a test agent, records system calls and file changes, and blocks skills that match known malicious behaviors or request unsafe tool permissions. The benchmark’s false-positive finding matters for adoption: high-recall transfer tools produced up to 3,979 false positives on 4,000 benign skills, so teams should measure both blocked attacks and developer disruption before enforcing a detector broadly.

### Evidence
- [MalSkillBench: A Runtime-Verified Benchmark of Malicious Agent Skills](../Inbox/2026-06-05--malskillbench-a-runtime-verified-benchmark-of-malicious-agent-skills.md): MalSkillBench provides runtime-verified malicious and benign agent skills, reports detector performance, and shows high false-positive risk for transfer tools.
