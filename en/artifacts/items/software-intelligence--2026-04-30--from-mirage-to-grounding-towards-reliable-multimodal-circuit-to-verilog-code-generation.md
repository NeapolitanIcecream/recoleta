---
source: arxiv
url: https://arxiv.org/abs/2604.27969v2
published_at: '2026-04-30T15:01:27'
authors:
- Guang Yang
- Xing Hu
- Xiang Chen
- Xin Xia
topics:
- multimodal-code-generation
- verilog-generation
- visual-grounding
- code-intelligence
- hardware-design
- benchmarking
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# From Mirage to Grounding: Towards Reliable Multimodal Circuit-to-Verilog Code Generation

## Summary
The paper shows that many multimodal code models can score well on circuit-to-Verilog tasks while relying on module-header names instead of reading the circuit image. It introduces C2VEval to expose this failure and VeriGround, a 4B model trained to use visual circuit topology and refuse invalid inputs.

## Problem
- Circuit diagrams encode hardware behavior, so a wrong visual-to-Verilog translation can create expensive RTL and silicon errors.
- Standard evaluation gives the model a module header, and names such as `sum`, `cout`, `clk`, or `fsm_3state` can reveal the target circuit without the image.
- This creates the Mirage failure: replacing the diagram with a blank image leaves Pass@k unchanged or higher, hiding weak visual grounding.

## Approach
- C2VEval contains 169 circuit-to-Verilog samples rendered from verified Verilog with netlistsvg, with exact image-code correspondence.
- The benchmark uses paired Normal and Anony variants. Normal keeps semantic identifiers; Anony replaces module, port, and parameter names with placeholders while preserving topology.
- Models are tested in Original mode with the real diagram and Mirage mode with a blank image while keeping the same header.
- VeriGround is trained with mixed Normal and Anony supervised fine-tuning, refusal examples for blank or mismatched images, and D-ORPO alignment that weights early generate-or-refuse tokens more heavily.

## Results
- On C2VEval Normal, Mirage mode matches or beats Original mode on all 8 evaluated MLLMs across reported metrics, showing that blank-image performance can equal or exceed real-image performance.
- Under Anony, Functional Pass@1 drops sharply for frontier models: GPT-5.4 falls from 45.51% Normal Original to 24.55% Anony Original, and Opus-4.6 falls from 52.69% to 11.38%.
- Sample-level analysis on 167 samples finds Original-only success at 8.2% in Normal and 8.8% in Anony, so the paper estimates genuine visual grounding at about 8-9% of samples.
- VeriGround 4B reaches Functional Pass@1 of 46.11% on Normal and 42.51% on Anony.
- VeriGround is close to GPT-5.4 on Normal Functional Pass@1, 46.11% versus 45.51%, and beats reported baselines on Anony with p < 0.001 by McNemar's test.
- VeriGround keeps False Refusal Rate at 1.20% on Normal and 0.00% on Anony valid inputs, while maintaining at least 92% Refusal Rate on blank images.

## Link
- [https://arxiv.org/abs/2604.27969v2](https://arxiv.org/abs/2604.27969v2)
