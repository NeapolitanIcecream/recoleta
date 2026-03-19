---
source: hn
url: https://github.com/cassmtnr/claude-code-starter
published_at: '2026-03-09T23:24:44'
authors:
- cassmtnr
topics:
- developer-tooling
- code-intelligence
- ai-agent-config
- repository-analysis
- cli-automation
relevance_score: 0.89
run_id: materialize-outputs
language_code: en
---

# Claude Code Starter CLI

## Summary
This is an intelligent CLI for existing code repositories that guides Claude to read real source code and automatically generate project-specific Claude Code configurations and documentation. Its value lies in upgrading generic scaffolding into a customized AI development environment based on the codebase's actual architecture, conventions, and tech stack.

## Problem
- Traditional static scaffolding tools or templates cannot truly understand a project's source code, so the AI configurations, documentation, and workflows they generate are often too generic and disconnected from the real architecture.
- It is costly for developers to manually prepare project context for AI coding assistants, such as architecture descriptions, rules, commands, and agent roles, and important details are easy to miss.
- If an AI assistant does not understand the codebase's languages, frameworks, patterns, and conventions, its code generation, review, and collaboration effectiveness will decline significantly.

## Approach
- First scan files such as `package.json`, configuration files, and lockfiles in the repository to detect languages, frameworks, toolchains, and project patterns.
- Based on the detected tech stack, automatically generate supporting files: `skills`, `agents`, `rules`, `commands`, and `.claude/settings.json`.
- Launch Claude CLI so Claude can directly read the actual source files and understand the project's architecture, conventions, and domain knowledge, rather than relying only on static templates.
- Write the results of the deep analysis into `CLAUDE.md`, forming comprehensive documentation for the current project and serving as the context entry point for subsequent `claude` workflows.
- Provide CLI modes such as interactive, non-interactive, force overwrite, and verbose logging to facilitate integration into existing development workflows.

## Results
- The text does not provide standard benchmarks, accuracy metrics, or systematic quantitative comparisons with other tools.
- In the example run, for an existing project containing **42 source files**, the tool generated **15 files**.
- The example identified the tech stack as **TypeScript + Next.js + bun + vitest**, and further generated **9 skills, 2 agents, and 2 rules**.
- The outputs include a project-specific `CLAUDE.md`, `.claude/settings.json`, multiple command files (such as `/task`, `/status`, `/done`, `/analyze`, `/code-review`), and agent files (such as `code-reviewer` and `test-writer`).
- Its strongest concrete claim is that, unlike static scaffolding, Claude actually reads the codebase source and uses that to generate customized documentation and configuration tailored to the project's architecture, patterns, conventions, and domain knowledge.

## Link
- [https://github.com/cassmtnr/claude-code-starter](https://github.com/cassmtnr/claude-code-starter)
