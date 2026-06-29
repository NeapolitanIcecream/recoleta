---
source: arxiv
url: https://arxiv.org/abs/2606.10933v1
published_at: '2026-06-09T14:44:43'
authors:
- Aman Sharma
- Sushrut Thorat
- Paras Chopra
topics:
- coding-agents
- metaprogramming
- esoteric-languages
- code-benchmarks
- tool-use
- software-agents
relevance_score: 0.94
run_id: materialize-outputs
language_code: en
---

# Frontier Coding Agents Use Metaprogramming to Adapt to Unfamiliar Programming Languages

## Summary
The paper finds that frontier coding agents handle unfamiliar programming languages best when they write generators in a familiar language, then debug the generated target-language code with local execution.

## Problem
- Standard coding benchmarks often test agents in Python, JavaScript, common libraries, and public repositories, where prior exposure can hide gaps in adaptation.
- Real software work can involve internal DSLs, proprietary config formats, generated APIs, and local tools with little public training data.
- The paper tests whether agents can learn enough during a session to write, run, debug, and submit correct programs in unfamiliar executable interfaces.

## Approach
- The authors evaluate six deployed coding agents: Claude Opus 4.6, Claude Sonnet 4.6, Claude Haiku 4.5, GPT-5.4 xhigh, GPT-5.4 mini, and Kimi K2.5.
- They use 80-problem sequences for four EsoLang-Bench languages: Brainfuck, Befunge-98, Whitespace, and Shakespeare.
- Each agent works in a persistent workspace with file editing, shell access, local interpreter calls, and up to 3 hidden submissions per problem.
- The main mechanism studied is metaprogramming: the agent writes a Python, JavaScript, or Rust program that emits target esolang source code, then tests and revises that generator locally.
- Diagnostic runs restrict metaprogramming, add written strategy guidance, provide helper libraries, and vary interpreter-call and output-token budgets.

## Results
- EsoLang-Bench separates agents far more than named mainstream benchmarks: the mean-score spread across six agents is 88.4 percentage points on EsoLang-Bench, compared with 6.6 on SWE-Bench Verified, 33.3 on Terminal-Bench 2.0, and 43.5 on LiveCodeBench v6.
- Main EsoLang-Bench mean scores are GPT-5.4 xhigh 99.7%, Claude Opus 4.6 86.9%, Claude Sonnet 4.6 66.3%, GPT-5.4 mini 32.5%, Claude Haiku 4.5 24.7%, and Kimi K2.5 11.3%.
- On Brainfuck, GPT-5.4 xhigh solves 98.8% and Opus 4.6 solves 80.0%, while Haiku 4.5 and Kimi K2.5 solve 5.0% each.
- Host-language generation explains much of the Brainfuck gain: Opus 4.6 solves 64/80 with Python generators, 63/80 with JavaScript, and 55/80 with Rust, versus 27/80 with direct authoring; GPT-5.4 xhigh solves 79/80, 77/80, and 79/80 with those hosts, versus 29/80 direct.
- Written strategy transfer gives little help, but executable helper code helps mid-tier agents: on Brainfuck, Sonnet 4.6 moves from 12/80 to 64/80 with the library, and GPT-5.4 mini moves from 5/80 to 53/80; on Befunge-98, Sonnet moves from 64/80 to 78/80 and GPT-5.4 mini from 11/80 to 64/80.
- Extra local interpreter calls and output tokens help agents that already build useful strategies; Haiku 4.5 remains near the floor, while Opus 4.6 improves with more interpreter access and reaches 20/20 on the first 20 Brainfuck and Befunge-98 problems with fewer output tokens than Sonnet 4.6.

## Link
- [https://arxiv.org/abs/2606.10933v1](https://arxiv.org/abs/2606.10933v1)
