---
source: arxiv
url: https://arxiv.org/abs/2606.11863v1
published_at: '2026-06-10T09:38:40'
authors:
- Yufu Wang
- He Jiang
- Hao Lin
- Peiyu Zou
- Ang Jia
- Xiaochen Li
- Zhilei Ren
topics:
- code-translation
- code-intelligence
- llm-agents
- semantic-augmentation
- software-reliability
- automated-testing
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# Enhancing LLM-Based Code Translation with Verified Multi-Semantic Representations

## Summary
Multisage improves LLM code translation by deriving semantic guidance from the source code and checking that guidance before prompting the translator.
It targets functional correctness on HumanEval-X, with reported success-rate gains up to 2.22×.

## Problem
- LLM code translators can produce target code that compiles yet changes control flow, data handling, types, or API behavior.
- Test cases, docs, and specs can reduce these errors, but many real codebases lack those resources.
- The paper says many failures are intervenable semantic errors; in lightweight models, model-specific errors account for only 10%–23% of failures.

## Approach
- Multisage first parses the source code with static analysis to extract control-flow structure, function input/output types, and external API calls.
- It then generates several semantic views from those parsed signals: code summaries, function-level test cases, API descriptions, and API-level test cases.
- It trains a multi-task semantic augmentation model using datasets such as XLCoST and XCodeEval, with adaptive task weighting inspired by FAMO and MFTCoder.
- It checks generated semantics with execution validation, semantics-preserving code mutations, and cross-view consistency tests, then filters weak or conflicting guidance.
- The calibrated semantic guidance and the original source code are placed into the prompt for the target-language LLM translation.

## Results
- On HumanEval-X, Multisage reports translation success-rate gains up to 2.22× over vanilla prompting across tested backbone models.
- Against semantic enhancement baselines such as Chain-of-Thought and single-stage semantic prompting, it reports success-rate gains up to 1.42× on small models, 1.28× on mid-scale models, and 1.17× on large models.
- The paper groups evaluated models as lightweight models under 10B parameters, mid-scale models with 10B–100B parameters, and high-performance large models above 100B parameters.
- Compared with TransCoder under the same evaluation setting, Multisage reports higher CodeBLEU while keeping competitive execution success rates; the excerpt does not provide exact CodeBLEU values.
- The largest relative gains are reported on smaller models, which suggests the added semantic guidance helps most when the backbone has limited capacity.

## Link
- [https://arxiv.org/abs/2606.11863v1](https://arxiv.org/abs/2606.11863v1)
