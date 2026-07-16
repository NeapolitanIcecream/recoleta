---
kind: trend
trend_doc_id: 793
granularity: day
period_start: '2026-05-01T00:00:00'
period_end: '2026-05-02T00:00:00'
topics:
- AI coding agents
- software engineering
- reward models
- agent orchestration
- reproducibility
- GPU serving
- developer tooling
run_id: materialize-outputs
aliases:
- recoleta-trend-793
tags:
- recoleta/trend
- topic/ai-coding-agents
- topic/software-engineering
- topic/reward-models
- topic/agent-orchestration
- topic/reproducibility
- topic/gpu-serving
- topic/developer-tooling
language_code: en
pass_output_id: 122
pass_kind: trend_synthesis
---

# AI coding agents are being judged by controls, traces, and full-task cost

## Overview
The day’s strongest work treats AI coding as a governed engineering process. AutoMat tests scientific reproducibility, SAGA measures full agent latency, and RECAP records real prompt-to-edit traces. The common demand is concrete evidence before trusting generated code or agent workflows.

## Findings

### Agent output needs specs, traces, and reproducibility checks
Several papers put the inspection layer around AI coding work under pressure. The specification-governance paper ties AI coding gains to review load, context limits, and testable specs. It cites positive task-level studies, then also reports evidence where experienced developers slowed down on mature codebases and delivery stability fell with higher AI adoption.

AutoMat gives the hardest empirical warning. The best tested coding-agent setting reproduced 54.1% of 85 computational materials-science claims. Paper-only reproduction had near-zero success across systems, which points to missing procedures, domain tools, and fragile execution as current failure points.

RECAP attacks the measurement problem inside the editor. It records Copilot chat, shadow git commits, and fine-grained edits in VS Code. In one course deployment, it captured 2,034 prompts and 8,239 commits, making repeated error loops and AI edit share visible at session level.

#### Sources
- [The Productivity-Reliability Paradox: Specification-Driven Governance for AI-Augmented Software Development](../Inbox/2026-05-01--the-productivity-reliability-paradox-specification-driven-governance-for-ai-augmented-software-development.md): Summarizes specification-driven governance, mixed productivity evidence, and reliability risks.
- [Can Coding Agents Reproduce Findings in Computational Materials Science?](../Inbox/2026-05-01--can-coding-agents-reproduce-findings-in-computational-materials-science.md): Reports AutoMat's 85-claim reproducibility benchmark and success rates.
- [RECAP: An End-to-End Platform for Capturing, Replaying, and Analyzing AI-Assisted Programming Interactions](../Inbox/2026-05-01--recap-an-end-to-end-platform-for-capturing-replaying-and-analyzing-ai-assisted-programming-interactions.md): Describes RECAP's prompt-to-edit capture method and deployment measurements.

### Code reward research is testing whether denser signals help
The reward story is cautious. The pass-rate reward study tests reinforcement learning (RL) for code generation with DeepSeek-R1-Distill-Qwen-7B, Qwen3-4B, and Qwen2.5-7B-Instruct. Dense partial-credit feedback did not improve final pass@k over binary pass-all-tests rewards. On Qwen3-4B with GRPO, binary reward beat pass-rate reward on average pass@1, 46.4% versus 44.2%, and on pass@16, 59.1% versus 56.8%.

Themis broadens what a code reward model should score. It builds a benchmark with about 8.9k pairwise preferences across eight languages and five criteria: correctness, runtime, memory, maintainability, and security. The paper’s numeric model gains are not in the excerpt, so the grounded contribution is the benchmark, training data, and multi-criteria setup.

#### Sources
- [Exploring Pass-Rate Reward in Reinforcement Learning for Code Generation](../Inbox/2026-05-01--exploring-pass-rate-reward-in-reinforcement-learning-for-code-generation.md): Compares pass-rate and binary rewards across models, algorithms, and pass@k metrics.
- [Themis: Training Robust Multilingual Code Reward Models for Flexible Multi-Criteria Scoring](../Inbox/2026-05-01--themis-training-robust-multilingual-code-reward-models-for-flexible-multi-criteria-scoring.md): Describes Themis-CodeRewardBench, preference data, languages, and scoring criteria.

### Agent orchestration is becoming a systems problem
SAGA shows that serving an agent is different from serving isolated LLM calls. Agent tasks often make 10 to 100 chained calls with tool gaps in between. SAGA schedules the whole workflow, preserves reusable key-value cache across tool calls, and routes later steps back to the same worker. On 64 A100 GPUs, it reduced task completion time by 1.73x on SWE-bench and 1.55x on WebArena versus vLLM with Automatic Prefix Caching.

A separate position paper makes a control-layer argument for Bayesian decision rules. It gives no experiments, so its value is conceptual: the orchestration layer can track task uncertainty, agent reliability, cost, and stopping decisions without making the language model itself Bayesian.

#### Sources
- [SAGA: Workflow-Atomic Scheduling for AI Agent Inference on GPU Clusters](../Inbox/2026-05-01--saga-workflow-atomic-scheduling-for-ai-agent-inference-on-gpu-clusters.md): Reports SAGA's workflow-level scheduler, KV-cache reuse, latency gains, and throughput tradeoff.
- [Position: agentic AI orchestration should be Bayes-consistent](../Inbox/2026-05-01--position-agentic-ai-orchestration-should-be-bayes-consistent.md): Summarizes the Bayes-consistent orchestration proposal and its lack of empirical results.
