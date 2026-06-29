---
source: arxiv
url: https://arxiv.org/abs/2606.02277v1
published_at: '2026-06-01T14:02:37'
authors:
- Bin Yu
- Yao Zhang
- Haishan Liu
- Shijie Lian
- Yuliang Wei
- Xiaopeng Lin
- Zhaolong Shen
- Changti Wu
- Ruina Hu
- Bailing Wang
- Cong Huang
- Kai Chen
topics:
- vision-language-action
- robot-benchmark
- semantic-grounding
- action-prediction
- embodied-evaluation
relevance_score: 0.93
run_id: materialize-outputs
language_code: en
---

# RoboSemanticBench: Diagnosing Semantic Grounding in Action Prediction for VLA Models

## Summary
RoboSemanticBench is a diagnostic benchmark for testing whether VLA models use instruction semantics when choosing robot actions. The paper finds that many fine-tuned VLA policies can grasp candidate objects but select the semantically correct target at random-level rates.

## Problem
- VLA models are expected to carry semantic knowledge from pretrained language or vision-language backbones into robot action prediction, but imitation fine-tuning can reward shortcuts instead.
- Standard robot benchmarks can mix motor skill, object recognition, and language following, so a high task score may hide weak semantic target selection.
- The problem matters because real robot instructions may require arithmetic, commonsense, factual knowledge, or multi-step language understanding before the robot can choose the right object.

## Approach
- RoboSemanticBench turns a multiple-choice question into a pick-and-place task: the robot must answer the question, map the answer option to a visible block, and move that block to an answer zone.
- The benchmark has three subsets: RSB-Math for controlled arithmetic, RSB-HardMath from GSM8K-style word problems, and RSB-General from commonsense and MMLU-style questions.
- Each subset has 4-choice and 10-choice suites, with randomized option-to-block mappings and block layouts to reduce fixed color, letter, and position shortcuts.
- The paper reports Task Success Rate (TSR), Grasp Success Rate (GSR), and normalized Semantic Grounding (nSG), where nSG=0 means random target choice after a successful grasp.
- The authors evaluate GO1, OpenVLA-OFT, DexVLA, TinyVLA, PD-VLA, pi0, pi0.5, GR00T N1.7, and QwenGR00T after 100,000 fine-tuning steps, usually with batch size 64.

## Results
- Across 500 simulation episodes per model and suite, pi0.5 has the best average TSR at 21.8%, followed by pi0 at 12.7%, GR00T N1.7 at 12.6%, OpenVLA-OFT at 11.1%, QwenGR00T at 10.7%, PD-VLA at 9.0%, TinyVLA at 8.6%, DexVLA at 6.5%, and GO1 at 2.0%.
- Random target choice is 25% in 4-choice suites and 10% in 10-choice suites; many models fall near or below these levels after conditioning on grasp success through nSG.
- Average nSG is negative for OpenVLA-OFT (-7.2%), GO1 (-19.4%), DexVLA (-3.4%), pi0 (-5.7%), GR00T N1.7 (-5.9%), and QwenGR00T (-7.1%).
- pi0.5 is the strongest model by nSG, with an average of 5.2%; PD-VLA reaches 3.2%, and TinyVLA is close to random at 0.2%.
- In the 10-choice suites, pi0.5 reaches 12.0% TSR on RSB-Math-10, 16.2% on RSB-HardMath-10, and 19.6% on RSB-General-10, while several other models stay below 9%.
- ReasoningVLA improves QwenGR00T average TSR from 10.7% to 16.0%, with gains on all six suites, but the paper reports that this still does not solve semantic grounding; QwenGR00T cotraining reduces average TSR to 8.2%.

## Link
- [https://arxiv.org/abs/2606.02277v1](https://arxiv.org/abs/2606.02277v1)
