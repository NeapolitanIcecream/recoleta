---
source: arxiv
url: https://arxiv.org/abs/2606.01969v1
published_at: '2026-06-01T09:32:25'
authors:
- Lo Gullstrand Heander
- Agnia Sergeyuk
- Ilya Zakharov
- "Emma S\xF6derberg"
- Nikita Mukhortov
topics:
- code-review
- llm-generated-code
- human-ai-interaction
- developer-tools
- trust-calibration
- ide-workflows
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Trust-Calibrated Code Review: A Participatory Design Study of Review Workflows for LLM-Generated Multi-File Changes

## Summary
This paper studies how developers should review LLM-generated changes that span several files. Its main claim is that IDE review tools should help reviewers calibrate trust by showing risk, rationale, and safe execution boundaries at the right level of detail.

## Problem
- Developers increasingly review code produced by LLM agents, but current IDE and diff tools give weak support for judging large multi-file changes.
- The task matters because reviewers may miss bugs, security risks, architecture drift, or maintainability issues when generated changes look coherent but contain local failures.
- The study identifies trust calibration as the main review problem: reviewers need to know which files, lines, and agent actions deserve closer attention.

## Approach
- The authors ran a participatory design study with JetBrains using the Double Diamond process: Discover, Define, Develop, and Deliver.
- In the Discover phase, 17 professional practitioners identified review challenges for LLM-generated multi-file changes; 7 of them returned for the Develop phase to sketch workflows and tool ideas.
- The core method is a three-level review workflow: overview for understanding the whole change, file-analysis for ranking files by risk, and code-snippet review for checking specific lines or chunks.
- The proposed tool design uses seven constructs: chunk, risk-per-line, risk-per-file, judge, walk-through, zooming in/out, and security cage.
- In simple terms, the IDE would first explain what the agent changed, then point reviewers to risky files and lines, then let them inspect concrete code with safety and confidence signals.

## Results
- Workshop participants produced 64 challenge notes grouped into Trust, Lack of control, Quality, and UI; Trust received 12 of the 17 red “dangerous” votes, while Lack of control received the other 5.
- The Define phase grouped challenges into 12 topics, including Broken code (13 occurrences), Intent misalignment (8), Bad UI/UX (6), Overcomplexity (6), Cognitive load (6), Lack of trust (5), and Lack of transparency/explainability (5).
- The validation survey received 97 responses; 54 were removed as likely LLM-generated or invalid, leaving 43 practitioner responses.
- All three workflow levels scored above the neutral midpoint in the survey, with mean Likert scores between 3.50 and 3.91 on a 5-point scale.
- 63% of respondents expected the prototype to reduce overall review effort compared with current tools, and 52% expected reduced trust-assessment effort.
- The paper does not report code-quality gains, defect-detection accuracy, or task-time measurements from a controlled review experiment.

## Link
- [https://arxiv.org/abs/2606.01969v1](https://arxiv.org/abs/2606.01969v1)
