---
source: arxiv
url: http://arxiv.org/abs/2603.01460v1
published_at: '2026-03-02T05:17:55'
authors:
- Ruihan Wang
- Chencheng Guo
- Guangjing Wang
topics:
- ai-coding
- client-side-development
- design-to-code
- prd-understanding
- multi-stage-pipeline
- code-generation
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Production-Grade AI Coding System for Client-Side Development

## Summary
This paper presents a production-grade AI coding system for real-world client-side development. It converts Figma designs, natural-language PRDs, and enterprise engineering standards into auditable intermediate artifacts, then generates code in stages. Its core value is that it does not "write code in one shot"; instead, it separates requirement understanding, planning, and execution, making it more reliable at meeting production requirements.

## Problem
- It is difficult to turn **designs + PRDs + enterprise standards** into deployable client-side code; existing design-to-code approaches often focus only on visual translation or one-shot generation, and struggle to reliably implement interaction logic.
- PRDs are unstructured, ambiguous, and incomplete, while Figma describes only UI structure and style without behavioral semantics; this disconnect can cause inconsistencies between code and product requirements.
- Client-side development also faces engineering constraints such as platform fragmentation, deep codebases, slow debugging, and poor runtime observability, so the cost of generation errors is higher than in many web/server scenarios.

## Approach
- It uses a **multi-stage, artifact-driven** pipeline: first context normalization, then task planning, and finally recoverable execution orchestration; each step produces persistent artifacts to support manual review, traceability, and failure recovery.
- It converts Figma into a design IR, transforms PRDs into structured "requirement understanding" artifacts, and injects engineering rules from the enterprise knowledge base, such as component usage conventions and spacing/asset rules.
- It models **PRD understanding as a UI component entity extraction problem similar to NER**: it first identifies the UI components mentioned in the PRD, then anchors the corresponding logic to specific components, reducing errors from open-ended reasoning.
- It uses a two-layer agent architecture: the coding agent in the IDE handles reasoning and code modification, while the backend capability server handles normalization, planning, and orchestration; during execution, it uses Task IR + dependency DAG + topological sorting to apply code changes step by step.
- To improve PRD decomposition capability, the authors built their own dataset based on real PRDs and performed LoRA fine-tuning on Qwen2.5-72B / Qwen2.5-VL-72B; the text and multimodal datasets each contain 182 samples, split 8:2.

## Results
- **PRD decomposition, text setting**: F1 improved from **0.568** to **0.743**; Precision improved from **0.506** to **0.822**, and Recall from **0.685** to **0.722**. This indicates that domain fine-tuning significantly strengthens the ability to identify UI control categories from PRDs.
- **PRD decomposition, multimodal setting**: F1 improved from **0.211** to **0.848**; Precision improved from **0.202** to **0.880**, and Recall from **0.256** to **0.865**. The improvement over the unfine-tuned multimodal baseline is very large.
- **Contribution of visual information**: for the fine-tuned multimodal model, removing images reduced F1 from **0.848** to **0.751**, showing that visual cues such as screenshots/sketches in PRDs provide clear help for identifying UI control categories.
- For data and training setup: the text and multimodal datasets each contain **182** samples, and the best model uses **LoRA rank=4**, trained for **30 epochs**, running on **4×H20 GPU**.
- The paper also claims that end-to-end evaluation shows relatively high **UI fidelity** and robust **interaction logic** implementation in real-world cases, but the current excerpt does not provide complete quantitative figures for the UI fidelity study or detailed comparisons with specific baselines.

## Link
- [http://arxiv.org/abs/2603.01460v1](http://arxiv.org/abs/2603.01460v1)
