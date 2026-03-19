---
source: arxiv
url: http://arxiv.org/abs/2603.05487v1
published_at: '2026-03-05T18:53:50'
authors:
- Hugo Buurmeijer
- Carmen Amo Alonso
- Aiden Swann
- Marco Pavone
topics:
- vision-language-action
- mechanistic-interpretability
- activation-steering
- representation-control
- openvla
- robot-policy
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Observing and Controlling Features in Vision-Language-Action Models

## Summary
This paper proposes a framework for internal interpretability and controllability in Vision-Language-Action models (VLAs): first "observe" hidden features, then use minimal linear interventions to "control" those features. The core goal is to guide robot behavior in real time **without fine-tuning the model**, while preserving the original closed-loop capability and natural actions as much as possible.

## Problem
- Although VLAs are powerful, their behavior is often **unpredictable and difficult to correct online**, and may also be inconsistent with user preferences or safety constraints.
- Existing activation steering ideas from LLMs **cannot be directly transferred** to VLAs, because VLAs involve multimodal inputs, continuous action outputs, and operate within closed-loop robotic control.
- The key question is: can we **read out behavior-relevant features** from a VLA's internal representations, and **manipulate those features online** in a way that is **lightweight, precise, and minimally disruptive to the original policy**?

## Approach
- The paper introduces two formal concepts: **feature-observability** (whether a target feature can be read out from the hidden state of a given layer) and **feature-controllability** (whether modifying the hidden state of a given layer can push the feature into a target range).
- A **linear observer/probe** is used to predict robot state or action features from activations at a Transformer layer; the paper mainly focuses on measurable and controllable variables such as end-effector position, orientation, and gripper state/action.
- A **minimum-norm linear intervention** is applied by adding an offset vector to the hidden representation so that the feature read out by the observer falls into a desired range; when the observer is linear and the target is a one-dimensional interval, the intervention has a **closed-form solution**.
- The observer and controller are embedded into the forward pass at inference time and executed online at a selected layer, forming a closed-loop steering mechanism that **requires no additional training/fine-tuning**.
- The method is validated on two types of VLAs: **OpenVLA** (Transformer-based) and **π₀.₅** (Transformer + flow-matching hybrid).

## Results
- The paper explicitly claims that on **Libero / π₀.₅** and **BridgeData V2 / OpenVLA**, robot **state and actions can be observed from the representation space using linear probes**, and that these observations are robust to small perturbations.
- The paper claims that through **targeted, lightweight linear interventions**, it is possible to **reliably steer robot behavior** while **preserving closed-loop capability**, enabling online alignment without fine-tuning.
- The paper also claims that the method supports **real-time** alignment of VLAs to user preferences and task requirements, with **minimal/negligible** additional runtime overhead, because both the observer and controller use linear computation and a closed-form control solution.
- This excerpt **does not provide complete quantitative results** (such as success rates, errors, or percentage improvements over baselines); it only mentions that Figure 3 shows comparisons with "mean prediction/majority-class prediction" baselines, and Figure 4 shows the effect of interventions at different layers on actions (such as delta yaw), but the specific values are missing from the excerpt.
- Therefore, the strongest concrete conclusion is: **linear observability + minimal linear controllability** holds for two representative VLA architectures, and can be used for **online, no-fine-tuning** behavior steering.

## Link
- [http://arxiv.org/abs/2603.05487v1](http://arxiv.org/abs/2603.05487v1)
