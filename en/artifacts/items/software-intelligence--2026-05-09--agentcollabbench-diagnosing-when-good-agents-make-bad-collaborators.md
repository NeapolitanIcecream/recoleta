---
source: arxiv
url: https://arxiv.org/abs/2605.08647v1
published_at: '2026-05-09T03:35:09'
authors:
- Aritra Mazumder
- Shubhashis Roy Dipta
- Nusrat Jahan Lia
- Tanzila Khan
- Kainat Raisa Hossain
- Nehaa Shri
- Shubhrangshu Debsarkar
- Humayra Tasnim
- Gour Gupal Talukder Shawon
- Debjoty Mitra
- Sumaiya Ahmed Rani
- Al Jami Islam Anik
- Al Nafeu Khan
topics:
- multi-agent-systems
- software-engineering-agents
- agent-evaluation
- llm-reliability
- collaboration-failures
- benchmarking
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# AgentCollabBench: Diagnosing When Good Agents Make Bad Collaborators

## Summary
AgentCollabBench tests whether multi-agent LLM pipelines preserve constraints, facts, private context, and marked information while agents pass messages to each other. The paper claims topology can create reliability failures even when each model can produce valid-looking final outputs.

## Problem
- Multi-agent software, DevOps, and data-engineering workflows can lose a hard constraint or spread a false premise while still returning a complete final artifact.
- Outcome-only benchmarks miss process failures such as constraint loss, false-belief spread, cross-task leakage, and multi-hop information loss.
- This matters for deployed agent teams because a valid Kubernetes manifest, code patch, or data pipeline can omit a required security or compliance condition.

## Approach
- The benchmark contains 900 human-validated tasks across software engineering, DevOps, and data engineering.
- Each task targets one of four risks: Instruction Decay Rate (IDR), Radioactive Tracer Durability (RTD), Consensus Pollution Rate (CPR), and Cross-task Leakage Containment (CLC).
- It varies five communication topologies: linear chain, branching tree, converging DAG, fully connected, and custom graph.
- The method injects controlled artifacts such as hard constraints, unique tracer strings, false facts, or private strings, then checks whether they survive, spread, or leak.
- RTD and CLC use deterministic string checks; IDR and CPR use LLM judges validated against humans with Cohen's kappa >= 0.69 and 84.4-89.3% agreement.

## Results
- On 900 tasks, Qwen-3.5-35B-A3B had the best tracer durability and instruction stability: RTD 94.0% and IDR 0.9%.
- GPT 4.1 mini had the lowest leakage and false-belief spread: CLC 2.6% and CPR 17.7%, while its RTD was 80.3%.
- Llama 3.1 8B Instruct had the weakest profile on three metrics: IDR 10.1%, CPR 40.3%, and RTD 62.6%; the introduction also reports cross-task leakage at 4.9%.
- Qwen still spread injected false beliefs in 20.7% of downstream responses and had CLC 4.7%, so strong performance on one risk did not cover all risks.
- Topology explained 7-40% of the variance in multi-hop information survival, with converging DAG nodes losing minority-branch constraints more often than linear chains.
- Perturbation tests moved in the expected directions: IDR rho 0.211, CPR rho 0.411, CLC rho 0.146, and RTD rho -0.313 as topology siloing increased.

## Link
- [https://arxiv.org/abs/2605.08647v1](https://arxiv.org/abs/2605.08647v1)
