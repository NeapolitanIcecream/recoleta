---
source: arxiv
url: https://arxiv.org/abs/2605.04835v1
published_at: '2026-05-06T12:31:49'
authors:
- "David Sch\xF6n"
- Faiza Amjad
- Tehreem Asif
- Ranim Khojah
- Mazen Mohamad
- Francisco Gomes de Oliveira Neto
- Philipp Leitner
topics:
- code-refactoring
- llm-code-generation
- developer-adoption
- github-mining
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Patterns of Developer Adoption of LLM-Generated Code Refactoring Suggestions

## Summary
This paper studies how developers use ChatGPT refactoring suggestions in real GitHub commits. Its main claim is that developers often commit suggestions with little change, or they select parts of a larger suggestion and discard the rest.

## Problem
- The paper addresses a gap in LLM code-refactoring research: prior work judged suggestion quality, while this study measures how developers apply those suggestions in actual repositories.
- This matters because refactoring can affect maintainability and correctness, and teams need to know when ChatGPT output can be copied, edited, or treated as a starting point.
- The study only covers commits that link to a ChatGPT conversation, so it does not measure rejected suggestions.

## Approach
- The authors start from DevGPT, which contains 29,778 ChatGPT prompts and responses, 19,106 code snippets, and 3,245 commit objects collected in July-August 2023.
- They filter commits with 25 refactoring-related keywords, remove duplicates and invalid GitHub links, then build a curated dataset of 169 refactoring commits and 440 changed-file datapoints.
- For each changed file, they reconstruct the file before and after the commit from GitHub unified diffs, extract ChatGPT code blocks, and map each committed file to the most similar ChatGPT suggestion using normalized Levenshtein similarity.
- They estimate adoption with Jaccard 3-gram similarity, normalized Levenshtein similarity, token match rate, and CrystalBLEU.
- They manually inspect 190 datapoints to classify refactoring activities and developer edits, then exclude 16 cases where the commit changed behavior rather than refactoring only.

## Results
- Developers usually reached an adopted refactoring suggestion within 1-4 prompts in the ChatGPT conversation.
- Jaccard 3-gram and normalized Levenshtein scores show a bimodal pattern: many cases sit at low similarity around 0.1-0.3, while many others sit above 0.9.
- Token match rate is concentrated above 0.9 and has almost no density at low values, which suggests many low Jaccard or Levenshtein cases come from developers deleting unused parts of a larger ChatGPT suggestion.
- In the manually inspected subset, readability was the most common target at 38%, and maintainability was next at 34%.
- The most common observed refactoring activities were rename with 44 cases, improve documentation with 37 cases, restructure with 36 cases, and split logic with 33 cases.
- One repository, tisztamo/Junior, contributed 143 commits and 407 files, so the dataset has a strong project imbalance.

## Link
- [https://arxiv.org/abs/2605.04835v1](https://arxiv.org/abs/2605.04835v1)
