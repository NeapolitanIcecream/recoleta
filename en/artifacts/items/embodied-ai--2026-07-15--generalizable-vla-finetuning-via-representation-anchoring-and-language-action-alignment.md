---
source: arxiv
url: https://arxiv.org/abs/2607.13429v1
published_at: '2026-07-15T04:13:54'
authors:
- Dwip Dalal
- Shivansh Patel
- Chahit Jain
- Jeonghwan Kim
- Utkarsh Mishra
- Alex Baratian
- Hyeonjeong Ha
- Heng Ji
- Svetlana Lazebnik
- Unnat Jain
topics:
- vision-language-action
- robot-foundation-model
- representation-anchoring
- language-action-alignment
- sim2real
- robot-data-scaling
relevance_score: 0.97
run_id: materialize-outputs
language_code: en
---

# Generalizable VLA Finetuning via Representation Anchoring and Language-Action Alignment

## Summary
Anchor-Align improves VLA finetuning by preserving pretrained vision-language representations and training language predictions to agree with robot actions. The method reports stronger semantic, perceptual, and long-horizon generalization than standard behavior cloning and several VLA baselines in simulation and on a physical xArm7 robot.

## Problem
- Behavior-cloning finetuning can overwrite the visual and semantic representations that support generalization, causing policies to memorize training scenes rather than respond to changed objects, positions, or instructions.
- Co-training on generic image-text data does not directly constrain representations on robot observations and can leave language and action predictions misaligned.
- This matters because standard manipulation benchmarks may hide failures that emerge under spatial rearrangement, semantic changes, perceptual perturbations, and long-horizon execution.

## Approach
- Vision-Language Anchoring keeps a frozen copy of the pretrained VLM and distills its vision and text hidden states into the trainable backbone at every decoder layer.
- Language-Action Alignment converts each demonstration action chunk into one of six motion-direction labels—up, down, left, right, forward, or backward—and predicts that label from the same robot observation used for action prediction.
- The method jointly optimizes standard behavior-cloning loss, the layer-wise anchoring loss, and the language-action alignment loss, without requiring additional data or architectural changes.
- It is evaluated with VLA-Adapter using regression actions and with StarVLA using a flow-matching action head, covering two architectures and action-generation mechanisms.

## Results
- On LIBERO-PRO, Anchor-Align reaches a mean success rate of 71.9%, versus 61.0% for VLA-Adapter; on LIBERO-Plus it reaches 90.3%, versus 85.1%. It improves every reported axis in both benchmarks.
- On the difficult LIBERO-PRO position-swap test, Anchor-Align scores 22.6%, compared with 2.3% for VLA-Adapter and 0% for MolmoAct, OpenVLA-OFT, and the reported co-training baseline.
- On CALVIN ABC→D, five-instruction completion rises to 77.9% from 73.1% for VLA-Adapter and 66.5% for OpenVLA-OFT; average rollout length increases to 4.5 tasks from 4.3.
- In physical xArm7 experiments, success improves from 28% to 54% and from 37% to 60% across the two evaluated VLA architectures, according to the abstract.
- Ablations show complementary effects: anchoring alone reaches 68.1% on LIBERO-PRO and 87.3% on LIBERO-Plus, alignment alone reaches 65.9% and 88.6%, while the full method reaches 71.9% and 90.3%.
- The excerpt does not provide complete real-robot task breakdowns or all statistical details, so the reported gains should be interpreted within the listed benchmarks, architectures, and evaluation settings.

## Link
- [https://arxiv.org/abs/2607.13429v1](https://arxiv.org/abs/2607.13429v1)
