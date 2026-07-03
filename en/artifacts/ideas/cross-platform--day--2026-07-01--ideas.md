---
kind: ideas
granularity: day
period_start: '2026-07-01T00:00:00'
period_end: '2026-07-02T00:00:00'
run_id: 023f448a-f8cd-48d3-a811-f15fd71263e9
status: succeeded
topics:
- AI coding agents
- Flutter
- Agent Development Kit
- developer skills
- frontend generation
tags:
- recoleta/ideas
- topic/ai-coding-agents
- topic/flutter
- topic/agent-development-kit
- topic/developer-skills
- topic/frontend-generation
language_code: en
pass_output_id: 262
pass_kind: trend_ideas
upstream_pass_output_id: 261
upstream_pass_kind: trend_synthesis
---

# Reviewable Flutter Generation Workflows

## Summary
The case points to a practical pattern for teams building Flutter clients for ADK agents: make the coding agent create reviewable interface, usage, architecture, and design files before code, then fold each failed run into a reusable skill. The clearest build target is a small ADK Flutter client workflow with post-generation checks for platform permissions, markdown, streaming events, web networking, and tool-call display.

## Staged planning files before Flutter code generation for ADK clients
Teams building Flutter clients for ADK agents can require the coding agent to produce four reviewable files before it writes UI code: `AGENT_INTERFACE_NOTES.md`, `FRONTEND_USAGE_NOTES.md`, `FRONTEND_ARCHITECTURE_NOTES.md`, and `FRONTEND_DESIGN_NOTES.md`. This gives the developer a concrete place to check the backend interface, expected user behavior, state model, and visual plan while the cost of revision is still low.

The useful adoption change is a gate in the coding-agent workflow. The agent reads the ADK codebase, drafts the notes, pauses for review, and only then generates the Flutter app. A cheap test is to run the workflow on two existing ADK agents with no frontend and check whether the notes correctly identify streaming behavior, APIs, tool calls, and required client state before code is generated.

### Evidence
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): The post names the four planning files and describes their role before code generation.
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): The author used a second Antigravity conversation to inspect notes, specifications, and code structure before updating the workflow.

## Post-generation checks for ADK Flutter client failure modes
A reusable Flutter frontend skill for ADK agents should include a post-generation checklist tied to failures that appear when the app runs on real targets. The checklist can cover macOS and iOS network permissions, markdown rendering with `flutter_markdown`, lint and formatting rules, sealed message types, chat auto-scroll, `package:http` networking for web builds, partial streaming event aggregation, and tool invocation display.

This is a concrete support layer for generated clients. The coding agent can run formatting and lint checks, scan for `dart:io` in web-bound networking code, verify entitlements, and include a small streaming-event test that assembles partial ADK events before adding completed messages to the session list. These checks target errors that a single code-generation pass can miss.

### Evidence
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): The iteration log lists concrete failures and fixes across permissions, markdown, linting, message types, scrolling, web networking, partial events, and tool invocation display.
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): The summary confirms that partial ADK streaming events were handled by accumulating `event.partial` chunks and adding completed events to the session list.

## Reviewer loop that converts human Flutter fixes into skill updates
Developers using coding agents on unfamiliar ADK backends can keep a separate review loop for the reusable skill. One agent runs the current workflow and generates artifacts. A second conversation reviews the artifacts with the developer, records gaps, and updates the skill. After the update, the generated frontend is deleted and the workflow is run again.

This works best when the developer reads the generated notes and source files, runs the app, and directly fixes repeated failures. The next prompt asks Antigravity how to fold those fixes into the skill, so the next generated client starts with the newly learned rules. The workflow is useful for teams that need generated code they can explain and maintain after the agent session ends.

### Evidence
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): The author describes installing existing skills, starting a repeated workflow, evaluating output, updating guidance, deleting generated artifacts, and rerunning.
- [Learning faster with Antigravity](../Inbox/2026-07-01--learning-faster-with-antigravity.md): The post says the author researched recurring failures, modified notes and code, then asked Antigravity how to update the skill so future generations matched the fixes.
