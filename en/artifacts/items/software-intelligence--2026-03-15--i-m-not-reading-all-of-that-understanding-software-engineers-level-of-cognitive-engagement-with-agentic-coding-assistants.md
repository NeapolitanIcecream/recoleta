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
- code-intelligence
- cognitive-engagement
- software-engineering
relevance_score: 0.91
run_id: materialize-outputs
language_code: en
---

# I'm Not Reading All of That: Understanding Software Engineers' Level of Cognitive Engagement with Agentic Coding Assistants

## Summary
This paper studies software engineers’ cognitive engagement when collaborating with agentic coding assistants, pointing out that as tasks progress, developers think less and less about the process itself. Based on this, the authors argue that ACAs should be designed as genuine “Tools for Thought” that support thinking, rather than merely executors that automatically produce code.

## Problem
- The paper addresses the question of whether software engineers, when using agentic coding assistants (ACAs), reduce their critical thinking and process understanding as agent autonomy increases.
- This matters because software engineers need to judge correctness, weigh trade-offs, and identify failure modes, while LLMs/ACAs may still produce hallucinations, biases, or hidden defects.
- If developers only verify “whether the result is correct” without understanding “how it was done,” errors, edge cases, and security issues may be more easily missed in high-risk software contexts.

## Approach
- The authors conducted a formative user study, recruiting **4 software engineers** with experience ranging from **less than 1 year to more than 10 years**, and had them use **Cline** to complete an Excel-processing code generation task.
- The task flow was divided into two phases, **Plan** and **Act**, and the researchers observed on site how participants read the plan, responded to clarification questions, reviewed execution outputs, and whether they inspected the generated code.
- The study used **Bloom’s taxonomy** as the framework for cognitive engagement, breaking engagement into four categories: **recall / understand / analyze / evaluate**, and administered a self-report questionnaire immediately after the task to reduce recall bias.
- The authors then cross-checked questionnaire responses against the actual working directory, generated files, and observation notes, and conducted thematic analysis to identify patterns in how cognitive engagement changed across stages.
- The core mechanism can be summarized in the simplest terms: first let engineers use an ACA on a real task, then examine how much they actually remembered, understood, analyzed, and evaluated, in order to determine whether the ACA was weakening thinking.

## Results
- The sample size was very small, with only **4 participants**, and the paper did not report statistical significance or large-scale benchmark results; its conclusions are therefore **formative/exploratory findings**.
- The authors claim that cognitive engagement continuously declines as the task progresses: engagement is highest during planning, decreases during execution due to text information overload, and in the evaluation stage participants mainly check whether the output is correct rather than closely inspecting the code-generation process.
- In the recall questions, for “how many functions/methods were in the generated script,” **4/4 answered incorrectly (0% correct)**, indicating very weak memory of the code structure.
- For recalling the working directory name, only **2/4 answered correctly (50%)**; for the name of the first created file, **3/4 answered correctly (75%)**.
- The paper also reports that only **half (2/4)** of participants could understand the purpose of the first function and provide a reliable summary; likewise, only **half (2/4)** could analyze the code reasonably well and feel confident about its handling of edge cases.
- On whether to continue manually modifying the code, participants’ reasons centered on “**It generated my desired output**,” “**I trust Cline**,” and “**It worked**,” supporting the authors’ core conclusion: developers focus more on the happy path and final output than on process-level verification.

## Link
- [http://arxiv.org/abs/2603.14225v1](http://arxiv.org/abs/2603.14225v1)
