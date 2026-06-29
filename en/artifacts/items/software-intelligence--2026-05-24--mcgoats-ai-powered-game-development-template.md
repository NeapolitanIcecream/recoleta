---
source: hn
url: https://github.com/Totes-MickGOATs/mcgoats-game-template
published_at: '2026-05-24T22:21:25'
authors:
- lastdong
topics:
- ai-assisted-development
- game-development
- ci-cd
- code-agents
- tdd
- github-automation
relevance_score: 0.78
run_id: materialize-outputs
language_code: en
---

# Mcgoats AI-powered game development template

## Summary
Mcgoats is a GitHub template that sets up AI-assisted game development with Claude Code, CI, branch protection, auto-merge, and TDD rules. It targets teams that want game projects to start with guarded automation instead of ad hoc repo setup.

## Problem
- New game repos often lack CI, branch rules, test habits, and AI-agent instructions, which causes unsafe merges and inconsistent project structure.
- AI coding agents need repo-specific commands, docs, hooks, and guardrails to make useful changes without bypassing review.
- The template matters because game projects can accumulate build and workflow debt early, especially when engine setup, tests, and GitHub rules are added later.

## Approach
- A `/setup` flow in Claude Code guides engine selection, GitHub setup, branch protection, CI verification, and first feature-branch work.
- The repo uses 3 main-branch guards: a Claude Code PreToolUse hook, a git pre-commit hook, and GitHub branch protection.
- Development runs through worktree-based feature branches, pull requests, FIFO squash auto-merge triggered by a `ready-to-merge` label, and post-merge test checks.
- Engine modules copy CI, lint, hooks, skills, and configs for Godot, Unity, or Unreal, then remove the setup module.
- Claude-facing files include `CLAUDE.md`, per-directory docs, system manifests, hooks, commands, statusline support, and agent skills loaded as needed.

## Results
- No benchmarked research results are provided; the excerpt gives implementation claims and setup features, with no accuracy, productivity, or defect-rate measurements.
- The template supports 3 engines: Godot, Unity, and Unreal; Godot support is reported as used across a shipping game project, while Unity and Unreal are starter modules.
- It lists a 3-layer main-branch protection path: Claude Code hook, git pre-commit hook, and GitHub branch protection.
- It includes 5 engine-agnostic skills plus engine-specific skills, reusable CI workflows, post-merge full-test runs, and issue creation on post-merge failure.
- Version requirements include Python 3.14+, Godot 4.x, Unity 2022+, and Unreal 5.x.

## Link
- [https://github.com/Totes-MickGOATs/mcgoats-game-template](https://github.com/Totes-MickGOATs/mcgoats-game-template)
