---
source: arxiv
url: https://arxiv.org/abs/2605.08435v1
published_at: '2026-05-08T19:58:27'
authors:
- Matthias Galster
- Seyedmoein Mohsenimofidi
- "Levi B\xF6hme"
- Jai Lal Lulla
- Muhammad Auwal Abubakar
- Christoph Treude
- Sebastian Baltes
topics:
- agentic-coding-tools
- code-intelligence
- software-engineering-dataset
- ai-configuration
- human-ai-collaboration
- github-mining
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# A Dataset of Agentic AI Coding Tool Configurations

## Summary
This paper releases a curated GitHub dataset of repository-level configuration files for agentic AI coding tools. It targets research on how developers steer tools such as Claude Code, GitHub Copilot, OpenAI Codex, Cursor, and Gemini.

## Problem
- Developers now write project-specific instructions, rules, hooks, and tool settings for coding agents, but researchers lacked a curated multi-tool dataset of these artifacts at scale.
- The missing data limits studies of configuration adoption, context engineering, AI-authored changes, and human-AI collaboration in real repositories.
- Existing datasets focus on AI-generated code, pull requests, or single-tool artifacts, so they do not capture raw configuration contents across tools and mechanisms.

## Approach
- The authors started from 187,304 GitHub repositories in the SEART GitHub Search dataset and filtered them by license, activity, language, repository status, topic patterns, commit count, watchers, and redirects.
- They kept 40,585 actively maintained repositories, then used README content, GitHub Linguist file summaries, external-link summaries, and GPT-5.2 to classify 36,710 as engineered software projects.
- They cloned the engineered repositories and applied documented detection heuristics for 5 tools and 8 configuration mechanisms: Context Files, Skills, Subagents, Commands, Rules, Settings, Hooks, and MCP configurations.
- They stored per-artifact metadata such as file path, creation date, commit count, first and last commit hashes, and for context files, language and AI-authorship signals.
- They also scanned repositories with configuration artifacts for AI-co-authored commits and released the dataset, pipeline, and website.

## Results
- The dataset contains 4,738 repositories with at least one detected configuration artifact, drawn from 36,710 engineered software repositories.
- It includes 15,591 configuration artifacts and the full content of 18,167 configuration files.
- It covers 5 tools: Claude Code in 2,525 repositories, GitHub Copilot in 1,397, Cursor in 466, Gemini in 183, OpenAI Codex in 53, plus 909 repositories with only AGENTS.md.
- Context Files are the dominant mechanism: 9,470 artifacts across 4,463 repositories. Other counts are Skills 2,430 artifacts in 547 repositories, Commands 1,098 in 284, Rules 997 in 298, Subagents 884 in 273, Settings 472 in 447, MCP 138 in 124, and Hooks 102 in 101.
- The dataset includes 148,519 AI-co-authored commits from 3,392 repositories.
- Compared with the authors' prior study, the scope grows from 2,853 to 4,738 repositories, and the improved classification process reduces unsure cases from 2,204 to 152, reported as a 93% reduction.

## Link
- [https://arxiv.org/abs/2605.08435v1](https://arxiv.org/abs/2605.08435v1)
