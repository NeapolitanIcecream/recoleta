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
- design-to-code
- client-side-development
- prd-understanding
- multimodal-code-generation
relevance_score: 0.05
run_id: materialize-outputs
language_code: en
---

# Production-Grade AI Coding System for Client-Side Development

## Summary
This paper proposes an AI coding system for real-world industrial client-side development that converts Figma designs, PRD documents, and enterprise engineering specifications into auditable intermediate artifacts, then generates code in stages. Its core contribution is replacing one-shot generation with a structured pipeline, and significantly improving alignment between requirement understanding and implementation through UI-component-oriented PRD decomposition.

## Problem
- Existing design-to-code or code generation methods often lean toward visual translation or single-shot generation, and struggle to simultaneously satisfy production requirements such as **design consistency, interaction logic, and enterprise standards**.
- Client-side development involves heterogeneous inputs: Figma provides layout and style, but lacks behavioral semantics; PRDs describe behavior, but are often **unstructured, ambiguous, and incomplete**.
- Real-world mobile engineering also faces complex codebases, platform differences, high debugging costs, and weak runtime observability, so “generating deployable code” is harder than ordinary prototype generation, and also more important.

## Approach
- The system uses a **multi-stage, artifact-driven** pipeline: it first performs context normalization, then task planning, and finally incremental code generation according to dependencies; each step preserves persistent artifacts to support review, recovery, and reproducibility.
- It models **PRD understanding as a UI component entity extraction task similar to NER**: identifying components such as buttons, input fields, and lists from PRDs, and binding logic to specific UI components to reduce mismatches between requirements and implementation.
- It normalizes Figma inputs to generate hierarchical design IR, style tokens, and component sets; it can optionally use YOLO to detect UI elements, correct redundant hierarchies, and add explicit nodes.
- It injects enterprise knowledge through retrieval augmentation, such as component usage rules, spacing systems, and asset specifications, making project constraints explicit to the model.
- It organizes execution using Task IR + sibling DAG + Kahn topological sorting, so tasks can progress in a dependency-aware, recoverable, and traceable way rather than through open-ended free generation.

## Results
- On the PRD decomposition task, the **text baseline** achieved an F1 of **0.568**, which improved to **0.743** after domain fine-tuning; Precision rose from **0.506** to **0.822**, and Recall from **0.685** to **0.722**.
- The **multimodal baseline** performed poorly, with an F1 of only **0.211**; after fine-tuning, the multimodal model reached **0.848 F1**, with Precision **0.880** and Recall **0.865**, indicating that task-specific training is critical.
- When images were removed from the fine-tuned multimodal model, F1 dropped from **0.848** to **0.751**, showing that visual information provides a clear complementary benefit for recognizing UI control categories from PRDs.
- For training data, the authors constructed two specialized datasets: a **text dataset with 182 samples** and a **multimodal dataset with 182 samples**, both split **8:2** into training and test sets; the best models were based on **Qwen2.5-72B-Instruct** and **Qwen2.5-VL-72B-Instruct**, using **LoRA rank=4** and **30 epochs**.
- The paper also claims that end-to-end evaluation shows **high UI fidelity** and **robust implementation of interaction logic**, but in the provided excerpt, aside from PRD decomposition, it does not provide more complete end-to-end quantitative tables or detailed numerical comparisons with external methods.

## Link
- [http://arxiv.org/abs/2603.01460v1](http://arxiv.org/abs/2603.01460v1)
