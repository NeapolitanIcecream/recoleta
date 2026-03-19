---
source: arxiv
url: http://arxiv.org/abs/2603.14225v1
published_at: '2026-03-15T05:03:20'
authors:
- Carlos Rafael Catalan
- Lheane Marie Dizon
- Patricia Nicole Monderin
- Emily Kuang
topics:
- agentic-coding-assistant
- human-ai-interaction
- cognitive-engagement
- software-engineering
- user-study
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# I'm Not Reading All of That: Understanding Software Engineers' Level of Cognitive Engagement with Agentic Coding Assistants

## Summary
This paper examines, through a small-scale formative user study, how software engineers’ cognitive engagement changes when using agentic coding assistants. The authors find that as tasks progress, engineers increasingly spend less effort understanding and verifying the process, and focus more on whether “the result looks right.”

## Problem
- The paper addresses the question of whether software engineers using agentic coding assistants (ACA) may reduce critical thinking, verification, and understanding because the assistant is too autonomous.
- This matters because software built by software engineers is often used in high-risk real-world contexts, while ACA/LLM systems may still hallucinate, exhibit bias, or miss edge cases.
- If engineers only look at the “happy path” and overtrust the ACA, incorrect code, fragile implementations, and even potential security issues may make their way into production systems.

## Approach
- The authors conducted a formative user study recruiting **4 software engineers** from a large company in the Philippines, with experience spanning four bands: **<1 year, 1-5 years, 6-10 years, >10 years**.
- Participants used **Cline** to complete a fixed code-generation task: process Excel files, locate the dashboard sheet, copy column data, and generate a new workbook.
- The study divided interaction into three phases: **planning / execution / evaluation**, and used **Bloom’s Taxonomy** to design a post-task questionnaire measuring four types of cognitive engagement: recall, comprehension, analysis, and evaluation.
- The authors cross-checked questionnaire responses against the actual working directory / generated code, and combined this with observation notes for thematic analysis to identify patterns in how cognitive engagement changed.
- The core mechanism can be summarized in the simplest terms: first let engineers complete a real ACA programming task, then check what they actually remembered, understood, analyzed, and whether they truly evaluated the coding process rather than just the result.

## Results
- The main finding is that cognitive engagement declines as the task progresses: participants were **most engaged during the planning phase**, but became noticeably disengaged during the **execution phase** because of large amounts of text output, and by the **evaluation phase** most only verified the output rather than reviewing the process.
- On recall questions, regarding the working directory name, only **2/4** answered correctly; regarding the first file created, **3/4** were correct; regarding how many functions were in the generated script, **all 4/4 answered incorrectly**.
- At the comprehension level, the authors report that only **half (2/4)** of participants could understand the first function and reliably provide a brief summary.
- At the analysis level, again only **half (2/4)** could analyze the code reasonably well and feel confident about its handling of edge cases; what participants mainly remembered and analyzed was the **“happy path”** leading to the correct output.
- At the evaluation level, **4/4** participants did not continue manually modifying the code after obtaining an apparently correct Excel output; their reasons included “**It generated my desired output**,” “**I trust Cline**,” and “**It worked**.”
- The paper does not provide statistical significance tests, control baselines, or large-sample quantitative performance improvements; its strongest concrete claim is that current text-based ACA interaction creates information overload, prompting engineers to adopt low-cost verification strategies and thereby weakening deep thinking.

## Link
- [http://arxiv.org/abs/2603.14225v1](http://arxiv.org/abs/2603.14225v1)
