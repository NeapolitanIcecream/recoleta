---
source: arxiv
url: http://arxiv.org/abs/2604.22615v1
published_at: '2026-04-24T14:46:03'
authors:
- Chengyang Li
- Kaiyi Xiong
- Yuan Xu
- Lei Qian
- Yizhou Wang
- Wentao Zhu
topics:
- vision-language-action
- human-to-robot-transfer
- gaze-modeling
- robot-manipulation
- few-shot-robot-learning
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# GazeVLA: Learning Human Intention for Robotic Manipulation

## Summary
GazeVLA learns human intention from egocentric human video and transfers that signal to robot manipulation. It uses gaze as the intention signal, predicts intention before action, and reports better few-shot performance and stronger out-of-distribution generalization than prior robot and human-pretrained baselines.

## Problem
- Vision-language-action models still need large amounts of robot demonstration data, which is expensive and hard to scale.
- Human egocentric video is easier to collect, but direct transfer is hard because human and robot bodies and action spaces differ.
- Prior work mostly learns **what** action to take. This paper targets **why** the action is taken, using intention as the bridge.

## Approach
- The paper introduces **VLIA** (Vision-Language-Intention-Action), which models intention with **human gaze** and inserts it as an intermediate step between perception and action.
- It pretrains on a curated egocentric human dataset built from **13 datasets** with **over 150M frames**, using gaze and hand annotations plus language.
- The model uses **PaliGemma** as the vision-language backbone and a **conditional flow matching** action expert for continuous action generation.
- At inference time, it follows an intention-action chain: first predict discretized gaze tokens from image and instruction, then generate future actions conditioned on that predicted intention.
- During post-training, it mixes a small amount of robot data with human data at a **1:1 sampling ratio**; robot data have no intention labels, so intention knowledge is transferred from human supervision only.

## Results
- On human pretraining evaluation, intention prediction error is **4.8% of the image diagonal**, about **11 pixels** on **224×224** images. Hand motion reconstruction reaches **4.71 cm** mean keypoint error and **12.31°** wrist rotation error.
- On the **AV-ALOHA** simulation benchmark, average success rate is **49** in-distribution, beating **pi0.5: 41**, **LFA: 43**, **H-RDT: 39**, and **DP: 28**.
- On AV-ALOHA out-of-distribution with distractors, average success rate is **28**, above **pi0.5: 22**, **LFA: 14**, **H-RDT: 14**, and **DP: 7**.
- On AV-ALOHA out-of-distribution with lighting changes, average success rate is **27**, above **pi0.5: 23**, **H-RDT: 6**, and **LFA/DP: 0**. The paper states this is a **22% relative improvement** over **pi0.5** in OOD settings.
- On individual simulation tasks, it reaches **100** on cube transfer ID and **56** on slot insertion OOD-distractors, compared with **94** and **47** for **pi0.5**.
- In real-robot experiments, the excerpt reports stronger performance across gripper and dexterous tasks with only **10 robot trajectories** and **50 human trajectories** per task. It gives one explicit number: **85% success** on simple pick-and-place, and says screw tightening reaches **2×** the success rate of **pi0.5**. The excerpt does not include the full numeric table from Figure 6.

## Link
- [http://arxiv.org/abs/2604.22615v1](http://arxiv.org/abs/2604.22615v1)
