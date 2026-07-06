---
source: hn
url: https://fly.io/blog/building-agents-that-dont-break-themselves/
published_at: '2026-07-05T23:54:43'
authors:
- ryantsuji
topics:
- agent-sandboxing
- software-agents
- command-execution
- credential-isolation
- checkpoint-rollback
relevance_score: 0.74
run_id: materialize-outputs
language_code: en
---

# Building Agents That Don't Break Themselves

## Summary
The article recommends keeping the agent process durable while sending risky shell commands to separate Fly.io Sprites. This split protects the agent host, limits credential exposure, and lets failed command runs roll back from checkpoints.

## Problem
- Agents need shell access to run tests, edit files, install dependencies, apply migrations, and inspect systems, but model-generated commands can delete files, damage toolchains, or affect other users.
- Putting the whole agent in one sandbox leaves a lifecycle conflict: the agent needs persistent memory and history, while command execution should be disposable.
- Multi-user agents need per-user command execution without storing long-lived user credentials on shared disk.

## Approach
- Keep the agent loop on a stable host, such as a Fly Machine, VPS, laptop, or long-lived Sprite, and run shell commands in a separate Sprite.
- SpriteDoc creates 1 Sprite per user session, uploads source trees on first filesystem use, installs needed CLIs, and runs later commands for that session in the same isolated sandbox.
- SpriteDoc injects a user's Fly token into the environment only for a single `flyctl` command, then removes it when the command returns.
- Hermes Agent uses a Sprite backend where each task can keep its own Sprite, so installed tools and task state can persist across sessions.
- Risky steps can create Sprite checkpoints before execution, then restore the prior filesystem and toolchain state after a bad command.

## Results
- The excerpt gives no benchmark table, dataset, baseline, accuracy metric, or task-success rate.
- SpriteDoc uses 1 shared Node.js agent runtime while giving each user session its own Sprite for command execution.
- The credential design keeps 0 long-lived user tokens at rest inside the Sprite; the token exists only in the environment for 1 command.
- Hermes can run inside 1 Sprite while dispatching commands to a second Sprite with a different machine id and boot, proving command execution can be isolated from the agent's own runtime.
- In the rollback example, an agent deletes `/root/app`, `/usr/bin/python3`, and `/usr/bin/git`; checkpoint restore brings back 2 migration files and `git version 2.51.0` in about 9 seconds.
- Idle Sprites move through warm and cold states and can be torn down, so inactive sessions avoid paying for a running box.

## Link
- [https://fly.io/blog/building-agents-that-dont-break-themselves/](https://fly.io/blog/building-agents-that-dont-break-themselves/)
