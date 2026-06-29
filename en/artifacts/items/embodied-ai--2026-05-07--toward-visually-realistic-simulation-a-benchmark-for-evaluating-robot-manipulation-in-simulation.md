---
source: arxiv
url: https://arxiv.org/abs/2605.06311v1
published_at: '2026-05-07T14:13:05'
authors:
- Yixin Zhu
- Zixiong Wang
- Jian Yang
- Jin Xie
- Jingyi Yu
- Jiayuan Gu
- Beibei Wang
topics:
- robot-manipulation
- simulation-benchmark
- sim2real
- vision-language-action
- pbr-assets
- visual-realism
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Toward Visually Realistic Simulation: A Benchmark for Evaluating Robot Manipulation in Simulation

## Summary
VISER is a visually realistic simulation benchmark for robot manipulation that targets the visual sim-to-real gap in VLA evaluation. It reports stronger agreement with real-world policy results by adding PBR materials, specular cues, and soft shadows.

## Problem
- Existing robot manipulation benchmarks often simplify lighting and materials, so simulated VLA success can disagree with real-world success.
- The paper identifies specular highlights and contact shadows as visual cues that affect geometry reasoning and spatial grounding.
- This matters because real robot evaluation is costly, and simulation is useful only when it predicts real-world policy behavior.

## Approach
- VISER builds a 3D asset set with 1,049 objects across 319 categories and 12 supercategories, using clean PBR materials.
- The asset pipeline renders each object from 32 views, uses an MLLM to identify material-aware parts, retrieves matching materials, uses SAM3 for part masks, then projects masks into UV space for PBR texturing.
- A second MLLM checks mask quality and adds prompts for re-segmentation when masks miss object parts.
- Scene layouts are generated from descriptions or images by extracting objects, building a scene graph, estimating 2D table coordinates, and instantiating objects in simulation.
- The benchmark includes 14 curated tasks, 8 reconstructed real-world tasks, generated tasks, basic skills such as pick up and put in, and long-horizon tasks scored with Qwen-3-VL Agent Score.

## Results
- VISER reports an average Pearson correlation coefficient of 0.92 between simulation and real-world performance across policies.
- In sim-to-real correlation tests, Octo reaches r=0.9988 in VISER versus r=0.8860 in SimplerEnv; OpenVLA reaches r=0.8496 in VISER versus r=-0.2712 in SimplerEnv.
- Specular highlights improve the eggplant-in-pot step from 10% success without specular to 90% with specular, compared with 100% in the real world; grasping the eggplant stays at 100% in all three settings.
- Soft shadows improve put-spoon-on-towel success to 49%, compared with 12% without shadows, 0% with hard shadows, and 42% in the real world.
- Asset quality scores are higher than RoboTwin and ManiTwin: VISER gets VLM-S 55.35 and CLIP-S 25.20, versus RoboTwin 45.66/21.35 and ManiTwin 38.27/20.75.
- The benchmark table reports VISER as 1,049 assets, 319 asset categories, and 22 plus generated tasks, with soft shadows, specular rendering, clean PBR materials, and validated sim-to-real correlation.

## Link
- [https://arxiv.org/abs/2605.06311v1](https://arxiv.org/abs/2605.06311v1)
