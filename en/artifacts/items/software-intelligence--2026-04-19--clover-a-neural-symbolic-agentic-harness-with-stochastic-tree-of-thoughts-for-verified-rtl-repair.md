---
source: arxiv
url: http://arxiv.org/abs/2604.17288v1
published_at: '2026-04-19T07:04:49'
authors:
- Zizhang Luo
- Yansong Xu
- Runlin Guo
- Fan Cui
- Kexing Zhou
- Mile Xia
- Hongyuan Hou
- Yuhao Luo
- Yun Liang
topics:
- rtl-repair
- neural-symbolic-agents
- tree-of-thoughts
- hardware-verification
- code-intelligence
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Clover: A Neural-Symbolic Agentic Harness with Stochastic Tree-of-Thoughts for Verified RTL Repair

## Summary
Clover is an automated RTL repair system that combines LLM agents with SMT-based symbolic repair and a search procedure over repair hypotheses. It targets verified hardware bug fixing, where pure template-based repair misses many bugs and pure LLM repair is unreliable on long RTL code and waveform data.

## Problem
- RTL program repair is slow and costly because engineers must inspect code, run simulations, read waveforms, and try patches across many iterations.
- Existing RTL repair methods split into two weak extremes: symbolic systems are precise but limited to a small set of repair templates, while LLM systems are flexible but can lose context, misread low-level traces, and produce inconsistent patches.
- Real RTL bugs often need several repair steps at different abstraction levels, so a single repair strategy does not cover the full space of fixes.

## Approach
- Clover treats RTL repair as a structured search over code states. A main agent proposes bug hypotheses, applies one patch at a time, runs validation, and keeps successful edits so it can perform multi-step repair.
- The system routes work by task type: LLM sub-agents handle code understanding and lint fixing, while SMT-based symbolic repair handles low-level edits that fit repair templates.
- It adds an RTL-specific toolbox with simulator access, a VCD trace viewer, a language server for code navigation, Verilator, and a custom linter so agents can inspect designs and test candidate fixes.
- Its main search method is stochastic tree-of-thoughts: each hypothesis and dialogue state becomes a node in a search tree, and Clover samples which node to expand using a heuristic based on passed testbenches, number of queries, compile errors, token use, and patch count.
- Clover extends prior symbolic RTL repair with an added cycle-shift template for temporal bugs and lets the agent choose when to invoke each template, then converts solver output into source-level patch actions.

## Results
- On the RTL-Repair benchmark, Clover fixes **96.8%** of bugs within a fixed time limit.
- The paper claims this covers **94% more bugs** than traditional baselines and **63% more bugs** than LLM-based baselines.
- Clover reports an average **pass@1 of 87.5%**, which the authors use as evidence that the search procedure improves reliability, not only peak success rate.
- The excerpt names the benchmark as **RTL-Repair** and compares against both traditional symbolic/template methods and prior LLM-based RTL repair systems, but it does not give the full per-baseline table in the provided text.
- The paper also claims broader symbolic applicability by extending the repair flow to **SystemVerilog** and adding a **cycle-shift** repair template, though the excerpt does not include an isolated ablation number for those additions.

## Link
- [http://arxiv.org/abs/2604.17288v1](http://arxiv.org/abs/2604.17288v1)
