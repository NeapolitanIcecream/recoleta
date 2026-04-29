---
source: arxiv
url: http://arxiv.org/abs/2604.19728v1
published_at: '2026-04-21T17:51:51'
authors:
- Jean Mercat
- Sedrick Keh
- Kushal Arora
- Isabella Huang
- Paarth Shah
- Haruki Nishimura
- Shun Iwase
- Katherine Liu
topics:
- vision-language-action
- robot-foundation-model
- multimodal-training
- robot-data-scaling
- sim-evaluation
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# VLA Foundry: A Unified Framework for Training Vision-Language-Action Models

## Summary
VLA Foundry is an open-source codebase for training language, vision-language, and vision-language-action models in one stack. The paper’s main claim is that this unified pipeline makes VLA research easier to control and that stronger VLM backbones, such as Qwen3-VL, improve downstream robot policy performance.

## Problem
- Open VLA projects often focus on the final action-training stage and rely on separate pretraining pipelines, which makes backbone, data-mixture, and recipe studies hard to run cleanly.
- Robotics data is scarce compared with text and image-text data, so upstream LLM and VLM training choices can strongly affect downstream robot performance.
- Researchers need one system that supports full-pipeline experiments, modular swaps of backbones and datasets, and reproducible large-scale training.

## Approach
- The framework uses one shared codebase for LLM, VLM, and VLA training, with YAML/dataclass configuration, pluggable registries, shared training loops, and support for both from-scratch training and Hugging Face backbones.
- It standardizes multimodal data handling: text, image-caption, and robotics datasets can be mixed with weighted sampling, and robotics data gets dedicated normalization, action chunking, pose handling, and preprocessing into WebDataset shards.
- For scale, it supports distributed training with DDP/FSDP2, mixed precision, gradient checkpointing, and multi-node runs benchmarked up to 128 GPUs across 16 nodes.
- The paper demonstrates the framework with two model families: Foundry-VLA-1.7B trained through an LLM→VLM→VLA pipeline from scratch, and Foundry-Qwen3VLA-2.1B-MT built on a pretrained Qwen3-VL 2B backbone.
- The VLA model adds an observation token to the VLM sequence and feeds its hidden states into a 325M-parameter flow-transformer action head trained with flow matching to denoise action sequences.

## Results
- The from-scratch LLM is a 1.2B-parameter model trained on 500M samples / 1T tokens from DCLM. On standard multiple-choice benchmarks, the 1T-token checkpoint reports HellaSwag **66.7**, MMLU **26.6**, ARC-e **71.7**, ARC-c **39.3**, PIQA **77.5**, WinoGrande **62.6**, OpenBookQA **40.8**, and BoolQ **65.4**.
- The from-scratch VLM combines that LLM with an 86M-parameter ViT and is trained on **200M** DataCompDR-1B samples. On COCO_VAL captioning, the 200M-sample checkpoint reports BLEU-1 **58.64**, BLEU-2 **38.62**, BLEU-3 **24.49**, BLEU-4 **15.57**, ROUGE-L **38.17**, and CIDEr **55.14**.
- The VLA stack uses a 325M-parameter transformer action head on top of the VLM, giving a full from-scratch VLA model of **1.7B** parameters; the Qwen-based multitask model is **2.1B** parameters.
- The evaluation benchmark, lbm_eval_oss, contains **49** tabletop bimanual manipulation tasks in Drake simulation.
- The abstract claims that, in nominal closed-loop evaluation on LBM Eval, the fully open from-scratch model is on par with the authors’ prior closed-source work, and replacing the backbone with Qwen3-VL beats their baseline by a wide margin.
- The provided excerpt does not include the main VLA closed-loop success-rate table, so the exact robot-policy improvement numbers over baseline are not available here.

## Link
- [http://arxiv.org/abs/2604.19728v1](http://arxiv.org/abs/2604.19728v1)
