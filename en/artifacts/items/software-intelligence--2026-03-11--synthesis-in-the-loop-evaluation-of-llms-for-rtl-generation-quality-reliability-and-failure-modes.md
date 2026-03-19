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
- rtl-generation
- verilog
- llm-evaluation
- hardware-synthesis
- code-generation
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Synthesis-in-the-Loop Evaluation of LLMs for RTL Generation: Quality, Reliability, and Failure Modes

## Summary
This paper proposes a “synthesis-in-the-loop” evaluation framework for RTL generation, using the HQI metric—composed of post-synthesis area, delay, and warnings—to systematically evaluate the real hardware usability of 32 LLMs on 202 Verilog tasks. The main conclusion is that looking only at simulation pass rates significantly overestimates model capability; while frontier models are already approaching expert-level quality, single-run deployment stability and synthesis failure modes remain the main bottlenecks.

## Problem
- Most existing RTL generation evaluations look only at syntax or whether simulation passes, and cannot measure whether the code is **synthesizable** or the resulting **hardware quality** after synthesis.
- For chip design, functional correctness alone is not enough; if area/delay degrades severely, or the design cannot be mapped to gate-level circuits at all, the generated result cannot be used in a real production flow.
- Therefore, a unified evaluation method is needed that covers “syntax → synthesis → functionality → QoR,” avoiding misjudgment of hardware generation capability by software-code evaluation paradigms.

## Approach
- The authors build a staged evaluation pipeline: first checking Verilog syntax (Icarus Verilog), then performing synthesis (Yosys + Nangate45 45nm), and finally running testbenches to verify functional correctness.
- They propose **HQI (Hardware Quality Index)**, ranging from 0 to 100; only designs that pass syntax, synthesis, and functionality all at once receive a score, and quality is computed from **area, delay, and warning count** relative to expert reference designs.
- They evaluate **32 models** on **202 tasks** (from VerilogEval and RTLLM), with **5 independent samples** for each model-task pair, while also reporting complexity-weighted Coverage, Global HQI (best-of-5), and ExpHQI (single-attempt expected quality).
- They design a tool-adjudicated taxonomy of synthesis failures, diagnosing samples that pass parsing but fail at the Yosys stage into nine categories to analyze systematic failure mechanisms across models.
- They additionally re-synthesize across **3 technology libraries** to verify whether model rankings are robust to process variation.

## Results
- In the evaluation of **32 models, 202 tasks, and 5 attempts per task**, the models form a three-tier structure: **Tier 1** has **13** models (Global HQI **>71**), **Tier 2** has **11** (**53–68**), and **Tier 3** has **8** (**<53**).
- The strongest model is **Gemini-3-Pro**, reaching **87.5% Coverage** and **85.1 Global HQI**; it is followed by **GPT-5.4-Pro 81.3**, **Gemini-3-Flash 81.2**, **GPT-5.3-Codex 80.8**, and **GPT-5-Pro 80.5**. The weakest model, **Mistral-Nemo**, achieves only **18.1 Global HQI**; the paper states that the gap in hardware implementation quality between the strongest and weakest is about **4.7×**.
- Looking only at simulation overestimates hardware readiness: across all models, the **best-of-5 pass rate is on average 7.5 points higher than Global HQI**; for example, **GPT-4.1** has **76.7% pass vs. 62.8 HQI** (a gap of **13.9**), and **Gemini-2.0-Flash** has **54.5% pass vs. 39.6 HQI** (a gap of **14.9**).
- There is a clear deployment stability gap: the **difference between best-of-5 and single-attempt expected quality is 3.8–22.1 HQI points**; even within Tier 1, the median gap is **8.2**, indicating that even frontier models often fail to reach their capability ceiling in a single call.
- Out of **32,320** total generations, **195** were genuine synthesis failures; the top three failure modes account for **76.6%**: **late syntax errors: 59 cases (30.0%)**, **undefined module references: 50 cases (25.4%)**, and **non-synthesizable constructs: 41 cases (20.8%)**.
- Failure modes diverge significantly by model type: proprietary models more often “fail late,” with **46%** of their failures being late syntax errors in the elaboration stage, and **synthesis timeout 12%** appearing only in proprietary models; open-weight models more often “fail early,” with **undefined module 40%**, **non-synthesizable 29%**, and **simulation-only system tasks 13%**, pointing to training data biased more toward simulation-grade RTL than synthesis-grade RTL. Another robustness result is that model rankings are almost unchanged across **3 technology libraries**, with **Spearman ρ > 0.99**.

## Link
- [http://arxiv.org/abs/2603.11287v1](http://arxiv.org/abs/2603.11287v1)
