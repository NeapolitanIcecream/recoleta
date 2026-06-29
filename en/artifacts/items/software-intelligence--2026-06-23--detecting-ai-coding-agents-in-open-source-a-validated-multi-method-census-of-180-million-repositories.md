---
source: arxiv
url: https://arxiv.org/abs/2606.24429v1
published_at: '2026-06-23T11:05:42'
authors:
- Arsham Khosravani
- Audris Mockus
topics:
- ai-coding-agents
- open-source-mining
- software-supply-chain
- code-intelligence
- repository-metadata
- agent-detection
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Detecting AI Coding Agents in Open Source: A Validated Multi-Method Census of 180 Million Repositories

## Summary
This paper measures AI coding agent traces across more than 180 million Git repositories and shows that single-signal studies miss most activity. Its main claim is that commit, pull-request, author, and configuration-file signals identify different agent populations and work types.

## Problem
- AI coding agents often leave weak or inconsistent traces, so open-source studies can undercount AI-assisted code.
- Reliable detection matters for software supply-chain audits, prevalence measurement, and studies of code quality or project velocity.
- Prior censuses based on bot accounts, pull requests, or configuration files cover only one channel.

## Approach
- The authors use World of Code snapshots V2412, V2510, and V2604, covering December 2024 through April 2026 and more than 180 million repositories.
- They define four trace types: centralized bot accounts, commit-message signatures, human author-name patterns, and configuration-file-only traces.
- They scan author maps, commit messages, and file-to-project maps; resolve human aliases; keep bot identities separate; and defork projects before counting adoption.
- They validate every detector cell with 495 hand labels, report per-cell precision with Wilson confidence intervals, and compare their commit census with the AIDev pull-request census.

## Results
- In V2510, multi-method Claude Code detection finds 850,157 commits. Bot-account lookup alone finds 28,154 commits, a 30x relative-recall gap; the union is still a lower bound.
- In V2510, Copilot SWE Agent has 1,127,201 commits across 85,739 projects, Claude Code has 850,157 commits across 17,295 projects, Devin has 215,998 commits, and Jules has 209,911 commits.
- In V2604, commit-attributed agents produce 1,772,677 commits. Claude Code contributes 886,122 commits, or 50%; Replit contributes 314,779, Jules 215,804, and Aider 196,132.
- Commit-attributed AI agents exceed 320,000 commits per month at the March 2026 peak. Within projects with AI-attributed commits, the AI share rises from 1.6% of non-bot activity in December 2025 to 6.7% in March 2026.
- The V2604 configuration-file census finds 1,699,950 configuration-file occurrences. Claude accounts for 888,177 occurrences across 21,078 projects, GitHub Copilot for 211,166 occurrences, and Codex for 134,810 occurrences.
- Compared with AIDev, a pull-request census misses 79% of commit-detected Claude Code adopters, while a commit-based census misses nearly all Codex adopters.

## Link
- [https://arxiv.org/abs/2606.24429v1](https://arxiv.org/abs/2606.24429v1)
