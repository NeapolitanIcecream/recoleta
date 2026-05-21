---
source: arxiv
url: https://arxiv.org/abs/2605.12610v1
published_at: '2026-05-12T18:02:04'
authors:
- Smitha S Kumar
- Michael A Lones
- Manuel Maarek
- Hind Zantout
topics:
- code-intelligence
- automated-code-review
- peft
- programming-education
- code-llama
- java-feedback
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Fine-Tuning Models for Automated Code Review Feedback

## Summary
The paper fine-tunes Code Llama 7B to generate Java code review feedback for students, with separate feedback on the mistake and the next step. It claims PEFT beats prompting on instructor ratings and reaches student-rated usefulness close to ChatGPT in a small study.

## Problem
- Programming students need feedback that identifies the bug and gives a useful next step without handing over a full solution.
- Proprietary LLMs raise cost, privacy, transparency, and customization issues when student code is sent to external systems.
- Open models such as Code Llama can run locally, but the base model gives weaker feedback without task adaptation.

## Approach
- The authors build a dataset of 425 Java examples: 85 bug types, 5 samples per bug type, each with code, KM feedback, and KH feedback.
- DeepSeek-R1 generates the initial triplets, and the first author validates the feedback.
- CodeLlama-7B-Instruct is fine-tuned with QLoRA-style PEFT: 4-bit nf4 quantization, frozen base weights, and LoRA adapters on q_proj and v_proj.
- Trainable parameters drop from 6,743,789,568 to 5,242,880, with rank 10, scaling factor 16, and 0.08% dropout.
- The study compares PEFT against zero-shot prompting and 3-example in-context prompting, then evaluates outputs with instructor labels, BLEU, ROUGE, BERTScore, and a 7-student focus group.

## Results
- PEFT reaches 61% KM accuracy, compared with 20% for the baseline Code Llama prompt and 54% for few-shot prompting.
- PEFT reaches 60% KH helpfulness, compared with 26% for baseline and 46% for few-shot prompting.
- Misleading suggestions fall to 47% with PEFT, compared with 83% for baseline and 60% for few-shot prompting; lower is better.
- Prompt adherence reaches 95% with PEFT, compared with 54% for baseline and 86% for few-shot prompting.
- PEFT performance is similar across error categories: 49% for imperative errors and 52% for object-oriented errors.
- In the student study, 7 CS1 students rated compiler errors, ChatGPT feedback, and PEFT feedback on usefulness, clarity, and structure; the excerpt reports that ChatGPT and PEFT both received positive responses, while compiler error messages were rated ineffective.

## Link
- [https://arxiv.org/abs/2605.12610v1](https://arxiv.org/abs/2605.12610v1)
