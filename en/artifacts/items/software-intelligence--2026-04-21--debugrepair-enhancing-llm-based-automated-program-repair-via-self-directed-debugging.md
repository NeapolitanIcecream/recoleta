---
source: arxiv
url: http://arxiv.org/abs/2604.19305v1
published_at: '2026-04-21T10:11:59'
authors:
- Linhao Wu
- Yifei Pei
- Zhen Yang
- Kainan Li
- Zhonghang Lu
- Hao Tan
- Xiran Lyu
- Jia Li
- Yizhou Chen
- Pengyu Xue
- Kunwu Zheng
- Dan Hao
topics:
- automated-program-repair
- llm-debugging
- code-intelligence
- self-directed-debugging
- software-engineering
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# DebugRepair: Enhancing LLM-Based Automated Program Repair via Self-Directed Debugging

## Summary
DebugRepair improves LLM-based automated program repair by adding a debugging step that collects runtime state, instead of relying only on failing test outcomes and stack traces. The paper reports state-of-the-art repair results across Java and Python benchmarks and shows gains across several backbone LLMs.

## Problem
- Existing feedback-based LLM repair methods mainly use outcome-level signals such as failed tests and stack traces, which show the symptom of a bug but often hide the runtime state that caused it.
- Without intermediate execution evidence, the model can guess the wrong cause and produce patches that only mask the failure instead of fixing the bug.
- This matters because automated program repair is only useful when it can find correct patches for real bugs, especially on harder cases where static code plus test outcomes are not enough.

## Approach
- DebugRepair first applies **test semantic purification**: it slices the failing test to keep the minimal failure-triggering statements and required class-level dependencies, which reduces irrelevant context and noisy debug logs.
- It then performs **simulated instrumentation**: the LLM predicts useful variables and locations to inspect, inserts print-style debugging statements, and executes the instrumented code to collect intermediate runtime traces.
- To keep instrumentation safe, the system checks that the instrumented function matches the original logic after removing debug prints/comments and also checks compilation; if LLM-inserted instrumentation fails, a rule-based AST instrumentation fallback is used.
- Finally, **debugging-driven conversational repair** runs in an iterative hierarchy: an outer loop manages instrumentation and trace collection, while an inner loop refines patches using prior repair attempts plus newly observed runtime states until tests pass or the budget ends.

## Results
- On **Defects4J** with **GPT-3.5**, DebugRepair correctly fixes **224 bugs**, with an average **26.2%** improvement over state-of-the-art LLM-based baselines.
- On **Defects4J** with **DeepSeek-V3**, DebugRepair correctly fixes **295 bugs**, which is **59 more** than the second-best baseline.
- Across **five additional backbone LLMs** from different families and sizes, DebugRepair improves repair performance by **51.3% on average** over each model's vanilla setting.
- The evaluation covers **three benchmarks** across **two languages**: **Defects4J (v1.2 and v2.0)**, **QuixBugs**, and **HumanEval-Java**, with comparisons against **15 representative approaches**.
- The paper states that ablation studies show all major components help, especially test purification and simulated debugging, but the excerpt does not provide detailed ablation numbers.

## Link
- [http://arxiv.org/abs/2604.19305v1](http://arxiv.org/abs/2604.19305v1)
