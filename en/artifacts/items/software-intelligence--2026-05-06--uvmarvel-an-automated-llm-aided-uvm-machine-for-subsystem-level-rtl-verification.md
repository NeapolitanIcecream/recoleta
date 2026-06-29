---
source: arxiv
url: https://arxiv.org/abs/2605.04704v2
published_at: '2026-05-06T09:55:36'
authors:
- Junhao Ye
- Dingrong Pan
- Hanyuan Liu
- Yuchen Hu
- Jie Zhou
- Ke Xu
- Xinwei Fang
- Xi Wang
- Nan Guan
- Zhe Jiang
topics:
- rtl-verification
- uvm-automation
- code-intelligence
- llm-agents
- hardware-engineering
- testbench-generation
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# UVMarvel: an Automated LLM-aided UVM Machine for Subsystem-level RTL Verification

## Summary
UVMarvel automates subsystem-level RTL verification by using LLMs to build UVM testbenches and refine stimuli. It claims 95.65% average code coverage and a 4.5-hour run to 90% coverage on industrial-style subsystem benchmarks.

## Problem
- RTL verification consumes nearly 70% of IC front-end effort, and subsystem-level UVM testbench construction still needs expert manual coding.
- Prior LLM and template-based UVM flows work mainly at IP level and struggle with bus timing, inter-IP dependencies, protocol semantics, and long corner-case sequences.
- Initial LLM-generated stimuli can average below 40% coverage because they repeat simple patterns and miss multi-step subsystem behavior.

## Approach
- UVMarvel converts specs and RTL into a five-part IR: module name, interface description, register configuration, timing characteristics, and functional description.
- A Bus Protocol Library supplies UVM skeletons for interfaces, drivers, monitors, and agents across APB, AHB, AXI, P-Channel, and Q-Channel, while the LLM fills DUT-specific fields.
- A Coverage Analyser extracts uncovered and partially covered items from simulator coverage reports and feeds compact targets to the LLMs.
- A Signal Tracker traces uncovered signals through Verilog files to find related statements and controllable top-level I/O paths.
- A Verilog Patcher rebuilds minimal valid RTL slices around those statements, then GPT-4.1, Claude 4.5, and Gemini 2.5 Pro generate or repair new UVM sequences.

## Results
- UVMarvel reports 95.65% average code coverage across six subsystem benchmarks: Watchdog, Pwrctrl, Cordic, IdleControl, LPctrl, and Busremap.
- Per-design code coverage is 98.84% on Watchdog, 93.66% on Pwrctrl, 100% on Cordic, 94.90% on IdleControl, 90.83% on LPctrl, and 95.66% on Busremap.
- Functional coverage is 100% on Watchdog, 90.64% on Pwrctrl, 100% on Cordic, 96.12% on IdleControl, 89.33% on LPctrl, and 98.27% on Busremap.
- The benchmark set covers APB, AHB, AXI, Q-Channel, and P-Channel designs with 3 to 10 modules and about 800 to 3000+ RTL lines per design.
- The paper claims UVMarvel reaches 90% code coverage in 4.5 hours, 20.17x faster than an expert manual flow, excluding the human IR and test-planning phase.

## Link
- [https://arxiv.org/abs/2605.04704v2](https://arxiv.org/abs/2605.04704v2)
