---
source: hn
url: https://pub.towardsai.net/from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness-74b4d67b5373?source=friends_link&sk=9e8b13e4920771b5d414db224901bf0e
published_at: '2026-06-12T23:25:57'
authors:
- tacoda
topics:
- mcp
- agentic-tools
- code-intelligence
- software-foundations
- configuration-management
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# From a Single File to an MCP Server: Six Rewrites of My Own Harness

## Summary
This article describes six rewrites of a personal Claude harness, ending with an MCP server that lets agents fetch rules, skills, and live state as structured data. The main claim is that repeated cleanup of a working setup reveals its real shape: structure should travel, while project-specific content should stay local.

## Problem
- A single 1,800-line `CLAUDE.md` file became hard to remember, easy to contradict, and slow to revise.
- Global rules leaked into projects where they did not apply, so the agent loaded irrelevant context and followed mixed instructions.
- A file-only harness could not share defaults across teams, track versions, or expose live state to the agent.

## Approach
- Split one large config into per-topic files, then moved rules to scoped paths so location controlled activation.
- Separated always-loaded rules, named skills, and slash commands into different directories and file types.
- Built Sellier as a CLI scaffold for project harnesses, then replaced it with Keystone, which supports project types, agent selection, migrations, plugins, team/org/project layers, and strict cascade rules.
- Repackaged Keystone as `keystone-mcp`, with tools for context lookup and scaffolding, prompts for workflows like bootstrap and audit, and resources for status, verify, and budget data.

## Results
- The author reports that the global config shrank to about one-third of its prior size after scope was moved into subdirectory files.
- The agent’s behavior improved after contradictory rules stopped living in the same file, and rules no longer fought each other.
- Sellier exposed three clear limits: one starter set did not fit different project types, it did not support team customization, and it had no update path.
- Keystone added typed scaffolding, migrations, plugins, cascade resolution, and per-agent rendering; the article gives no benchmark numbers for these changes.
- `keystone-mcp` lets an agent call `keystone_get_context(topic)`, `keystone_list_topics()`, `keystone_harness_bootstrap()`, and fetch resources like `keystone://harness/verify`, but the article provides no quantitative evaluation of speed, accuracy, or adoption.

## Link
- [https://pub.towardsai.net/from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness-74b4d67b5373?source=friends_link&sk=9e8b13e4920771b5d414db224901bf0e](https://pub.towardsai.net/from-a-single-file-to-an-mcp-server-six-rewrites-of-my-own-harness-74b4d67b5373?source=friends_link&sk=9e8b13e4920771b5d414db224901bf0e)
