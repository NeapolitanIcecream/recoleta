---
kind: trend
trend_doc_id: 1018
granularity: day
period_start: '2026-05-16T00:00:00'
period_end: '2026-05-17T00:00:00'
topics:
- code agents
- agent benchmarks
- execution feedback
- GPU kernels
- code safety
- token cost
- supply-chain risk
run_id: materialize-outputs
aliases:
- recoleta-trend-1018
tags:
- recoleta/trend
- topic/code-agents
- topic/agent-benchmarks
- topic/execution-feedback
- topic/gpu-kernels
- topic/code-safety
- topic/token-cost
- topic/supply-chain-risk
language_code: en
pass_output_id: 156
pass_kind: trend_synthesis
---

# Code agents are being tested as bounded workers, not code generators

## Overview
The strongest signal is operational evaluation. 1GC-7RC, AgentKernelArena, and TOBench all score agents inside bounded work loops with tools, runtime checks, and resource limits. The same concern appears in reliability papers, supply-chain risk work, and reports on token budgets.

## Clusters

### End-to-end agent benchmarks
New benchmarks treat agents as workers that must plan, edit, run tools, and recover from mistakes. 1GC-7RC gives agents seven machine-learning tasks on one NVIDIA A100 GPU, with no internet access and 40–120 minute task budgets. AgentKernelArena tests 196 GPU kernel tasks across HIP, Triton, and PyTorch-to-HIP paths, then checks compilation, correctness, speed, and hidden input shapes. TOBench adds multimodal tool use: 100 executable tasks, 27 Model Context Protocol servers, and task-specific verifiers.

The results are mixed in a useful way. Claude Code with Sonnet 4.6 improves over all seven visible 1GC-7RC baselines. AgentKernelArena reports high compilation and correctness on many kernel categories, with mean speedups up to 6.89×, but PyTorch-to-HIP kernels often fail on unseen shapes. TOBench is much harsher: the best model reaches 41.0% task success against a 94.0% human benchmark.

#### Evidence
- [1GC-7RC: One Graphic Card -- Seven Research Challenges! How Good Are AI Agents at Doing Your Job?](../Inbox/2026-05-16--1gc-7rc-one-graphic-card-seven-research-challenges-how-good-are-ai-agents-at-doing-your-job.md): Defines 1GC-7RC tasks, compute limits, and reported Sonnet 4.6 results.
- [AgentKernelArena: Generalization-Aware Benchmarking of GPU Kernel Optimization Agents](../Inbox/2026-05-16--agentkernelarena-generalization-aware-benchmarking-of-gpu-kernel-optimization-agents.md): Defines AgentKernelArena task set, scoring, speedups, and unseen-shape issue.
- [TOBench: A Task-Oriented Omni-Modal Benchmark for Real-World Tool-Using Agents](../Inbox/2026-05-16--tobench-a-task-oriented-omni-modal-benchmark-for-real-world-tool-using-agents.md): Defines TOBench task design and reports model and human success rates.

### Execution feedback and refusal controls
Several papers focus on deciding when code generation is trustworthy enough to use. CodeRefuser samples programs, runs generated tests, clusters outputs, and refuses prompts that look likely to fail. Its calibration target is task-level risk, with the default setting checking whether all three sampled solutions are wrong.

Training-time feedback is also getting more careful. The diffusion-code reinforcement learning study finds that Pylint-style static analysis can be a better reward than unit-test pass rate when most generated programs fail. On DiffuCoder, static checking raises HumanEval from 53.9 to 67.1 and reduces rollout time from 29.3 seconds to 26.5 seconds. Moderate hints help, but high hint ratios can hurt, so the useful signal depends on task difficulty and reward type.

#### Evidence
- [Task Abstention for Large Language Models in Code Generation](../Inbox/2026-05-16--task-abstention-for-large-language-models-in-code-generation.md): Describes CodeRefuser, output clustering, calibration, and precision gains.
- [Beyond Execution: Static-Analysis Rewards and Hint-Conditioned Diffusion RL for Code Generation](../Inbox/2026-05-16--beyond-execution-static-analysis-rewards-and-hint-conditioned-diffusion-rl-for-code-generation.md): Reports static-analysis reward results, rollout-time reduction, and hint effects.

### Traceability and package risk
Agent safety work in this period centers on traceable action, not only safer final answers. The provenance paper argues that tool-using agents need records that show causal contribution, execution traceability, and possible intervention points across design, deployment, and monitoring. Its evidence base is mostly conceptual and cited risk data, but it names a concrete gap: multi-step agent harm can involve developers, tool authors, platform operators, and deployers.

Package hallucination gives the risk a software-supply-chain example. A replication across Claude Sonnet 4.6, Claude Haiku 4.5, GPT-5.4-mini, Gemini 2.5 Pro, and DeepSeek V3.2 finds overall hallucination rates clustered between 4.62% and 6.10%. The most actionable finding is a shared set of 127 nonexistent package names hallucinated by all five models, including 109 PyPI names and 18 npm names.

#### Evidence
- [Responsible Agentic AI Requires Explicit Provenance](../Inbox/2026-05-16--responsible-agentic-ai-requires-explicit-provenance.md): Summarizes the explicit provenance proposal and cited agent-risk evidence.
- [The Range Shrinks, the Threat Remains: Re-evaluating LLM Package Hallucinations on the 2026 Frontier-Model Cohort](../Inbox/2026-05-16--the-range-shrinks-the-threat-remains-re-evaluating-llm-package-hallucinations-on-the-2026-frontier-model-cohort.md): Reports package hallucination rates and shared hallucinated package names.

### Operating cost and agent-native tooling
The practical constraint is no longer only model quality. Token use is becoming a budget line for engineering groups. The Pragmatic Engineer report cites two companies with about 10× token-spend growth in six months, one seed-stage infrastructure company rising from about $200 to about $3,000 per developer per month, and a SaaS company cutting costs 30% by changing the default model.

Tool design is responding at the code-editing layer. ane is an early terminal editor that lets agents read or edit a function, definition, line, or delimiter scope through Language Server Protocol support and headless CLI commands. The project has no benchmark evidence yet, but its design target is clear: reduce full-file reads and broad patches by giving agents narrower code operations.

#### Evidence
- [Token spend breaks budgets – what next?](../Inbox/2026-05-16--token-spend-breaks-budgets-what-next.md): Reports token-spend growth, per-developer costs, and cost-control examples.
- [Ane: CLI editor that uses LSPs to let agents explore/edit code with fewer tokens](../Inbox/2026-05-16--ane-cli-editor-that-uses-lsps-to-let-agents-explore-edit-code-with-fewer-tokens.md): Describes ane's LSP-backed narrow editing commands and lack of quantitative benchmarks.
