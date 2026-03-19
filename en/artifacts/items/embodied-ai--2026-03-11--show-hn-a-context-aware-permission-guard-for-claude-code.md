---
source: hn
url: https://github.com/manuelschipper/nah/
published_at: '2026-03-11T23:26:25'
authors:
- schipperai
topics:
- ai-safety
- permission-guard
- developer-tools
- context-aware-security
- llm-agent
- policy-enforcement
relevance_score: 0.03
run_id: materialize-outputs
language_code: en
---

# Show HN: A context-aware permission guard for Claude Code

## Summary
nah is a context-aware permission guard for Claude Code that replaces simple per-tool allow/deny with classification based on **what an action actually does**. It aims to automatically allow safe operations, block dangerous ones, and hand ambiguous cases to the user or an optional LLM, without completely disabling permission protections.

## Problem
- The existing Claude Code permission mechanism is mainly binary allow/deny at the tool level, but real risk depends on **context**. The same command can have very different risk depending on its parameters, path, and content.
- Maintaining only a deny list does not scale and can be bypassed by the model through variants, detours, or chained operations, creating risks such as file deletion, key exfiltration, and malicious script execution.
- Users need a permission control method that is safer than `--dangerously-skip-permissions` while also avoiding frequent interruptions to normal development workflows.

## Approach
- Before each tool call executes, it intercepts the request through a PreToolUse hook and first uses a **deterministic structured classifier** to judge, in milliseconds, what the call is actually doing rather than only looking at the tool name.
- It maps calls to about 20 built-in action types, such as file deletion, git history rewriting, and network access, then decides `allow`, `ask`, or `block` based on default or user-defined policies.
- It uses **contextual information** when judging file reads and writes, for example whether the target path is sensitive, whether written content looks like a private key, or whether a command contains dangerous patterns like `curl ... | sh` or `git push --force`.
- For ambiguous cases that deterministic rules cannot resolve, it can optionally use an LLM to handle only the remaining `ask` decisions; the LLM’s authority can also be capped so it cannot grant anything above `ask`.
- Configuration uses layered global config plus project-level `.nah.yaml`, where project config can only **tighten** policy and not relax it, reducing the risk that a malicious repository could allow dangerous commands through configuration.

## Results
- The article does not provide formal benchmarks, paper-style experiments, or quantitative metrics such as accuracy or false positive rate, so there is **no verifiable quantitative performance data**.
- The system claims to run deterministic classification before every tool call, with rule execution taking **milliseconds**, and to cover **20** built-in action types.
- It provides a security demo with **25** live cases across **8** threat categories, such as remote code execution, data exfiltration, and obfuscated commands; the full demo takes about **5 minutes**.
- The qualitative examples suggest it can distinguish between similar operations with different risk levels: for example, `git push` can be allowed, while `git push --force` triggers a prompt or block; `rm -rf __pycache__` can be allowed, while `rm ~/.bashrc` is blocked; reading `./src/app.py` can be allowed, while reading `~/.ssh/id_rsa` is denied or requires confirmation.
- It claims to work out of the box with zero configuration, while also supporting minimal or blank-policy modes and fallback cascades across multiple LLM providers for ambiguous decisions.

## Link
- [https://github.com/manuelschipper/nah/](https://github.com/manuelschipper/nah/)
