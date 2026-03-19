---
source: arxiv
url: http://arxiv.org/abs/2603.11287v1
published_at: '2026-03-11T20:26:58'
authors:
- Weimin Fu
- Zeng Wang
- Minghao Shao
- Ramesh Karri
- Muhammad Shafique
- Johann Knechtel
- Ozgur Sinanoglu
- Xiaolong Guo
topics:
- llm-evaluation
- rtl-generation
- verilog
- synthesis-in-the-loop
- hardware-quality
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# Synthesis-in-the-Loop Evaluation of LLMs for RTL Generation: Quality, Reliability, and Failure Modes

## Summary
This paper proposes a "synthesis-in-the-loop" evaluation framework for RTL generation, used to measure whether LLM-generated Verilog not only passes tests, but is also truly synthesizable and whether the synthesized hardware quality approaches that of expert designs. Across 202 tasks, 32 models, and 5 samples per problem, the authors find a clear three-tier stratification in hardware-level capability and expose systematic differences in single-shot deployment reliability and failure modes.

## Problem
- Existing RTL generation evaluations mostly focus only on syntax or simulation pass rates, and cannot determine whether code is **synthesizable**, nor whether post-synthesis area, timing, and warnings meet the bar.
- This matters because the real bottleneck in chip RTL development is not just "functional correctness"; designs must also proceed to backend implementation and satisfy area/timing constraints. Relying only on simulation pass rates overestimates the practicality of LLMs for production-grade hardware design.
- Even if generated Verilog passes tests, it may still contain non-synthesizable constructs or be 2–5× worse than expert implementations in area/latency, neither of which traditional software-style evaluation can detect.

## Approach
- The authors evaluate **32 language models** on **202 Verilog tasks** (from VerilogEval and RTLLM), with **5 independent generations** for each model-task pair.
- They use a three-stage scoring pipeline: first **syntactic validity** (Icarus Verilog), then **synthesizability** (Yosys + Nangate45 45nm), and finally **functional correctness** (testbench simulation); failure at any stage gives an HQI of 0.
- They propose the **Hardware Quality Index (HQI)**, which compares designs that pass all three stages against expert references on **area, delay, and warning count** after normalization, yielding a score from 0–100; 100 means matching the expert implementation.
- They use **complexity-weighted Coverage, Global HQI, and Expected HQI** to measure, respectively, whether tasks can be solved, the best-of-5 capability ceiling, and the deployment quality of a single call, thereby explicitly quantifying the "capability-deployment" gap.
- They also construct a **nine-category synthesis failure taxonomy** based on Yosys diagnostics, and resynthesize under two additional technology libraries to verify that rankings are robust across processes.

## Results
- In the evaluation of **32 models, 202 tasks, and 5 samples per task**, the authors find a three-tier capability structure: **13 models** in Tier 1 (Global HQI ≥ 71), **11** in Tier 2 (53–68), and **8** in Tier 3 (<53). The best model is **Gemini-3-Pro**, achieving **87.5% Coverage** and **85.1 Global HQI**.
- Leading models also include **GPT-5.4-Pro (81.3 HQI)**, **Gemini-3-Flash (81.2)**, **GPT-5.3-Codex (80.8)**, and **GPT-5-Pro (80.5)**; the strongest open-weight models, such as **DeepSeek-V3.2 (58.8)** and **Qwen3.5-397B-OSS (58.2)**, trail the proprietary Tier 1 frontier models by about **15–20 HQI points**.
- The paper argues that traditional simulation pass rates **systematically overestimate** hardware usability: across all 32 models, the **best-of-five pass rate is on average 7.5 points higher than Global HQI**. For example, **GPT-4.1** has a pass rate of **76.7%** but a Global HQI of only **62.8** (a gap of **13.9**); **Gemini-2.0-Flash** shows **54.5% vs 39.6** (a gap of **14.9**).
- The gap between single-shot deployment and multi-sample performance is substantial: the **difference between best-of-five and single-attempt is 3.8–22.1 HQI points**; even within Tier 1, the median gap is **8.2 points**. The top model **Gemini-3-Pro** drops from **85.1 Global HQI** to **78.5 Expected HQI**, indicating that even frontier models need multi-sample strategies.
- The failure analysis covers **32,320 generations**, including **195 genuine synthesis failures**. The three main causes account for **76.6%**: **late syntax errors 59 times (30.0%)**, **undefined module references 50 times (25.4%)**, and **non-synthesizable constructs 41 times (20.8%)**. This shows that many failures occur at the real hardware-constraint layer where code can pass parsing but fail synthesis.
- Rankings are highly robust to changes in technology libraries: across Nangate45, IHP SG13G2, and OSU 0.35μm, model ranking correlations reach **Spearman ρ > 0.99**; sensitivity analysis of HQI weights also shows **ρ ≥ 0.997** and a maximum rank shift of **no more than 3 places**. This suggests the evaluation conclusions are not accidental artifacts of one specific scoring detail or technology library.

## Link
- [http://arxiv.org/abs/2603.11287v1](http://arxiv.org/abs/2603.11287v1)
