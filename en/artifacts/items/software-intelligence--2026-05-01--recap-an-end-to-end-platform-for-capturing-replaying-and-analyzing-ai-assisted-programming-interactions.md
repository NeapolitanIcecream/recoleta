---
source: arxiv
url: https://arxiv.org/abs/2605.01104v1
published_at: '2026-05-01T21:20:38'
authors:
- Keyu He
- Qianou Ma
- Valerie Chen
- Wayne Chi
- Tongshuang Wu
topics:
- ai-assisted-programming
- code-intelligence
- developer-telemetry
- human-ai-interaction
- programming-education
- session-replay
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# RECAP: An End-to-End Platform for Capturing, Replaying, and Analyzing AI-Assisted Programming Interactions

## Summary
RECAP is an open-source VS Code platform for recording, replaying, and analyzing AI-assisted programming sessions. It links GitHub Copilot chat prompts to fine-grained code edits, so researchers can inspect how developers use AI during real projects.

## Problem
- Chat logs and git histories alone cannot show which prompt led to which edit, what the developer rejected, or how the work changed over time.
- Modern coding agents can edit multiple files across long sessions, while normal commits and short lab studies lose much of that detail.
- This matters for educators and researchers who need evidence about AI reliance, debugging behavior, and the code effects of AI assistance.

## Approach
- A VS Code extension records Copilot chat JSON files and a shadow git history of workspace changes.
- The shadow git store commits file saves, creates, deletes, renames, and unsaved dirty snapshots with a 5-second debounce and 30-second maximum interval.
- The system matches Copilot text edit groups to later git diffs within a 5-minute window using fuzzy line-level comparison, then labels edits as Copilot, human, partial match, unmatched, or likely external source.
- A web replay viewer merges chat events and code commits into one timeline with file tree, diff view, chat panel, and color-coded event markers.
- Analysis modules classify prompts into 17 behavior codes across 6 categories, compute AI edit share by work session, and cluster prompt embeddings.

## Results
- In a Spring 2026 university course deployment, RECAP captured 2,034 prompts from 29 students and 8,239 shadow-git commits from 41 students across 406 work sessions.
- The assignment lasted 2 weeks and asked students to extend two LLM-based features in Zulip.
- Prompt classification found Explain at 44%, with explain-error prompts alone at 29%; Plan and Code were each 14%, Converse was 13%, Setup was 8%, and Eval was 6%.
- AI edit share declined over successive work sessions, with weighted linear fit r = -0.222 and p < 0.001.
- Replay exposed concrete behavior patterns, including an 11-minute TypeError loop where prompts 17, 20, and 23 repeated the same error and Copilot produced fixes that led back to the original issue.
- The paper presents the deployment as a platform demonstration rather than a controlled outcome study, so it does not claim improvements in developer speed, code quality, or learning outcomes.

## Link
- [https://arxiv.org/abs/2605.01104v1](https://arxiv.org/abs/2605.01104v1)
