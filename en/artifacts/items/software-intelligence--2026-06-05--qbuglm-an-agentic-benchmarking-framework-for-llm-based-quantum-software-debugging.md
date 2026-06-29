---
source: arxiv
url: https://arxiv.org/abs/2606.07314v1
published_at: '2026-06-05T14:34:46'
authors:
- An B. B. Pham
- Hoa T. Nguyen
- Muhammad Usman
topics:
- quantum-software-debugging
- llm-agents
- code-repair
- openqasm
- benchmarking
- multi-agent-systems
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# QBugLM: An Agentic Benchmarking Framework for LLM-based Quantum Software Debugging

## Summary
QBugLM is a multi-agent benchmarking system for testing whether LLMs can find and repair bugs in OpenQASM 3.0 quantum programs. Its main finding is that feedback retries raise repair success sharply, while simple structured prompts beat CoT and ReAct in the reported case study.

## Problem
- Quantum bugs can produce wrong answers without runtime errors, so syntax checks and standard debugging often miss defects that change circuit behavior.
- Prior LLM quantum-code benchmarks mainly test code generation or SDK-specific code; this paper tests detection and repair on SDK-agnostic OpenQASM 3.0.
- This matters because automated quantum coding agents need to find, fix, and validate programs without human hints.

## Approach
- QBugGen injects one controlled bug into each valid MQT Bench OpenQASM 3.0 circuit using four bug classes: deprecated syntax, structural circuit errors, gate redundancy, and semantic deviation.
- QBugFind asks one LLM agent to report the fault line and bug class. QBugFix asks another LLM agent to edit the program.
- QBugCheck runs the reference and fixed programs on a noiseless Qiskit Aer simulator, compares output distributions with total variation distance at εδ = 0.05, and requires gate count tolerance εg = 0.
- The case study uses five 5-qubit circuits: dj, grover, bv, ghz, and wstate. It tests Claude Sonnet 4.6 and Qwen3 Coder Next with structured, CoT, and ReAct prompting.
- Each configuration allows K = 3 attempts, meaning one initial attempt plus two retries, and validation uses 1,024 shots.

## Results
- On the Bernstein-Vazirani circuit, structured prompting gives the best Pass@1: Claude Sonnet 4.6 reaches 97% and Qwen3 Coder Next reaches 95%. CoT gives 90% for Claude and 45% for Qwen3; ReAct gives 95% for Claude and 63% for Qwen3.
- The paper reports that one retry raises Pass@1 from below 25% to above 80%, making feedback the largest measured factor in repair success.
- Without retries on BV with structured prompting, Qwen3 reaches 20% Pass@1 on semantic deviation, deprecated syntax, and gate overuse; Claude reaches 0% on those three categories. Both models reach 60% on structural errors.
- After two retries, Claude reaches 100% on semantic deviation, deprecated syntax, and gate overuse, but 80% on structural errors. Qwen3 reaches 100% on structural errors, deprecated syntax, and gate overuse, but 92% on semantic deviation. The paper also reports Pass@5 = 100% across all categories after two retries.
- Qwen3 is cheaper than Claude on structural errors, deprecated syntax, and gate overuse: $0.042, $0.036, and $0.061 per mutant versus $0.202, $0.327, and $0.496, which are 4.8x, 9.1x, and 8.1x cost reductions.
- Qwen3 is 1.5x to 4.6x faster on those same categories; for structural errors, it averages 28 seconds per mutant versus 127.6 seconds for Claude. On semantic deviation, Qwen3 uses about 350,000 tokens versus 91,000 for Claude and reaches 92% Pass@1 versus Claude’s 100%.

## Link
- [https://arxiv.org/abs/2606.07314v1](https://arxiv.org/abs/2606.07314v1)
