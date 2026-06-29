---
source: arxiv
url: https://arxiv.org/abs/2605.19369v1
published_at: '2026-05-19T05:04:42'
authors:
- Ravishka Rathnasuriya
- Wei Yang
topics:
- code-calibration
- selective-prediction
- uncertainty-estimation
- code-intelligence
- abstention
- program-analysis
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# When to Answer and When to Defer: A Decision Framework for Reliable Code Predictions

## Summary
This paper proposes a deployment decision process for code models that accepts predictions only when calibrated correctness scores clear a threshold and routes uncertain cases to analysis tools or recovery steps.

## Problem
- Code models can assign high confidence to wrong vulnerability, defect, completion, synthesis, or repair outputs, which makes IDE and CI automation risky.
- Standard calibration can lower average error while still failing to rank individual code predictions by correctness, so it may not support selective prediction.
- Abstention needs a follow-up action, such as static analysis, validation, prompt augmentation, or human review, or it only hides errors.

## Approach
- The system extracts uncertainty signals from classification and generative code models, including predictive distributions, entropy-like scores, margins, variance, and sampling disagreement.
- Calibration maps those signals to per-sample correctness probabilities; proposed options include weighted logistic scaling for generation and logit-based correctness estimation for classification.
- At inference time, a tunable threshold accepts outputs above the score cutoff and defers lower-scored outputs.
- Deferred generation cases go through MCP-based recovery, such as prompt augmentation, documentation injection, diversified decoding, compiler checks, validators, length constraints, or task decomposition.
- Deferred classification cases can be checked with static analyzers, program slicing, rule validators, or security-pattern checks.

## Results
- On MBPP+, weighted Platt calibration improved DeepSeek-Coder-7B from Brier 0.273 and ECE 0.223 to Brier 0.162 and ECE 0.072; Platt scaling was 0.224/0.103 and isotonic regression was 0.216/0.143.
- On MBPP+, weighted Platt calibration improved CodeLlama-7B from Brier 0.220 and ECE 0.108 to Brier 0.172 and ECE 0.045; isotonic regression reached 0.215/0.054.
- For defect prediction, the reported logit/confidence method improved DeepSeek-Coder-7B from Brier 0.130 and ECE 0.029 to Brier 0.098 and ECE 0.012.
- For defect prediction, the same method improved Qwen-Coder-7B from Brier 0.137 and ECE 0.023 to Brier 0.089 and ECE 0.011.
- The paper reports selective prediction accuracy above 70% at 80% coverage for MBPP+ generation and above 90% at 80% coverage for defect prediction.
- The authors evaluated 16 uncertainty metrics across defect prediction, vulnerability detection, and code generation, and found no task-agnostic metric that reliably supports abstention without task-specific calibration.

## Link
- [https://arxiv.org/abs/2605.19369v1](https://arxiv.org/abs/2605.19369v1)
