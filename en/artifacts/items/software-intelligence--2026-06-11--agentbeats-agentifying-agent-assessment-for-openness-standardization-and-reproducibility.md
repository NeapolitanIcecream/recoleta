---
source: arxiv
url: https://arxiv.org/abs/2606.13608v1
published_at: '2026-06-11T17:23:54'
authors:
- Xiaoyuan Liu
- Jianhong Tu
- Yuqi Chen
- Siyuan Xie
- Sihan Ren
- Tianneng Shi
- Gal Gantar
- Evan Sandoval
- Donghyun Lee
- Daniel Miao
- Peter J. Gilbert
- Nick Hynes
- Mauro Staver
- Warren He
- David Marn
- Andrew Low
- Xi Zhang
- Elron Bandel
- Michal Shmueli-Scheuer
- Siva Reddy
- Alexandre Drouin
- Alexandre Lacoste
- Ramayya Krishnan
- Elham Tabassi
- Yu Su
- Victor Barres
- Chenguang Wang
- Wenbo Guo
- Dawn Song
topics:
- agent-evaluation
- benchmark-standardization
- multi-agent-systems
- a2a
- mcp
- reproducibility
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# AgentBeats: Agentifying Agent Assessment for Openness, Standardization, and Reproducibility

## Summary
AgentBeats proposes Agentified Agent Assessment (AAA), a way to evaluate agents by turning the benchmark into a judge agent that talks to subject agents through A2A and MCP. It targets the mismatch between fixed benchmark harnesses and diverse real agents, and claims this setup improves openness, standardization, interoperability, and reproducibility.

## Problem
- Agent evaluation is fragmented: each benchmark uses its own harness and assumptions about inputs, tools, and control.
- Integrating many agents with many benchmarks creates N x M bespoke work, which limits coverage and fairness.
- Benchmark setups often differ from production deployment, so reported scores can miss real-world behavior and risk.

## Approach
- AAA treats the benchmark itself as an agent that manages tasks, tools, scoring, and reporting.
- The judge agent and subject agents communicate through A2A for task management and MCP for tool access, so the benchmark no longer needs a custom interface for each agent.
- The benchmark logic can be internalized in two ways: programmatic internalization, which hard-codes the original evaluation flow, and semantic internalization, which expresses it in natural language.
- AgentBeats instantiates AAA with five operation modes to fit openness, privacy, and reproducibility constraints.
- The workflow has three roles: a delegator that starts the assessment, a judge agent that runs the benchmark, and one or more subject agents that are evaluated.

## Results
- The paper reports a five-month open competition with 298 judge agents across 12 categories and 467 subject agents from independent participants.
- That competition agentified dozens of benchmarks spanning coding, web browsing, healthcare, and multi-agent games.
- In a coding case study, agentified evaluation matched the public record where comparisons were possible and exposed head-to-head results that were missing before.
- The authors also report a co-adaptation effect between models and their native harnesses.
- No standard benchmark metric table is provided in the excerpt, so the strongest quantitative claims are the scale of the deployment study and the claim that fidelity was preserved.

## Link
- [https://arxiv.org/abs/2606.13608v1](https://arxiv.org/abs/2606.13608v1)
