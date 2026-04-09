---
kind: trend
trend_doc_id: 80
granularity: day
period_start: '2026-04-01T00:00:00'
period_end: '2026-04-02T00:00:00'
topics:
- software-agents
- coding-llms
- evaluation
- security
- gpu-kernels
run_id: materialize-outputs
aliases:
- recoleta-trend-80
tags:
- recoleta/trend
- topic/software-agents
- topic/coding-llms
- topic/evaluation
- topic/security
- topic/gpu-kernels
language_code: en
pass_output_id: 8
pass_kind: trend_synthesis
---

# Software-agent research is getting stricter about signal, evidence, and risk

## Overview
The period’s strongest theme is tighter control over software agents: cleaner traces for training, better logs for evaluation, and harder tests for what agents do in real repositories and real workspaces. The evidence is more practical than headline-driven. STITCH reports large gains from fewer, higher-value trajectories, while GitHub-scale and security studies put long-term code churn and prompt-injection risk in the foreground.

## Clusters

### Selective traces beat raw volume in coding agents
Training data quality is the clearest lever in this period’s agent work. STITCH filters long software-agent traces down to decision-critical segments, then fine-tunes on that smaller set. The reported gains are large: up to 63.16% relative improvement on SWE-bench Verified, 43.75% on Multi-SWE-bench Java with CodeArts Agent, and a 61.31% compilation pass rate on HarmonyOS ArkTS with less than 1K training trajectories. In parallel, Gentoo shows the same preference for structured signal at inference time. Its agent writes target-specific fuzz generators that beat human-written generators on 6 of 7 Java benchmarks, with average coverage gains of 11% to 21%. Coverage-guided mutation adds under 3% for agent-written generators in typical cases, which suggests the value is in encoding the right constraints early, not in spraying more random search later.

#### Evidence
- [Yet Even Less Is Even Better For Agentic, Reasoning, and Coding LLMs](../Inbox/2026-04-01--yet-even-less-is-even-better-for-agentic-reasoning-and-coding-llms.md): STITCH and SandForge results on SWE-bench, Java, and ArkTS with fewer trajectories.
- [Fuzzing with Agents? Generators Are All You Need](../Inbox/2026-04-01--fuzzing-with-agents-generators-are-all-you-need.md): Gentoo results on branch coverage and limited benefit from coverage-guided mutation.

### Evaluation now cares about reproducibility and code survival
Software-agent evaluation is getting closer to real use. One paper reviews 18 recent software engineering studies and finds only 1 compared against a relevant agentic baseline. It argues for publishing exact model versions, prompts, temperatures, and Thought-Action-Result logs so failures can be inspected instead of hidden behind final scores. Another paper leaves the benchmark sandbox and studies 111,969 real GitHub pull requests across Codex, Claude Code, Copilot, Jules, and Devin. The main result is uncomfortable but useful: agent-authored code shows higher later churn than human-authored code. The excerpt does not include the exact churn gap, but the signal is strong enough to put maintainability beside task completion as a first-class metric.

#### Evidence
- [Reproducible, Explainable, and Effective Evaluations of Agentic AI for Software Engineering](../Inbox/2026-04-01--reproducible-explainable-and-effective-evaluations-of-agentic-ai-for-software-engineering.md): Review of 18 SE agent papers and recommendation to publish TAR traces and exact settings.
- [Investigating Autonomous Agent Contributions in the Wild: Activity Patterns and Code Change over Time](../Inbox/2026-04-01--investigating-autonomous-agent-contributions-in-the-wild-activity-patterns-and-code-change-over-time.md): Large-scale GitHub study finding higher later churn for agent-authored code.

### Agent security is about scaffolds and exposed code, not model labels alone
Security evidence in this window is concrete and operational. ClawSafety tests prompt injection in high-privilege personal agents across 120 scenarios and 2,520 sandboxed trials. On OpenClaw, attack success ranges from 40.0% for Claude Sonnet 4.6 to 75.0% for GPT-5.1, and skill-file injection is the strongest vector on average at 69.4%. Scaffold choice also changes outcomes for the same model. A separate case study on Claude Code argues that shipping minified JavaScript does not hide prompts or product logic once LLMs can read and reorganize the bundle. The author reports extracting 147,992 strings from a 13MB CLI bundle in 1.47 seconds, including system prompts, telemetry events, and environment variables. Taken together, the lesson is simple: agent safety depends on the full stack, and client-side code exposure is easier to exploit when models can reverse engineer structure quickly.

#### Evidence
- [ClawSafety: "Safe" LLMs, Unsafe Agents](../Inbox/2026-04-01--clawsafety-safe-llms-unsafe-agents.md): Prompt-injection benchmark with model and scaffold-dependent attack success rates.
- [Obfuscation is not security – AI can deobfuscate any minified JavaScript code](../Inbox/2026-04-01--obfuscation-is-not-security-ai-can-deobfuscate-any-minified-javascript-code.md): Case study on AI-assisted deobfuscation of minified JavaScript and exposed artifacts.

### GPU kernel agents can optimize niches, with uneven wins
LLM code generation is also pushing into lower-level performance work, but the results are mixed. CuTeGen uses a compile-test-debug-optimize loop to write GPU kernels in NVIDIA’s CuTe layer. On KernelBench Level-1, it reports a 1.70x average speedup over PyTorch reference implementations for activation kernels, with 3.45x on Softsign and 2.45x on Swish. Matrix multiplication is less consistent: the system beats the cuBLAS-based reference on Square MatMul at 1.16x and on diagonal-matrix matmul at 17.66x, but several other matmul cases stay below baseline, including 0.67x on Standard MatMul and 0.43x on 3D Tensor MatMul. This looks promising for iterative kernel repair and tuning, but not yet like a general replacement for expert libraries.

#### Evidence
- [CuTeGen: An LLM-Based Agentic Framework for Generation and Optimization of High-Performance GPU Kernels using CuTe](../Inbox/2026-04-01--cutegen-an-llm-based-agentic-framework-for-generation-and-optimization-of-high-performance-gpu-kernels-using-cute.md): CuTeGen benchmark results across activation and matrix multiplication kernels.
