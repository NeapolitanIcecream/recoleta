---
source: arxiv
url: https://arxiv.org/abs/2606.31725v1
published_at: '2026-06-30T14:26:46'
authors:
- Jack Le
- Anh H. N. Nguyen
- Tien N. Nguyen
topics:
- code-intelligence
- llm-evaluation
- obfuscated-code
- program-comprehension
- human-ai-alignment
- software-security
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Do Machines Struggle Where Humans Do? LLM and Human Comprehension of Obfuscated Code

## Summary
This paper tests whether LLMs find obfuscated code hard in the same places humans do. Reasoning-tuned models track human task difficulty, while coder and instruction-tuned models show weak alignment.

## Problem
- Code obfuscation preserves behavior while changing names and control flow, so it can test whether a model follows program logic or relies on surface cues.
- Standard code benchmarks can hide brittle code understanding because familiar identifiers, idioms, and control-flow shape may carry much of the answer.
- This matters for code intelligence and software security: an agent that misreads obfuscated code may give wrong answers in auditing, reverse engineering, malware analysis, or protected-code maintenance.

## Approach
- The study reuses Nguyen et al.'s human dataset: 50 undergraduate programmers, 20 function-level output-prediction tasks, Python and JavaScript, and five obfuscation tiers from L0 to L3.
- It adds Dataset B with 250 snippets from HumanEval-X, CruxEval-X, and LeetCode, each instantiated across the same five tiers.
- It evaluates Llama, Qwen, DeepSeek, Phi, SmolLM, CodeLlama, and DeepSeek-Coder variants on exact output prediction.
- Obfuscation tiers include identifier renaming, adversarial renaming, control-flow flattening, and combined renaming plus control-flow flattening.
- The analysis uses Schulte's Block Model to locate failures at atom, block, relational, and macro levels, with metrics for accuracy, chain-of-thought length, dispatcher complexity, and high-confidence wrong answers.

## Results
- On Dataset A, DS-R1-Qwen-7B is the strongest model: 63.8% accuracy at L0, 64.2% at L1, 51.8% at L1b, 57.0% at L2, and 56.2% at L3.
- Human accuracy across all participants drops from 40.46% at L0 to 31.09% at L3. Beginners drop from 34.21% to 23.08%, and intermediates drop from 45.10% to 33.33%.
- Reasoning-tuned models align with human task difficulty: Spearman correlations are Qwen3-0.6B ρ=0.30, Phi-4 Mini ρ=0.47, SmolLM3-3B ρ=0.36, and DS-R1-Qwen-7B ρ=0.37, all with p≤0.003.
- Coder and instruction-tuned models show near-zero human alignment: Llama-3.1-8B ρ=0.08, CodeLlama-7B ρ=0.02, and DeepSeek-Coder-6.7B ρ=0.10.
- Control-flow flattening hurts accuracy as dispatcher complexity rises: Python while-if state count correlates with accuracy at r=-0.196 with q=3.08×10^-23; JavaScript dispatch-call references have r=-0.130 with q=2.76×10^-7.
- Low token limits strongly reduce strong reasoning-model performance, with OR=12.5, 95% CI [6.4, 24.2], p<0.001 for the reported comparison.

## Link
- [https://arxiv.org/abs/2606.31725v1](https://arxiv.org/abs/2606.31725v1)
