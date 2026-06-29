---
source: arxiv
url: https://arxiv.org/abs/2605.22368v1
published_at: '2026-05-21T12:00:45'
authors:
- Yifan Bai
- Xiaoyang Liu
- Zihao Mou
- Guihong Wang
- Jian Yu
- Shuhan Xie
- Yantao Li
- Yangyu Zhang
- Jingwei Liang
- Tao Luo
topics:
- verifiable-code-generation
- code-intelligence
- software-benchmarks
- lean
- adversarial-testing
- test-suite-generation
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# VeriScale: Adversarial Test-Suite Scaling for Verifiable Code Generation

## Summary
VeriScale expands and trims test suites for Lean-based verifiable code generation so weak specifications and implementations are harder to pass by accident. It creates VerinaPlus and VerinaLite from Verina and reports large score drops for top LLMs under the stronger tests.

## Problem
- Current verifiable code generation benchmarks have too few positive and negative tests, so LLMs can pass while missing the intended behavior.
- SpecGen needs unexpected inputs and unexpected outputs to check whether generated preconditions and postconditions reject invalid behavior.
- The issue matters because inflated benchmark scores make generated specifications and code look safer than they are.

## Approach
- VeriScale starts with LLM-generated seed inputs and type-aware mutation to create many candidate inputs for each task.
- It uses Lean checks against the ground-truth precondition to split candidates into expected inputs and unexpected inputs.
- For expected inputs, it runs the reference implementation to produce expected outputs.
- To create hard unexpected outputs, it asks stronger models to write adversarial implementations that produce wrong outputs accepted by generated postconditions.
- It reduces the expanded suite with boundary-preserving selection for unexpected inputs and a greedy set-cover step that keeps expected cases that kill many adversarial implementations.

## Results
- VerinaPlus expands Verina by over 83x overall; VerinaLite is a lighter 14x variant.
- Mean expected input-output cases grow from 5.89 in Verina to 370.07 in VerinaPlus, a 62.83x increase; VerinaLite keeps 52.34, an 8.89x increase.
- Mean unexpected outputs grow from 12.69 to 1114.01 in VerinaPlus, an 87.79x increase; VerinaLite keeps 202.35, a 15.95x increase.
- Mean unexpected inputs grow from 0.65 to 119.00 in VerinaPlus, a 183.08x increase; VerinaLite keeps 15.80, a 24.31x increase.
- For GPT-5.5, SpecGen drops from 68.78% on Verina to 44.44% on VerinaPlus, and CodeGen drops from 96.83% to 86.24%.
- The paper evaluates 8 LLMs with Lean v4.24.0, reports 100% code coverage for the augmented benchmarks, and says VerinaLite keeps similar discriminative power to VerinaPlus at lower evaluation cost.

## Link
- [https://arxiv.org/abs/2605.22368v1](https://arxiv.org/abs/2605.22368v1)
