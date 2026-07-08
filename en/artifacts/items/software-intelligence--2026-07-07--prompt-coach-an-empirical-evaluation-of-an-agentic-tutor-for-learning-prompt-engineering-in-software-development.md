---
source: arxiv
url: https://arxiv.org/abs/2607.06074v1
published_at: '2026-07-07T09:44:46'
authors:
- Rohit Mehra
- Kapil Singi
- Vikrant Kaulgud
- Vibhu Saujanya Sharma
- Swapnajeet Gon Choudhury
- Swati Sharma
- Adam P. Burden
- Majd Sakr
topics:
- prompt-engineering
- code-generation
- agentic-tutor
- ide-assistant
- human-ai-interaction
- software-engineering-education
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Prompt Coach: An Empirical Evaluation of an Agentic Tutor for Learning Prompt Engineering in Software Development

## Summary
Prompt Coach is a VSCode tutor that teaches developers to write better code-generation prompts through scored feedback and Socratic questions. In a 15-developer pre/post study, one 60-minute session improved average prompt-quality scores from 63.04 to 71.69.

## Problem
- Developers now need to express intent, constraints, context, output format, tests, and edge cases when asking LLMs to generate code.
- Static courses, tutorials, and prompt guides give generic advice and do not react to a developer’s codebase, task, target model, or skill gaps.
- The skill matters because weak prompts can omit constraints, error handling, and validation details that affect generated code quality.

## Approach
- Prompt Coach runs inside VSCode as a multi-agent system built with CrewAI, Azure backend services, ChromaDB for project-context retrieval, and GPT-4.1 for judging and guidance.
- It reads the local project context, including code, design notes, style guides, and requirements when available, then stores relevant information in a project-specific vector database.
- It scores each developer prompt from 0 to 100 across 8 dimensions: clarity, specificity, context awareness, adaptability, inclusion of constraints, error handling, output requirements, and testability.
- A consequence preview agent asks the target LLM what the current prompt would produce, uses likely failure modes internally, and does not show the generated code to the learner.
- A Socratic guidance agent turns weak dimensions into targeted questions, while a developer-modeling agent tracks repeated strengths and gaps across iterations.

## Results
- Study size was 15 professional developers with a mean of 9.6 years of experience, using a single-arm within-subjects pre/post design across 6 APPS benchmark tasks.
- Overall prompt-quality score rose from 63.04 at baseline to 71.69 after learning, a 13.73% relative increase with paired Wilcoxon p<.001.
- Gains by task complexity were 65.63 to 74.48 for introductory tasks (+13.93%, p=0.003), 62.56 to 69.05 for interview tasks (+10.38%, p=0.004), and 60.66 to 71.34 for competition tasks (+17.71%, p=0.001).
- The largest dimension gains were inclusion of constraints from 50.51 to 66.49 (+31.63%, p<.001), error handling from 52.56 to 68.67 (+30.66%, p<.001), and context awareness from 56.56 to 69.91 (+23.61%, p=0.002).
- Clarity did not improve: 79.87 to 79.71 (-0.19%, p=0.577). Adaptability improved from 66.89 to 69.58 (+4.02%) but was not significant at p=0.208.
- Perception scores on a 7-point Likert scale were positive: 100% agreement that the learning improved prompt-writing skills, 93.3% agreement on trust, 86.7% agreement on adoption likelihood, and 80.0% agreement that Prompt Coach was more useful than books, blogs, tutorials, articles, and MOOCs.

## Link
- [https://arxiv.org/abs/2607.06074v1](https://arxiv.org/abs/2607.06074v1)
