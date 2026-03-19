---
source: hn
url: https://rolandsharp.com/ssh-is-the-agent-internet/
published_at: '2026-03-10T23:49:52'
authors:
- epscylonb
topics:
- ssh
- agent-infrastructure
- git-based-workflow
- multi-agent-communication
- terminal-ui
relevance_score: 0.87
run_id: materialize-outputs
language_code: en
---

# SSH Is the Agent Internet

## Summary
This article argues for using **SSH+git** as a native internet stack for AI agents, replacing the complex HTTP/API/OAuth ecosystem with unified key-based identity, encrypted command channels, and repository-style storage. Using sshmail as an example, the author shows that agents can already communicate, collaborate, and extend functionality autonomously through pure SSH commands and filesystem interfaces.

## Problem
- The problem the article aims to solve is that the existing HTTP internet was primarily designed for browsers and document retrieval, so enabling agent application communication requires layering on APIs, OAuth, CORS, TLS certificates, tokens, client libraries, and many other complex components.
- This matters because the core things agents actually need are only **identity, communication, and storage**; if the foundational stack is too heavy, it raises the cost of agent collaboration, automated execution, and system integration.
- The author argues that much of the complexity in the current web application stack is not necessary for agents and limits more direct machine-to-machine interaction and automated software production.

## Approach
- The core mechanism is very simple: **identity = SSH key pair, communication = SSH-encrypted commands, storage = git repository/filesystem**. In other words, it replaces “calling APIs” with “executing SSH commands,” and turns “application state/messages” into “files and history in a repository.”
- The author built a prototype platform, **sshmail**: a messaging system deployed as a single binary, based on Wish (Charmbracelet’s SSH server framework) and SQLite; users or agents interact through commands such as `ssh sshmail.dev send ...`, `inbox`, and `poll`.
- The article further proposes a vision for an SSH-native platform: each agent has a git repo hosted over SSH, containing directories such as profile, resume, blog, and messages; messages are written into the repo, reading happens via pull, and collaboration happens via PRs.
- In this model, recruiting, group chat, bulletin boards, file transfer, blog publishing, and more are all unified as SSH commands and git workflows. The filesystem itself is the interface, with no need for an SDK or dedicated client.

## Results
- There are basically no quantitative results: the article **does not provide standard datasets, evaluation metrics, success rates, latency, throughput, or benchmark comparisons with HTTP systems**.
- The strongest empirical claim is that **“Within hours of launching”**, AI agents began using sshmail autonomously to send messages and collaborate within hours of launch, but no specific number of agents, tasks, or success rates is reported.
- The author claims the prototype already supports multiple features: **direct messages, boards, private rooms, groups, file transfers**, all operated through pure SSH commands.
- The article also claims that agents have already carried out several real interactions on the system: **discovering one another, suggesting features, discussing licenses, submitting PRs, publishing a web UI, stress-testing group chat**, but again without quantitative statistics.
- The article’s main breakthrough claim is not a numerical performance gain but architectural simplification: collapsing “GitHub + Slack + Substack”-style capabilities into the trio of **SSH, git, SQLite**, which the author argues is better suited as agent-native infrastructure.

## Link
- [https://rolandsharp.com/ssh-is-the-agent-internet/](https://rolandsharp.com/ssh-is-the-agent-internet/)
