---
source: arxiv
url: http://arxiv.org/abs/2604.09860v2
published_at: '2026-04-10T19:42:21'
authors:
- Xuning Yang
- Rishit Dagli
- Alex Zook
- Hugo Hadfield
- Ankit Goyal
- Stan Birchfield
- Fabio Ramos
- Jonathan Tremblay
topics:
- robot-benchmark
- vision-language-action
- sim2real
- generalization-evaluation
- high-fidelity-simulation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# RoboLab: A High-Fidelity Simulation Benchmark for Analysis of Task Generalist Policies

## Summary
RoboLab is a high-fidelity simulation benchmark for testing whether real-world-trained robot policies actually generalize to new tasks and domains. It builds held-out simulated tasks, scores failure modes and motion quality, and shows that current vision-language-action policies perform poorly on this kind of out-of-domain evaluation.

## Problem
- Existing robot benchmarks often train and test in overlapping simulated domains, so success rates can saturate and hide weak generalization.
- Real-world evaluation is expensive and slow, while many simulators are either too low-fidelity for real-world policies or too costly to extend scene by scene.
- Binary success alone misses useful failure signals such as wrong-object grasps, drops, collisions, and sensitivity to camera or scene changes.

## Approach
- The paper introduces RoboLab, a simulation platform in IsaacLab/Isaac Sim that generates photorealistic scenes and language-conditioned tasks with human-written or LLM-assisted workflows.
- It defines RoboLab-120, a benchmark of 120 human-verified tasks across three competency axes: visual, procedural, and relational, each with simple, moderate, and complex levels.
- Policies are trained only on real-world data such as DROID and then evaluated in held-out simulation, which separates training from test domains.
- Evaluation goes beyond success rate with graded task scores, logged failure events, trajectory metrics such as SPARC, speed, and path length, plus sensitivity analysis using simulation-based inference to estimate which scene variables drive success or failure.
- The generation pipeline scales scene and task creation: the paper reports over 800 generated scenarios and evaluates 812 generated tasks across 59 scenes for instruction-condition alignment and feasibility.

## Results
- On RoboLab-120, overall performance is low. Table I reports overall success of **23.3%** for **π0.5**, **15.7%** for **π0-FAST**, **5.2%** for **π0**, **2.0%** for **GR00T N1.6**, and **1.5%** for **PaliGemma**.
- The paper also states the best policy reaches **31.9% success** overall, while the introduction gives an approximate figure of **~30%** for **π0.5**. The excerpt contains this inconsistency, but both numbers support the same claim: strong current models fail on most held-out tasks.
- For **π0.5**, success by difficulty is **26.3% / 23.2% / 11.7%** on **simple / moderate / complex** tasks.
- For **π0.5**, relational subtasks are much easier than most other axes: **56.2%** overall relational success in Table I, with text-reported breakdowns of **76.0%** on conjunction, **60.0%** on counting, and **23.9%** on spatial relations.
- For **π0.5**, visual grounding remains weak: the text reports **35.0%** for size, **30.0%** for color, and **21.5%** for semantics. Procedural skills are also weak: **53.3%** on reorientation, **20.0%** on affordances, and **16.0%** on stacking.
- Language robustness is brittle. Table IV shows overall success across language specificity levels for **π0.5** at **16.8%**, **23.3%**, and **25.8%**; for **π0-FAST** at **9.7%**, **15.7%**, and **15.2%**; and for **π0** at **3.4%**, **5.2%**, and **6.5%**.
- Scene complexity hurts performance. In one ablation, **π0.5** drops from **70%** success with **1** target object to **30%** with **2** and **20%** with **3** on a canned-food packing task.
- Instruction wording can flip outcomes in the same scene. Examples for **π0.5** include **80%** on "Put the white mugs in the grey bin" versus **0%** on "Put away mugs," and **50%** on "Take all the bananas out of the grey bin and put it on the table" versus **10%** on "Empty the grey bin."
- The task-generation pipeline also has quantitative validation: across **812** generated tasks in **59** scenes, the paper reports **0.91** instruction-condition alignment, **0.96** clarity, **0.92** feasibility, **0.95** semantic match, **76%** fully aligned tasks, about **1%** misaligned, and **88%** object coverage.
- On selected real-vs-sim comparisons over **6 simple tasks**, Table V reports real success rates of **79.5**, **34.1**, **63.2**, and **0.0** versus simulated rates of **74.0**, **42.0**, **18.0**, and **4.0** for the shown policies, supporting the claim that simulation can be a useful but imperfect proxy for real-world behavior.

## Link
- [http://arxiv.org/abs/2604.09860v2](http://arxiv.org/abs/2604.09860v2)
