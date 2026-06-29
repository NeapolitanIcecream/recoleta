---
source: hn
url: https://vexjoy.com/posts/the-crypto-coin-was-the-tell/
published_at: '2026-05-23T22:13:04'
authors:
- AndyNemmity
topics:
- ai-agent-security
- npm-supply-chain
- code-agents
- claude-code
- developer-tools
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# The Crypto Coin was the tell – thoughts on GSD, and it's crypto rugpull

## Summary
The post warns users to uninstall the original Get Shit Done npm packages after the creator launched and drained a $GSD token, then disappeared while retaining npm publish access. The main risk is the update channel for local AI agents that can run shell commands on a developer machine.

## Problem
- The original maintainer still controls the publish path for `get-shit-done-cc` and `@gsd-build/sdk` after the reported rug pull.
- GSD agents can run with shell and bash permissions, so a malicious package update could execute code on a user’s machine.
- npm does not revoke package credentials when social trust collapses, and a community fork does not protect users who keep installing the old package names.

## Approach
- The post gives removal commands for global npm installs, `npx` use, and local installs.
- It tells users to inspect `~/.npm/_npx/` and `.claude` for leftover GSD directories.
- It points users who still want the workflow to `open-gsd/get-shit-done-redux`, which removed the original creator from the update path.
- It compares npm package trust with a git-based install model where users can inspect files and see changes before running them.
- The author argues for smaller, user-owned Claude Code setups based on local markdown, scripts, and workflow-specific agent files.

## Results
- The text has no benchmark, dataset, or model performance result; it is an incident analysis and security guidance post.
- Concrete claim: the community fork `open-gsd/get-shit-done-redux` was created overnight and audited after the $GSD incident.
- Concrete claim: the original npm packages were not known to be malicious at publication time, but the original maintainer still held publish access.
- Concrete system details: the author’s `vexjoy-agent` setup has 44 domain specialist agents, 121 workflow skills, and 77 lifecycle hooks.
- Concrete install details: the author’s setup uses `git clone`, `cd`, and `./install.sh`, then deploys across Claude Code, Codex, Gemini, and Factory.

## Link
- [https://vexjoy.com/posts/the-crypto-coin-was-the-tell/](https://vexjoy.com/posts/the-crypto-coin-was-the-tell/)
