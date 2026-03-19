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
- evaluation-framework
- prompt-engineering
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# A framework for assessing the capabilities of code generation of constraint domain-specific languages with large language models

## Summary
This paper proposes a general framework for evaluating the ability of large language models to generate constraint-oriented domain-specific language code from textual specifications, with a focus on OCL and Alloy, and compares them against Python. The conclusion is that LLMs are clearly stronger on mainstream languages, while they are more likely to fail on low-resource constraint DSLs, though multiple sampling attempts and code repair can bring improvements.

## Problem
- The problem the paper addresses is: **how to systematically evaluate the ability of LLMs to generate code for low-resource constraint DSLs**, rather than only looking at performance on popular general-purpose languages.
- This matters because constraint languages such as OCL and Alloy are used to **precisely express system constraints, verification, and testing**, but limited training data, dependence on domain models, and difficulty of direct execution make existing code-generation evaluation methods less suitable.
- Additional challenges of constraint DSLs include the need to understand **both the constraint text and the domain model in which it is defined**, the declarative nature of the language, and the possibility that multiple constraints may interact globally.

## Approach
- The paper proposes a **modular evaluation framework** that breaks the process into four steps: constructing prompts, invoking an LLM to generate code, checking whether the code is well-formed, and then checking whether it is correct.
- The framework supports multiple input combinations: **domain description, domain model, or both together**; it also supports different prompt templates, task organization strategies, and multiple generations.
- It designs **9 prompt templates**, covering whether to provide a natural-language domain description, a formal/natural-language domain model, and whether to ask the LLM to first explain or generate the domain model.
- For ill-formed code, the framework adds **single-round code repair**: feeding the erroneous code and parsing/compilation error messages back to the LLM, asking it to explain the problem and fix the code.
- The framework is instantiated to evaluate **OCL, Alloy, and Python**, and compares models such as **DeepSeek-coder, GPT-4o, GPT-4o-mini, Llama 3.1**; the paper states that the total number of experimental configurations **exceeds 90k**.

## Results
- The paper’s core conclusion is that **LLMs perform better overall on Python than on OCL and Alloy**, indicating that code generation for low-resource DSLs is significantly more difficult.
- The paper explicitly points out that **models with smaller context windows** (such as some open-source LLMs) may **be unable to generate constraint-related code**, because such tasks require accommodating both the constraint description and the domain model at the same time.
- **Multiple attempts** can increase the probability of generating correct code at least once, corresponding to improvements in **pass@k**; the paper treats this as one of the effective improvement strategies, but the excerpt **does not provide specific numerical values**.
- **Code repair** can also improve generation quality, especially when the model initially produces ill-formed code; the excerpt **does not provide exact percentage improvements before and after repair**.
- By contrast, the **choice of prompt template has relatively little impact**, at least compared with repeated sampling and repair strategies; the excerpt **does not provide quantified differences between templates**.
- The strongest specific quantitative claims available are that the framework covers **3 languages (OCL, Alloy, Python)**, evaluates **4 LLMs**, and explores **more than 90,000 configurations**; however, the excerpt currently provided **does not report concrete experimental numbers such as final accuracy or pass@k**.

## Link
- [http://arxiv.org/abs/2603.05278v1](http://arxiv.org/abs/2603.05278v1)
