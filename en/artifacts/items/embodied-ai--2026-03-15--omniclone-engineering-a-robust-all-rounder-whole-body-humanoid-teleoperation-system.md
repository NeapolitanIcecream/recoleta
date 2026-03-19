---
source: arxiv
url: http://arxiv.org/abs/2603.14327v1
published_at: '2026-03-15T11:13:04'
authors:
- Yixuan Li
- Le Ma
- Yutang Lin
- Yushi Du
- Mengya Liu
- Kaizhe Hu
- Jieming Cui
- Yixin Zhu
- Wei Liang
- Baoxiong Jia
- Siyuan Huang
topics:
- humanoid-teleoperation
- whole-body-control
- benchmarking
- vision-language-action
- sim2real
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# OmniClone: Engineering a Robust, All-Rounder Whole-Body Humanoid Teleoperation System

## Summary
OmniClone presents an engineered system for whole-body humanoid robot teleoperation, along with a fine-grained diagnostic benchmark, OmniBench. Its goal is to achieve more robust, more general, and more deployable whole-body motion tracking and data collection under low-cost hardware and limited data.

## Problem
- Existing whole-body humanoid teleoperation systems typically report only coarse aggregate metrics, which obscure failure modes across different motion regimes such as squatting, jumping, and low-position manipulation.
- Existing approaches are often tightly coupled to specific hardware, operator body shapes, and communication setups, requiring cumbersome calibration and making stable deployment in real-world settings difficult.
- This matters because whole-body teleoperation is not only used for real-time remote control, but is also key infrastructure for collecting high-quality demonstration data and training general-purpose robot/VLA policies.

## Approach
- The authors first build **OmniBench**: a diagnostic benchmark that evaluates across 6 skill categories (such as manipulation, walking, running, jumping, etc.) and 18 stratified difficulty/dynamics categories, specifically testing generalization to unseen motions.
- The core control policy is a **Transformer-based whole-body tracking policy**, trained via teacher-student distillation so that the model outputs joint control from historical proprioception and reference motion sequences.
- The authors use OmniBench to work backward and guide the training data recipe: the final balanced composition uses about **60% manipulation + 40% dynamic maneuvers/stable locomotion** to avoid a model that is only good at a single skill.
- At the system level, they add **operator-agnostic retargeting**, using dynamic scale correction to reduce geometric errors caused by differences in human body shape and MoCap systems; the paper notes that without correction, the maximum deviation is about **20 cm**, leading to an increase of about **20 mm MPJPE**.
- To handle jitter and latency in real deployment, the system uses **queue-based data management + zero-order hold + UDP communication**, achieving about **80 ms** end-to-end latency; the same policy also supports real-time teleoperation, generated motion playback, and VLA control input, making it a control-source-agnostic design.

## Results
- The paper claims that, compared with comparable methods, OmniClone reduces **MPJPE by more than 66%** through its data recipe and system optimizations, while requiring orders of magnitude fewer computational resources; training needs only about **30 hours of motion data**, a single **RTX 4090**, and about **80 GPU-hours** in total (**teacher about 60 hours, student about 22 hours**).
- On OmniBench, OmniClone outperforms GMT and Twist2 overall across all 18 stratified categories. For example, in **Loco-Manip Low**, MPJPE is **51.3 mm**, better than GMT’s **180.5 mm** and Twist2’s **210.5 mm**; in **Manip Medium**, it is **20.4 mm**, better than GMT’s **54.7 mm** and Twist2’s **156.3 mm**.
- It is also significantly stronger on dynamic motions: in **Run Medium**, OmniClone reaches **100% SR / 42.0 mm MPJPE**, compared with GMT’s **100% / 120.8 mm** and Twist2’s **100% / 176.9 mm**; in **Jump Medium**, it achieves **100% / 34.5 mm**, compared with GMT’s **90% / 105.3 mm** and Twist2’s **85% / 177.2 mm**.
- It also maintains a high success rate in some more difficult scenarios; for example, on **Walk Fast** it achieves **100% SR / 63.5 mm**, while OmniClone’s MLP version reaches only **20% SR / 111.7 mm**, showing that the Transformer backbone is clearly superior to the MLP.
- The real system generalizes to **6 operators** ranging from **1.47 m to 1.94 m**, spanning a **47 cm** height difference; the paper states that all novices completed a composite loco-manipulation task within **5–7** practice attempts.
- As a demonstration data engine, a VLA policy trained on data collected with OmniClone achieved real-world task success rates of **85.71%** (**Pick-and-Place**) and **80.00%** (**Squat to Pick-and-Place**).

## Link
- [http://arxiv.org/abs/2603.14327v1](http://arxiv.org/abs/2603.14327v1)
