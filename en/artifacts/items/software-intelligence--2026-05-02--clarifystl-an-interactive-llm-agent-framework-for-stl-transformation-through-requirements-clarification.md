---
source: arxiv
url: https://arxiv.org/abs/2605.01209v1
published_at: '2026-05-02T02:55:06'
authors:
- Yue Fang
- Zhi Jin
- Jie An
- Hongshen Chen
- Xiaohong Chen
- Naijun Zhan
topics:
- llm-agents
- requirements-engineering
- signal-temporal-logic
- formal-specification
- human-ai-interaction
- cyber-physical-systems
relevance_score: 0.72
run_id: materialize-outputs
language_code: en
---

# ClarifySTL: An Interactive LLM Agent Framework for STL Transformation through Requirements Clarification

## Summary
ClarifySTL is an interactive LLM agent system that asks users to fix vague or ambiguous natural-language requirements before converting them to Signal Temporal Logic (STL). It targets cyber-physical system specifications where missing time bounds, thresholds, or unclear references can produce wrong formal formulas.

## Problem
- Natural-language CPS requirements often omit exact time intervals, numeric thresholds, or conditional logic, which blocks faithful STL generation.
- Ambiguous wording can map to multiple valid STL formulas, so a direct NL-to-STL model may encode the wrong user intent.
- Manual STL writing is slow and error-prone for domain experts working with real-time and real-valued constraints.

## Approach
- ClarifySTL first runs a fine-tuned Vagueness Detector that classifies temporal, numerical, and conditional-logic vagueness, then asks targeted questions using Chain-of-Thought prompting.
- It rewrites the requirement with the user answer and repeats the vagueness check until no missing STL-critical details are detected.
- It then runs an Ambiguity Detector built with triplet contrastive learning for referential and semantic ambiguity.
- For ambiguous cases, it generates multiple STL candidates, back-translates them into natural language, compares interpretations, asks the user to clarify, and repeats the check.
- The final clarified requirement is sent to an LLM to generate the STL formula.

## Results
- On DeepSTL, ClarifySTL reports +13.92% Formula Accuracy and +12.08% Template Accuracy over the state-of-the-art model.
- On STL-DivEn, it reports +12.57% Formula Accuracy and +12.99% Template Accuracy over the state-of-the-art model.
- On AmbiEval, it reports 90.9% average detection accuracy for vagueness and ambiguity.
- Human evaluation reports that it clarifies 93.8% of defective requirements.
- Human evaluation rates 93.3% of vagueness clarification queries and 94.3% of ambiguity clarification queries as effective.

## Link
- [https://arxiv.org/abs/2605.01209v1](https://arxiv.org/abs/2605.01209v1)
