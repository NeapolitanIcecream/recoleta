---
source: arxiv
url: https://arxiv.org/abs/2606.09090v1
published_at: '2026-06-08T06:36:38'
authors:
- Christoph Treude
- Sebastian Baltes
topics:
- ai-coding-assistants
- context-files
- documentation-consistency
- code-intelligence
- software-maintenance
- human-ai-interaction
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Context Rot in AI-Assisted Software Development: Repurposing Documentation Consistency for AI Configuration Artifacts

## Summary
The paper defines context rot: stale AI coding-assistant configuration files that no longer match the repository. It shows that existing documentation consistency checks can detect references to deleted or renamed code elements.

## Problem
- AI coding assistants read persistent project files such as `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, `copilot-instructions.md`, and `GEMINI.md`; stale content can make the assistant import deleted modules, call missing functions, or follow abandoned conventions.
- These files change outside compiler and test feedback loops, so drift can persist without a visible failure.
- The problem matters because prior work cited in the paper links `AGENTS.md` files to lower agent runtime and token use, so inaccurate configuration can reduce AI-assisted development quality and efficiency.

## Approach
- The paper names the failure mode as context rot: divergence between AI configuration artifacts and the current codebase, tools, architecture, or workflow.
- It reuses DOCER, a README/wiki consistency checker, without tuning it for AI configuration files.
- DOCER extracts candidate code elements from the current configuration file, checks whether each element existed when the file was first committed, then checks whether it still exists at repository HEAD.
- Elements present at the first commit and absent at HEAD are classified as stale; elements absent from both snapshots are discarded as noise.
- The study focuses on referential rot and maps other documentation-consistency methods to future checks for behavioral instructions, MCP tool descriptions, architectural claims, and dependency references.

## Results
- The sample covers 356 repositories and 612 AI configuration files, drawn from 8,213 eligible files in 4,420 repositories; the sample targets 95% confidence with a 5% margin of error at repository level.
- DOCER extracted 29,454 candidate elements and verified 18,048 references that existed when the configuration file was first committed.
- It found 230 stale references, equal to 1.27% of verified references; 17,818 references, or 98.73%, were still valid at HEAD.
- At repository level, 82 of 356 repositories had at least one stale reference, or 23.0%, with a 95% CI of 18.8–27.2%.
- Manual inspection of 50 stale classifications found 32 genuine cases, or 64%; 12 were false positives and 6 were ambiguous.
- Stale rates by file type were 1.42% for `CLAUDE.md`, 1.04% for `AGENTS.md`, 1.42% for Copilot instruction files, 0.75% for `GEMINI.md`, 0.00% for `.cursorrules`, and 2.99% for other files.

## Link
- [https://arxiv.org/abs/2606.09090v1](https://arxiv.org/abs/2606.09090v1)
