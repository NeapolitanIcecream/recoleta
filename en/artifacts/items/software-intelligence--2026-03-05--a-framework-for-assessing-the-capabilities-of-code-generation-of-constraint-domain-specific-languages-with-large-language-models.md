---
source: arxiv
url: http://arxiv.org/abs/2603.05278v1
published_at: '2026-03-05T15:23:02'
authors:
- David Delgado
- "Lola Burgue\xF1o"
- "Robert Claris\xF3"
topics:
- llm-code-generation
- domain-specific-languages
- constraint-languages
- code-evaluation
- prompt-engineering
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# A framework for assessing the capabilities of code generation of constraint domain-specific languages with large language models

## Summary
This paper proposes a general framework for evaluating the ability of large language models to generate code for constraint domain-specific languages (DSLs) from textual specifications, and applies it to OCL, Alloy, and Python. The core conclusion is that LLMs are clearly stronger on Python, while they are more fragile on low-resource constraint languages such as OCL and Alloy, though multiple generations and code repair can bring improvements.

## Problem
- The paper addresses the problem of **how to systematically evaluate the ability of LLMs to generate code for low-resource constraint DSLs**, looking not only at whether code can be generated, but also at whether the code is **parsable/formally correct** and **actually satisfies the requirements**.
- This matters because constraint languages such as OCL and Alloy are used to **precisely express invariants, preconditions/postconditions, and integrity constraints**, which directly affect software verification, testing, and reliability. However, they have much less training data than mainstream languages like Python, so LLM performance is usually worse.
- Constraint DSLs are also harder because generation requires understanding both the **constraint itself** and the **domain model/schema** it depends on; moreover, these languages are more declarative and globally scoped, so they cannot always be validated through direct execution.

## Approach
- The paper proposes a **modular evaluation framework** that breaks the code generation process into four steps: **construct prompts**, **invoke the LLM to generate and extract code**, **check well-formedness (syntactic/structural validity)**, and **check correctness (functional/semantic correctness)**.
- The framework supports multiple input and prompting configurations: it can use **domain descriptions**, **domain models**, or both combined; it includes **9 prompt templates (PT1–PT9)** and multiple task delivery modes (batch, chained, isolated).
- To improve generation quality, the framework systematically studies two strategies: **single-round code repair** (feeding parsing/validation error messages back to the LLM to fix the code) and **multiple attempts** (generating several candidates for the same task and using pass@k to evaluate the probability that at least one succeeds).
- In the experimental instantiation, the authors choose **OCL, Alloy, and Python** as the three languages and compare models such as **DeepSeek-coder, GPT-4o, GPT-4o-mini, and Llama 3.1**; they also curate and expand a dataset containing domain specifications and integrity constraints.
- The paper claims to have systematically evaluated **more than 90k configurations** to analyze how different LLMs, prompts, repair, and multiple-attempt decisions affect results.

## Results
- The key conclusion explicitly reported by the paper is that **LLMs perform better overall on Python than on OCL and Alloy**, indicating that code generation for low-resource constraint DSLs is significantly harder; however, the abstract excerpt **does not provide specific percentages, accuracy, or pass@k values**.
- The authors note that **models with smaller context windows** (especially some open-source LLMs) may **be unable to generate constraint-related code**, because the task requires simultaneously managing both the **constraint** and the **domain model** in which it is defined; this excerpt likewise **does not provide specific model scores**.
- **Code repair** and **multiple candidate generations** can improve generation quality, while the impact of **prompt template choice** is relatively small. These are the paper’s strongest experimental claims, but the provided text **does not disclose concrete gain numbers or baseline differences**.
- One of the paper’s large-scale results is that its experiments explored **more than 90,000 configurations** to systematically compare code generation performance under different settings.
- From a contribution perspective, the main advance is not a new generation model, but a **parameterizable, reusable evaluation framework across GPLs and DSLs** that specifically covers the two evaluation layers of well-formedness and correctness for constraint DSLs.

## Link
- [http://arxiv.org/abs/2603.05278v1](http://arxiv.org/abs/2603.05278v1)
