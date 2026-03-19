---
source: hn
url: https://github.com/harveyrandall/bsky-cli
published_at: '2026-03-07T22:55:36'
authors:
- harveyrandall
topics:
- cli-tool
- bluesky
- typescript
- developer-tools
relevance_score: 0.0
run_id: materialize-outputs
language_code: en
---

# Show HN: Bsky-CLI – A full-featured CLI client for Bluesky

## Summary
This is a Bluesky command-line client written in TypeScript, aimed at providing a nearly full-platform-feature CLI experience. It is more like a developer tool/product release than a research paper, and it does not provide experimental evaluation results.

## Problem
- The problem it aims to solve is that Bluesky lacks a full-featured command-line client that is convenient for scripting, terminal-based operation, and multi-account management.
- This matters because developers, power users, and CI/automation scenarios need to post, retrieve content, interact, and manage accounts without relying on a graphical interface.
- The existing excerpt also suggests requirements for easy deployment and cross-platform use, including global installation, standalone binaries, and environment-variable-based configuration.

## Approach
- The core approach is straightforward: package common Bluesky operations into a unified set of CLI subcommands, such as timeline, posting, replying, liking, reposting, searching, notifications, and profile updates.
- It supports usage through multiple installation methods, including npm/yarn/pnpm/bun, Homebrew, and standalone binaries for macOS/Linux/Windows, lowering the deployment barrier.
- It uses a configuration precedence mechanism to make automation friendly: `CLI args > environment variables > config file`, and supports direct authentication from environment variables, making it suitable for scripts and CI.
- It supports isolated multi-account management via `--profile/-p`, allowing users to switch between personal/work accounts.
- It provides shell completion, test/build commands, and a build-from-source workflow, indicating that it is positioned as a maintainable, extensible developer tool.

## Results
- The text **does not provide any quantitative experimental results**; there are no datasets, baseline methods, accuracy, latency, throughput, or user study figures available for comparison.
- The strongest concrete claim given is "full-featured CLI client for Bluesky," and it lists many supported commands, such as `timeline/tl`, `stream`, `thread`, `post`, `reply`, `quote`, `delete`, `like`, `repost`, `bookmarks`, `follow/unfollow`, `search`, `profile-update`, `notifs`, `invite-codes`, `app-password`, `report`, and `mod-list`.
- In terms of compatibility, it explicitly requires `Node.js >= 22` and provides standalone binary releases for macOS, Linux, and Windows.
- In terms of account and automation capabilities, it supports multi-profile management, as well as environment-variable-based authentication and configuration override rules, making it suitable for scripting.
- The roadmap/unimplemented features are also clearly listed, including direct messages, list management, starter packs, moderation lists, post labels, automatic alt-text, OAuth login support, and Docker BuildKit binary builds.

## Link
- [https://github.com/harveyrandall/bsky-cli](https://github.com/harveyrandall/bsky-cli)
