---
source: arxiv
url: http://arxiv.org/abs/2603.01896v2
published_at: '2026-03-02T09:17:06'
authors:
- Shubham Ugare
- Satish Chandra
topics:
- code-reasoning
- llm-agents
- static-analysis
- patch-verification
- fault-localization
relevance_score: 0.08
run_id: materialize-outputs
language_code: en
---

# Agentic Code Reasoning

## Summary
This paper studies whether LLMs can, **without executing code**, traverse a codebase like an agent and perform reliable semantic reasoning. The authors propose a more constrained form of reasoning than free-form reasoning, called **semi-formal reasoning**, which uses a structured “certificate” to force the model to write out premises, execution paths, and conclusions, thereby improving accuracy across multiple code-understanding tasks.

## Problem
- Target problem: enable LLM agents to determine patch equivalence, localize defects, and answer code semantic questions **without running programs/tests**.
- This matters because executing code in real repositories is often expensive, dependency-heavy, and hard to scale, while many scenarios (RL rewards, code review, static analysis) require low-cost but reliable semantic judgments.
- Existing methods are either **unstructured reasoning**, which can skip steps and make unsupported assertions, or **fully formal verification**, which is too heavyweight for real-world multilingual repositories.

## Approach
- The paper introduces an **agentic code reasoning** setting: the agent may use tools to browse the repository and trace cross-file dependencies, but **may not execute repository code or tests**.
- The core method is **semi-formal reasoning**: the agent is given a structured template that requires it to explicitly fill in premises, analyze test cases / execution paths one by one, provide counterexamples or comparisons, and state a formal conclusion.
- Put simply, it changes “think and then answer” into “list evidence first, then trace step by step, and finally conclude,” reducing guesswork.
- The template is customized by task: patch equivalence requires comparing behavior for each test; fault localization requires listing suspicious regions and explaining how they cause failures; code QA requires function tracing, data flow, and evidence about semantic properties.
- The paper compares single-call, standard agentic reasoning, and semi-formal reasoning across three task types, and analyzes the trade-off between number of steps and error modes.

## Results
- **Patch equivalence (curated, 170 examples, Opus-4.5)**: overall accuracy improves from **78.2%** to **88.8%**; for non-equivalent samples from **78.6%** to **82.9%**, for equivalent samples from **78.0%** to **93.0%**; average steps increase from **10.08** to **28.17**.
- **Real agent-generated patch verification (200 examples, with test patches)**: under Opus-4.5, semi-formal agentic reaches **93.0%**, outperforming single-call **86.0%**, single-call+file context **87.5%**, agentic standard **87.0%**, and also clearly exceeding **difflib 73%**; under Sonnet-4.5, semi-formal agentic reaches **91.5%**, above agentic standard **84.5%**.
- **Code question answering (RubberDuckBench)**: the abstract states that semi-formal reaches **87%** accuracy, about a **9 percentage point** improvement over standard agentic reasoning; the contribution section also reports a **10.8 percentage point** gain over single-shot **76%**, and an **8.7 percentage point** gain over standard agentic reasoning.
- **Fault localization (Defects4J, small-scale 43 evaluable bugs)**: Opus-4.5 agentic semi-formal reaches **Top-5 72.1%** on the strict **All** metric, higher than agentic standard’s **60.5%** (+**11.6pp**); on the **Any** metric it reaches **88.4%**, above **81.4%** (+**7.0pp**).
- **Fault localization (Defects4J, large-scale 90 evaluable bugs)**: the paper explicitly states that Opus-4.5 semi-formal improves over standard by about **5 percentage points** on **Top-5 (All)**; the reported standard baseline is **43.3%**, implying semi-formal is about **48.3%**, though the truncated text does not fully show the final table values.
- Strongest conclusion: structured, checkable reasoning “certificates” can substantially improve the reliability of code semantic analysis **without executing code**, and bring patch verification accuracy close to the level needed for **execution-free RL reward**.

## Link
- [http://arxiv.org/abs/2603.01896v2](http://arxiv.org/abs/2603.01896v2)
