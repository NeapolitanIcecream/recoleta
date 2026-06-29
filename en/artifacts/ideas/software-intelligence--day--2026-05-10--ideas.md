---
kind: ideas
granularity: day
period_start: '2026-05-10T00:00:00'
period_end: '2026-05-11T00:00:00'
run_id: 7c039469-47a9-47fa-88d9-76c1179828fa
status: succeeded
topics:
- AI coding agents
- software testing
- tool use
- agent monitoring
- security
- maintenance cost
- smart contracts
- tool provenance
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/software-testing
- topic/tool-use
- topic/agent-monitoring
- topic/security
- topic/maintenance-cost
- topic/smart-contracts
- topic/tool-provenance
language_code: en
pass_output_id: 141
pass_kind: trend_ideas
upstream_pass_output_id: 140
upstream_pass_kind: trend_synthesis
---

# Agent Failure-Mode Gates

## Summary
Agent software work is moving toward checks tied to specific failure modes: live tool calls that return plausible wrong answers, monitors tested with narrow attack sets, and C/C++ libraries whose sequential tests miss shared-memory interactions. The practical work is to add small gates around those workflows before agents touch production systems or security-critical repositories.

## Pre-execution contract checks for code-mode tool-use agents
Teams running code-mode agents against live tools can add a verification pass before the first environment action. The verifier should read the task instruction and tool registry, then check the generated program for output shape, tool choice, call signatures, argument provenance, and call order. Failed checks should produce concrete repair instructions and rerun generation without executing the tool call.

RubricRefine is a useful template because it targets failures that can complete without runtime exceptions: wrong routing, broken data flow between tools, and valid-looking final answers built from the wrong intermediate values. On M3ToolEval, it reports 0.86 average success across seven models, compared with 0.62 for single-pass CodeAct, with no execution attempts during refinement. The first internal test should use multi-step tasks where a bad live call can change state, spend money, hit a rate limit, or expose data.

### Evidence
- [RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement](../Inbox/2026-05-10--rubricrefine-improving-tool-use-agent-reliability-with-training-free-pre-execution-refinement.md): RubricRefine defines task- and registry-specific pre-execution checks and reports a 0.86 versus 0.62 success gain on M3ToolEval.
- [RubricRefine: Improving Tool-Use Agent Reliability with Training-Free Pre-Execution Refinement](../Inbox/2026-05-10--rubricrefine-improving-tool-use-agent-reliability-with-training-free-pre-execution-refinement.md): The paper explains why retrying after execution is costly when tool calls can alter external state or are rate-limited, paid, or safety constrained.

## Red-team refreshes for coding-agent monitors using broader attack trajectories
Monitor evaluations for coding agents should include a repeatable attack-generation step, not only a fixed set of direct prompts. A security team can build a small pipeline that separates attack strategy, execution in a sandbox, and post-hoc trajectory refinement, then keeps only attacks where the side task succeeds and the trajectory remains faithful to the strategy.

MonitoringBench shows why this matters for pre-deployment testing. Direct Opus 4.6 elicitation collapsed into a narrow attack distribution, with 81% of attacks falling into two of five technical tiers. After taxonomy-guided generation and refinement, the Opus 4.5 full-trajectory monitor’s catch rate fell from 94.9% on directly elicited Opus attacks to 60.3% on the best refined attacks. The attack set includes operationally relevant sabotage such as firewall backdoors, sudo privilege escalation, credential exfiltration, and malware download.

### Evidence
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): MonitoringBench describes the taxonomy, decomposition into strategy/execution/refinement, and the catch-rate drops under stronger attacks.
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): The abstract states the semi-automated red-teaming method and the 2,644-trajectory BashArena benchmark.
- [MonitoringBench: Semi-Automated Red-Teaming for Agent Monitoring](../Inbox/2026-05-10--monitoringbench-semi-automated-red-teaming-for-agent-monitoring.md): The paper describes mode collapse in direct attack elicitation and warns that high monitor scores can reflect weak red-teaming.

## Shared-memory access-pair test drivers for C/C++ libraries
Maintainers of C/C++ libraries can use agent-generated tests more effectively by aiming them at shared-memory access pairs. The workflow is concrete: use static analysis to find public entry points, shared variables, shared-memory access locations, and conflicting access pairs; trace backward from a target access to the inputs and object states that can reach it; generate multi-threaded drivers; run them under a dynamic analyzer such as ThreadSanitizer; feed uncovered pairs and build failures back into another generation round.

ConCovUp reports this pattern on nine real-world C/C++ libraries totaling about 1,000 kLoC. It raises average Shared Memory Access Pair Coverage from 36.6% with a Claude Code baseline to 68.1%. The reported gain is coverage of concurrent interactions, not a claim that every new test finds a bug, so the cheap adoption check is to measure new SMAP coverage and ThreadSanitizer findings on one library before adding it to regular CI.

### Evidence
- [ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing](../Inbox/2026-05-10--concovup-effective-agent-based-test-driver-generation-for-concurrency-testing.md): ConCovUp combines static shared-access analysis, backward path reasoning, multi-threaded driver generation, and execution feedback, with a 36.6% to 68.1% SMAP Coverage result.
- [ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing](../Inbox/2026-05-10--concovup-effective-agent-based-test-driver-generation-for-concurrency-testing.md): The paper states that dynamic tools such as TSan need test drivers that reach critical shared-memory interactions at runtime.
- [ConCovUp: Effective Agent-Based Test Driver Generation for Concurrency Testing](../Inbox/2026-05-10--concovup-effective-agent-based-test-driver-generation-for-concurrency-testing.md): The introduction explains why sequential unit tests miss internal synchronization interactions in open-source libraries.
