---
source: arxiv
url: https://arxiv.org/abs/2605.04845v1
published_at: '2026-05-06T12:43:46'
authors:
- "Johannes H\xE4rtel"
topics:
- llm-agents
- repository-mining
- code-intelligence
- software-classification
- dynamic-context-retrieval
- tool-use
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Agentic Repository Mining: A Multi-Task Evaluation

## Summary
This paper tests whether LLM agents with bash access can classify software repository artifacts as well as LLMs given hand-built context. Across 4 tasks and 4943 valid classifications, agents reach similar accuracy while avoiding context-window failures on large artifacts.

## Problem
- Software repository mining often needs labels for commits, reviews, code lines, or whole repositories, and human labeling is slow, costly, and inconsistent.
- Simple LLM classifiers need someone to decide which repository context to put in the prompt, and that choice can cause wrong labels or context-window overflow.
- The problem matters because repository-mining studies depend on these labels for defect, security, maintenance, and project-quality analysis.

## Approach
- The study compares fixed-context LLM calls against agents built on the same LLMs.
- Agents start with an artifact identifier, such as a commit SHA, then inspect the repository in a sandboxed Docker container using bash and git commands.
- The evaluation covers 4 classification tasks: Munaiah repository classification (172 repos), Herbold bug-fix line classification (212 lines), Härtel security review classification (135 reviews), and Levin maintenance-intent commit classification (129 commits).
- It tests 8 approach configurations across Claude 3.7 Sonnet, Mistral Large 3, and Llama 3.3 70B, including chain-of-thought, no-chain-of-thought, memorization, native tool calling, and stop-sequence tool calling.
- The study measures accuracy, tokens, time, cost, failures, exploration steps, and 100 manually inspected disagreement cases.

## Results
- The experiment produced 5184 attempts; 212 were excluded because memorization did not apply to Herbold lines, and 29 were real errors, leaving 4943 valid classifications.
- The provided excerpt does not give per-task accuracy numbers. It claims no clear accuracy winner, with agents competitive against simple LLMs even though agents retrieve their own context.
- Agents had 0 context-window overflow errors. Simple Llama had 9, simple Claude Sonnet had 7, simple Claude Sonnet no-CoT had 6, and simple Mistral had 3.
- Simple LLMs used about 5K–8K input tokens per run. Agent Mistral averaged 8.5K fresh input tokens and 607 output tokens; Agent Sonnet stop-sequence averaged 10.7K fresh input, 18.2K cache-read, 4.9K cache-write, and 720 output tokens; Agent Sonnet native averaged 14.2K fresh input, 18.5K cache-read, 5.3K cache-write, and 1.1K output tokens.
- Agents cost more per run by factors of 1.2 to 3.2, but their cost had near-zero correlation with engineered context size, while simple LLM cost rose with large prompts.
- Manual diagnosis of 100 disagreement cases found cases where ground-truth labels or task specifications were questionable, so measured accuracy against the original labels may undercount methods with broader repository access.

## Link
- [https://arxiv.org/abs/2605.04845v1](https://arxiv.org/abs/2605.04845v1)
