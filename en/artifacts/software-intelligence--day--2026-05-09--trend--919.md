---
kind: trend
trend_doc_id: 919
granularity: day
period_start: '2026-05-09T00:00:00'
period_end: '2026-05-10T00:00:00'
topics:
- coding agents
- program repair
- execution feedback
- code generation
- formal verification
- agent safety
- multi-agent systems
run_id: materialize-outputs
aliases:
- recoleta-trend-919
tags:
- recoleta/trend
- topic/coding-agents
- topic/program-repair
- topic/execution-feedback
- topic/code-generation
- topic/formal-verification
- topic/agent-safety
- topic/multi-agent-systems
language_code: en
pass_output_id: 138
pass_kind: trend_synthesis
---

# Executable evidence dominates agent software reliability research

## Overview
The day’s strongest signal is executable evidence for agent software. Papers test code with generated inputs, diagnose failed runs from telemetry, and enforce contracts around skills or tool actions. Agent output now needs a checkable trace before teams trust it.

## Findings

### Execution-based code selection
Several code-generation papers treat execution traces as the main signal for choosing or rejecting large language model (LLM) outputs. Semantic Voting clusters candidate programs by sandboxed behavior on generated inputs; across 18 HumanEval+ and MBPP+ settings, execution-based selectors beat output-pattern majority voting by 19 to 52 percentage points. SketchVerify adds structured candidate generation: it asks for different algorithmic sketches, fills them, then verifies candidates by execution fingerprints. On 19 hard HumanEval+ problems for Gemini 3.1 Flash Lite, K=2,M=5 solved 11 problems versus 5 for flat N=10 sampling.

Uncertainty work follows the same practical route. Semantic distance estimation (SDE) and directed SDE compare sampled programs by graded behavioral distance on fuzzed inputs. The directed variant reports AUROC 0.844 for GPT-4o-mini on LiveCodeBench pass@1 failure prediction, beating listed baselines such as DiffTrust and Semantic Entropy in the summary table.

#### Sources
- [Semantic Voting: Execution-Grounded Consensus for LLM Code Generation](../Inbox/2026-05-09--semantic-voting-execution-grounded-consensus-for-llm-code-generation.md): Semantic Voting summary gives execution-fingerprint selection method and 19–52 point gains over output-pattern majority voting.
- [Sketch-and-Verify: Structured Inference-Time Scaling via Program Sketching](../Inbox/2026-05-09--sketch-and-verify-structured-inference-time-scaling-via-program-sketching.md): SketchVerify summary reports sketch-based candidate generation and hard HumanEval+ gains over flat sampling.
- [Using Semantic Distance to Estimate Uncertainty in LLM-Based Code Generation](../Inbox/2026-05-09--using-semantic-distance-to-estimate-uncertainty-in-llm-based-code-generation.md): Semantic distance summary reports DSDE method, LiveCodeBench AUROC, and baseline comparisons.

### Repair and recovery after failed runs
Program repair work is giving learning systems finer credit for what changed. BoostAPR trains on execution-verified demonstrations, then uses a sequence reward model and a line-level reward model during PPO. On SWE-bench Verified, it reaches 40.7% pass@1 on 500 tasks, up from 17.8% for the Qwen2.5-Coder-32B base model. The line-level reward adds 2.4 points over sequence-only PPO in the reported result.

PROBE addresses a later stage of the same reliability problem: what to do after an agent fails. It records span-level telemetry, localizes the failure anchor, and emits bounded retry guidance only when the diagnosis is grounded and actionable. Across 257 initially unresolved cases, it reports 65.37% Top-1 diagnosis accuracy and 21.79% recovery. The gap between those two numbers is useful: finding the fault is easier than producing a next run that succeeds.

#### Sources
- [BoostAPR: Boosting Automated Program Repair via Execution-Grounded Reinforcement Learning with Dual Reward Models](../Inbox/2026-05-09--boostapr-boosting-automated-program-repair-via-execution-grounded-reinforcement-learning-with-dual-reward-models.md): BoostAPR summary provides dual reward model design and benchmark results on SWE-bench Verified and other repair benchmarks.
- [Debugging the Debuggers: Failure-Anchored Structured Recovery for Software Engineering Agents](../Inbox/2026-05-09--debugging-the-debuggers-failure-anchored-structured-recovery-for-software-engineering-agents.md): PROBE summary provides telemetry-based diagnosis design, recovery gating, and diagnosis/recovery results.

### Contracts and proofs for agent side effects
Agent reliability papers also put checks around the environment that agents touch. SkillGuard turns stale skill-library assumptions into contracts over operational items such as package versions, URLs, API paths, environment variables, and configuration files. On DriftBench, it reports 0 false positives across 599 no-drift and hard-negative cases, while contract-free CI probes produce 40% false positives. In a live scan of 49 real skills, one-round contract-guided repair reaches 78% success.

Formal verification appears in two forms. Containment verification proves boundary policies in the agent runtime, using Dafny to verify a PocketFlow action interface with allowed reads, tool calls, and step bounds. A separate compiler study gives cost data: full Lean 4 verification of coding-agent compiler optimizations takes about 7.6 to 19.9 times more active development time than credible compilation in the tested passes, with thousands of proof lines added for the verified versions.

#### Sources
- [Skill Drift Is Contract Violation: Proactive Maintenance for LLM Agent Skill Libraries](../Inbox/2026-05-09--skill-drift-is-contract-violation-proactive-maintenance-for-llm-agent-skill-libraries.md): SkillGuard summary reports contract extraction, DriftBench composition, false-positive rates, and repair success.
- [Containment Verification: AI Safety Guarantees Independent of Alignment](../Inbox/2026-05-09--containment-verification-ai-safety-guarantees-independent-of-alignment.md): Containment verification summary describes Dafny-checked boundary policy for PocketFlow and its invariants.
- [Quantitative Comparison of Credible Compilation and Verification In Coding Agent Compiler Development](../Inbox/2026-05-09--quantitative-comparison-of-credible-compilation-and-verification-in-coding-agent-compiler-development.md): Compiler verification summary gives active-time ratios, token ratios, and proof-line burdens for full verification versus credible compilation.

### Agent coordination and topology
Coordination is becoming a test target, not just a system design choice. AgentCollabBench injects constraints, tracer strings, false facts, and private strings into 900 software, DevOps, and data-engineering tasks. It finds that communication topology explains 7% to 40% of the variance in multi-hop information survival, with converging DAG nodes losing minority-branch constraints more often than linear chains.

Evolutionary Ensemble of Agents studies coordination during coding-agent search. It keeps scored populations of solver code and agent guidance, then updates agents through Elo-style wins from their solver outputs. On the ICON positional-encoding task, the method finds a rescale-then-interpolate encoding that improves generalization to unseen example counts; at k=10, error stays below 0.15 with 2,000 training steps and below 0.08 with 10,000 steps in the reported setup.

#### Sources
- [AgentCollabBench: Diagnosing When Good Agents Make Bad Collaborators](../Inbox/2026-05-09--agentcollabbench-diagnosing-when-good-agents-make-bad-collaborators.md): AgentCollabBench summary provides benchmark size, topology types, risk metrics, and variance explained by topology.
- [Evolutionary Ensemble of Agents](../Inbox/2026-05-09--evolutionary-ensemble-of-agents.md): EvE summary describes scored solver/agent populations and reported ICON generalization results.
