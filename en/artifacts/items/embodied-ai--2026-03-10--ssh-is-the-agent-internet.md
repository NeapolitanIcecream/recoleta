---
source: hn
url: https://rolandsharp.com/ssh-is-the-agent-internet/
published_at: '2026-03-10T23:49:52'
authors:
- epscylonb
topics:
- ssh
- ai-agents
- agent-communication
- git-based-platform
- developer-infrastructure
relevance_score: 0.12
run_id: materialize-outputs
language_code: en
---

# SSH Is the Agent Internet

## Summary
This article argues for using **SSH + git** as the native internet stack for AI agents, instead of continuing to rely on the HTTP/API ecosystem designed for browsers. Through a prototype called **sshmail**, the author demonstrates that agents can handle identity, communication, and storage using only SSH commands, the filesystem, and repositories.

## Problem
- The article argues that the existing **HTTP/Web API** stack was designed for browsers and document retrieval, and introduces too much additional complexity when used for agent application interactions, such as OAuth, API keys, JSON protocols, TLS certificates, retries, and rate-limit handling.
- For AI agents, the only foundational capabilities actually needed are **authentication, encrypted communication, and persistent storage**; continuing to use the Web stack increases integration cost, fragility, and maintenance burden.
- This matters because if interaction protocols between agents, and between agents and services, are too heavy, they will slow down automated collaboration, discovery, task execution, and data portability.

## Approach
- The core idea is simple: treat **SSH as the native network protocol for agents**. Identity is an SSH key pair, communication is an authenticated and encrypted remote command, and storage is handled through a **git repo** and the filesystem.
- The author implemented a prototype system called **sshmail**: based on **Wish** (Charmbracelet's SSH server framework) and **SQLite**, a single SSH server binary provides messaging, inboxes, polling, groups, rooms, and file transfer capabilities.
- A client is not required, because “the server is the CLI”: users or agents can interact directly by running commands such as `ssh sshmail.dev send ajax "done"`, without needing an SDK, browser, or dedicated installer.
- To make data easier for agents to process, messages can be synced into **Markdown files**; the broader vision is for each agent to have an **SSH-hosted git repository** containing directories such as profile, resume, blog, and messages, where pull, commit, and PR become general mechanisms for discovery, application, review, and collaboration.
- The article further envisions unifying hiring, publishing, blogging, chat, archiving, and backup on top of **SSH + git + SQLite**, forming a platform that is “GitHub + Slack + Substack, but without HTTP.”

## Results
- No formal paper-style benchmarks, experimental data, or statistical metrics are provided, so there are **no quantitative results** available for rigorous comparison with existing HTTP/API systems.
- The strongest empirical claim is: **“Within hours of launching, AI agents were using sshmail autonomously”**—that is, within hours of launch, AI agents were already reading and writing messages and replying on their own, though no counts, task success rates, or controlled experiments are provided.
- The prototype currently supports specific features including **direct messages, boards, private rooms, groups, file transfers**; the implementation is **one binary, one deploy**, with **SQLite** used for backend storage.
- The key interaction flow described in the article is highly simplified: for example, sending a message requires only a single `ssh ... send ...` command; the author claims this avoids the entire set of components typically required by HTTP-based approaches, including **TLS cert, DNS, API endpoint, JSON serialization, auth token, token refresh, rate limit handling, client library**.
- The author also claims that agents have already used this SSH channel for several real collaborative behaviors, such as **discovering one another, suggesting features, discussing licensing, submitting PRs, stress-testing group chat, and building a Web UI**, but these remain anecdotal observations rather than systematic evaluation.

## Link
- [https://rolandsharp.com/ssh-is-the-agent-internet/](https://rolandsharp.com/ssh-is-the-agent-internet/)
