---
source: hn
url: https://github.com/manuelschipper/nah/
published_at: '2026-03-11T23:26:25'
authors:
- schipperai
topics:
- agent-safety
- permission-guard
- developer-tools
- code-assistant
- context-aware-security
relevance_score: 0.85
run_id: materialize-outputs
language_code: en
---

# Show HN: A context-aware permission guard for Claude Code

## Summary
nah is a context-aware permission guard for Claude Code that uses structured rules, rather than simple per-tool allow/deny decisions, to judge the true risk of each tool call. It aims to preserve automation efficiency while blocking dangerous file operations, key reads, data exfiltration, and malicious command execution.

## Problem
- The existing Claude Code permission mechanism mainly works on an allow-or-deny basis per tool, which is too coarse-grained to distinguish between safe and dangerous operations within the same tool.
- Relying only on maintaining a deny list is hard to make comprehensive across complex contexts, and the model may still bypass static restrictions, creating risks such as deleting files, leaking credentials, and executing malicious scripts.
- This matters because developer agents need greater autonomy, but fully open modes such as `--dangerously-skip-permissions` significantly increase the probability of damaging the local environment and sensitive data.

## Approach
- Before each tool execution, nah intercepts the call as a PreToolUse hook and first uses a **deterministic structured classifier** to judge by the “actual action type,” rather than crudely allowing based on the command name or tool name.
- The classifier makes decisions using context, such as the target path, command arguments, whether the written content contains private keys, whether it involves `git push --force`, and whether it accesses sensitive locations like `~/.aws` / `~/.ssh`.
- For cases the classifier cannot determine clearly, an LLM can optionally be connected to handle only the remaining “ask” decisions; and `max_decision: ask` can be set to prevent the LLM from escalating high-risk operations to direct allow.
- The system supports both global and project-level configuration: a project `.nah.yaml` can only tighten policies, not relax them, to prevent malicious repositories from bypassing protections via configuration; it also provides about 20 built-in action types, logging, testing, and command-line tuning capabilities.

## Results
- The text does not provide formal paper-style benchmark evaluations, accuracy, false-positive rates, or quantitative comparison results with other permission systems.
- The most specific demonstration result given by the author is: **25** live security cases covering **8** threat categories, runnable in about **5 minutes**, including remote code execution, data exfiltration, obfuscated commands, and others.
- The system claims the rule-based classification runs at the **millisecond level**, and that **every tool call** first goes through the deterministic classifier before optionally entering the LLM decision chain depending on the situation.
- In terms of built-in coverage, the project states it has **20** built-in action types, and the default `full` profile covers scenarios such as shell, git, packages, and containers.
- Example capabilities include: allowing `git push`, while triggering interception/confirmation for `git push --force`; allowing cleanup with `rm -rf __pycache__`, while blocking `rm ~/.bashrc`; allowing reads of `./src/app.py`, while intercepting reads of `~/.ssh/id_rsa`; and inspecting and blocking writes whose content contains private keys.

## Link
- [https://github.com/manuelschipper/nah/](https://github.com/manuelschipper/nah/)
