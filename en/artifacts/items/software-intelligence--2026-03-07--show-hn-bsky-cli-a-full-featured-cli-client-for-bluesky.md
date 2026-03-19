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
- social-media-client
relevance_score: 0.19
run_id: materialize-outputs
language_code: en
---

# Show HN: Bsky-CLI – A full-featured CLI client for Bluesky

## Summary
This is a full-featured Bluesky command-line client written in TypeScript, aimed at terminal users, scripts, and CI scenarios. It unifies common Bluesky social operations into an installable, multi-account-manageable, cross-platform CLI tool.

## Problem
- The problem it solves is: how to fully access and operate Bluesky from the command line without relying on a graphical interface or scattered scripts.
- This matters because developers, automation scripts, and CI workflows need a composable, reusable social platform interface that can be configured via environment variables.
- The excerpt emphasizes a “full-featured CLI client,” indicating the goal is to cover high-frequency functions such as posting, timelines, interactions, profile management, and notifications.

## Approach
- The core approach is to build a unified `bsky` command that maps Bluesky’s main capabilities into subcommands such as timeline, posting, replying, quoting, liking, reposting, following, searching, notifications, and profile updates.
- The authentication mechanism supports interactive login, command-line arguments, standard input, and environment variables, and clearly defines the configuration precedence as “CLI args > environment variables > config file,” making it convenient for scripted use.
- It supports multi-account configuration through `--profile` / `-p`, allowing users to switch between personal and work accounts.
- It provides standalone binaries for macOS, Linux, and Windows, as well as installation through npm/yarn/pnpm/bun/Homebrew, lowering the barrier to use.
- It also provides shell completion, test/build scripts, and a way to build from source, improving the development and contribution experience.

## Results
- In terms of feature coverage, the excerpt lists **30+ commands/subcommands**, including timeline, stream, thread, post, reply, quote, delete, like, repost, bookmarks, follow, search, profile, notification, app-password, report, mod-list, etc., showing relatively complete Bluesky CLI capabilities.
- In terms of platform support and distribution, it supports **4 JavaScript package manager installation methods** (npm, yarn, pnpm, bun) and **1 Homebrew installation method**, and provides standalone binaries for **3 major desktop platforms** (macOS, Linux, Windows).
- The runtime requirement is **Node.js >= 22**; it also supports building from source, global linking, type checking, test execution, and coverage commands, but the excerpt **does not provide specific test coverage figures**.
- For account management, it explicitly supports **multiple profiles**, enabling management of multiple Bluesky accounts within the same tool.
- The roadmap / not-yet-supported features list **6 items**: Direct messages, List creation and management, Starter packs, Moderation lists, Post labels, Auto alt-text for images and videos, as well as OAuth login support, indicating it is still expanding.
- The excerpt **does not provide benchmarks, performance metrics, user research, or quantitative comparisons with other Bluesky clients**; the strongest concrete claims are its “full-featured” positioning, cross-platform distribution, and broad command coverage.

## Link
- [https://github.com/harveyrandall/bsky-cli](https://github.com/harveyrandall/bsky-cli)
