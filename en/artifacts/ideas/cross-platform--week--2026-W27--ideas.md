---
kind: ideas
granularity: week
period_start: '2026-06-29T00:00:00'
period_end: '2026-07-06T00:00:00'
run_id: 5d689db2-594e-402e-bfce-c00c92627a2a
status: succeeded
topics:
- AI coding agents
- Antigravity
- Flutter
- ADK
- agent skills
- cross-platform development
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/antigravity
- topic/flutter
- topic/adk
- topic/agent-skills
- topic/cross-platform-development
language_code: en
pass_output_id: 272
pass_kind: trend_ideas
upstream_pass_output_id: 271
upstream_pass_kind: trend_synthesis
---

# Agent-generated Flutter code inspection

## Summary
Antigravity work in this pack points to reusable skills for ADK frontends and inspection aids for Flutter game logic. The common adoption blocker is trust in generated code when platform behavior, streaming events, or timing-sensitive physics fail outside the prompt.

## A reusable Antigravity skill for Flutter frontends on ADK agents
Teams building demos or internal tools on Google Agent Development Kit can turn each frontend failure into an Antigravity skill update. The useful pattern is concrete: require the agent to produce interface notes, usage notes, architecture notes, and design notes before code generation; review those artifacts; update `SKILL.md` and reference files; delete the generated frontend; then rerun the workflow.

This fits teams that have Python ADK agents but lack a client team ready to wire up Flutter. The case here reached a shareable `flutter_frontend_for_adk` skill after 13 iterations. The fixes were ordinary frontend integration issues that tend to repeat across projects: macOS and iOS network permissions, markdown rendering, linting, sealed message types, chat scrolling, web crashes from `dart:io`, partial ADK event aggregation, and tool invocation display.

A cheap test is to run the skill against two different ADK sample agents and check whether the second run needs fewer manual fixes. The acceptance bar should include a web build, one mobile target, a streaming response path, and a tool-call display path, because those are where the reported failures clustered.

### Sources
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): Summarizes the repeatable Antigravity workflow, staged deliverables, two-agent review loop, 13 iterations, and recurring ADK frontend fixes.
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): Names the `flutter_frontend_for_adk` skill and the planning documents produced before code generation.
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): Lists the later concrete fixes, including platform network permissions, markdown, lints, web networking, scrolling, and partial ADK events.

## Review pauses and reruns for agent-generated frontend code
Agent-generated frontend work needs an explicit stop point before code generation. The Antigravity ADK case added mandatory review steps after the early phases so the human developer could inspect notes and plans before the agent moved on. That small workflow change matters because the developer was using the process to learn the backend interface, not only to get files written.

The buildable version is a repository template for Antigravity skills that enforces review gates after discovery, usage, architecture, and design phases. Each gate should leave a named file in the repo and require approval before generation continues. The rerun step should reset generated files so the skill, not the local accident of one session, carries the improvement.

This is useful for developer enablement teams that maintain internal agent templates. It gives them a way to capture platform rules and project conventions as the work proceeds, including small but expensive misses such as ignored `frontend/lib` files or missing macOS and iOS entitlements.

### Sources
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): Describes installing existing Google Cloud and Flutter skills, then establishing an iterative loop with coder and author agents.
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): Shows the concrete update to add review pauses and fix gitignore behavior, followed by clearing files and rerunning.
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): Describes the skill as a record of what the developer learned and reports 13 iterations to reach a shareable version.

## Debug overlays and replay checkpoints for agent-built Flutter games
Flutter and Flame game teams using coding agents should ask for inspection tools while the game logic is being generated. In DashLander, reading the generated math was not enough to trust physics and collision behavior. A keyboard-gated debug mode displayed terrain data, surface tilt, and hitboxes so the developer could point the agent at the wrong calculation.

Replay logic needed a second support layer. Challenge Mode used ghosts of past high scores, which avoided real-time multiplayer infrastructure. Testing exposed millisecond-level drift: a replayed lander could look correct for most of a run and crash near the end. The fix was to store full lander state at thruster events and compare the live replay against those checkpoints.

A practical adoption test is to require every agent-built game prototype to ship with debug overlays for collision and physics state plus deterministic replay checks before adding more content. That gives the human reviewer evidence when the generated code behaves incorrectly, especially in places where visual output looks plausible until late in the run.

### Sources
- [Vibe once, run anywhere with Antigravity and Flutter](../Inbox/2026-06-29--vibe-once-run-anywhere-with-antigravity-and-flutter.md): Reports the initial Flutter and Flame game, the later prompt volume, and the need to refactor and add tests for understandable code.
- [Vibe once, run anywhere with Antigravity and Flutter](../Inbox/2026-06-29--vibe-once-run-anywhere-with-antigravity-and-flutter.md): Describes the debug mode with overlays for terrain data, relative tilt, and collision hitboxes, and introduces the replay desync bug.
- [Vibe once, run anywhere with Antigravity and Flutter](../Inbox/2026-06-29--vibe-once-run-anywhere-with-antigravity-and-flutter.md): Explains the millisecond scheduling drift and the fix using full physical state checkpoints at thruster events.
