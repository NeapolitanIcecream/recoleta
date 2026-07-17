---
source: arxiv
url: https://arxiv.org/abs/2607.15143v1
published_at: '2026-07-16T15:47:19'
authors:
- Aadesh Bagmar
- Pushkar Saraf
topics:
- code-intelligence
- ai-coding-agents
- software-supply-chain
- package-security
- automated-software-production
relevance_score: 0.96
run_id: materialize-outputs
language_code: en
---

# Setup Complete, Now You Are Compromised: Weaponizing Setup Instructions Against AI Coding Agents

## Summary
The paper shows that AI coding agents can turn attacker-edited setup documentation into package-install-time code execution. Across production harnesses, security depends on the harness-model combination, while a deterministic pre-install check for package names, sources, and versions closes most of the observed gap.

## Problem
- Coding agents often read README files, dependency specifications, and Makefiles, then install packages without verifying their names, registries, or vulnerability status.
- An attacker who changes only setup documentation can cause installation of a typosquat, a package from an untrusted registry, or a vulnerable version, executing code with the developer's permissions.
- This matters because autonomous setup removes the brief human review that might detect a misspelled package or unfamiliar source; the risk also extends to CI and build environments.

## Approach
- The authors evaluate 12 setup scenarios spanning five attack classes: package-name confusion, registry/source attacks, vulnerable versions, configuration poisoning, and attacker-controlled error messages.
- They run the scenarios across nine harness-model configurations involving four coding-agent harnesses and seven models, using production tools such as Claude Code, Copilot CLI, Codex CLI, and Cursor.
- Each agent receives the same generic setup request and must create a virtual environment, install dependencies, and verify the project; a run counts as caught only when the agent avoids or flags the attack before installation.
- The study compares model and harness effects, tests Python attacks on npm and Cargo, and evaluates security-oriented prompts plus a deterministic pre-install hook that checks names, sources, and versions.

## Results
- Name-based attacks were generally detected: obvious typosquats such as `tranformers` were caught at or near 30/30 runs in many configurations, but plausible separator confusion such as `azurecore` versus `azure-core` produced inconsistent detection.
- Source attacks were missed almost everywhere. In the controlled harness ablation, changing only the harness changed one untrusted-registry result from 10/10 caught to 9/30 caught (`p = 1.1 × 10^-4`); for the HTTPS variant, the comparison reversed from 0/10 to 10/10 caught (`p = 1.1 × 10^-5`).
- Vulnerable-version attacks were especially difficult: the baseline Claude Code result for the 10-package CVE battery was 0/30 caught, while a version-focused security prompt improved the comparison from 2/10 to 10/10 (`p < 10^-3`).
- The study reports that source blind spots reproduced on npm and Cargo, where nearly every model installed untrusted dependencies; pre-install refusal appeared mainly when a frontier model and an external source were combined.
- Security prompts recovered only the attack dimension they named, whereas the deterministic pre-install check verifying names, sources, and versions closed most of the observed gap; benign controls produced zero spurious security warnings.

## Link
- [https://arxiv.org/abs/2607.15143v1](https://arxiv.org/abs/2607.15143v1)
