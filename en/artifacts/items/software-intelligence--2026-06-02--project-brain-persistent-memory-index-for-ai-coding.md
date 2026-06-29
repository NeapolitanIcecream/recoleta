---
source: hn
url: https://github.com/OoneBreath/claude-code-project-brain
published_at: '2026-06-02T23:12:59'
authors:
- Slav_fixflex
topics:
- ai-coding
- project-memory
- claude-code
- code-intelligence
- developer-tools
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Project Brain – Persistent memory index for AI coding

## Summary
Project Brain is a Claude Code skill that keeps project memory in a small Markdown index with linked detail files. It targets repeated context setup, project mix-ups, and wasted tokens in AI coding sessions.

## Problem
- Claude Code users often re-explain architecture, deployment, stack, history, and pitfalls at the start of each session.
- Long always-loaded notes or READMEs can waste context, including cases where users paste a 1000-line README for routine tasks.
- Multi-project work can cause the model to confuse stacks, prior decisions, and completed work across repos.

## Approach
- The skill creates a `.project-brain/` folder with `index.md` as a small map and per-project topic files under `projects/<project>/<topic>.md`.
- Claude reads the index first, then opens one linked topic file only when the user asks about that area.
- `init` detects projects from signals such as `git`, `package.json`, and `pyproject.toml`, then adds a pointer in `CLAUDE.md` so future sessions load the map.
- Status values such as verified, failed, and in-progress record outcomes, while superseded notes keep prior decisions instead of overwriting them.
- A `brain-check` validator catches broken pointers, malformed frontmatter, and index-to-topic status drift.

## Results
- The excerpt reports no benchmark, ablation, user study, or measured token reduction.
- Claimed token benefit: only `index.md` loads eagerly, so per-session context is bounded by the index size rather than the full history or a 1000-line README.
- Claimed recall benefit: after 3 months away from a project, Claude can use stored stack, deployment, decisions, failed attempts, and verified work without the user pasting context again.
- Claimed navigation behavior: a question such as “how did we solve the cache issue?” should load 1 topic file through 1 index pointer instead of reading the whole knowledge base.
- Setup claim: run `install.sh` once per machine, run `init` once per workspace, and one brain can catalog many projects on a server.

## Link
- [https://github.com/OoneBreath/claude-code-project-brain](https://github.com/OoneBreath/claude-code-project-brain)
