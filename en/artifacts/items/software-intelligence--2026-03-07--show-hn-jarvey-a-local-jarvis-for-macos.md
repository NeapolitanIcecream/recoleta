---
source: hn
url: https://github.com/novynlabs-repo/Jarvey
published_at: '2026-03-07T23:04:06'
authors:
- AhmedAshraf
topics:
- desktop-agent
- computer-use-agent
- voice-interface
- macos-automation
- gui-agent
relevance_score: 0.9
run_id: materialize-outputs
language_code: en
---

# Show HN: Jarvey - a local JARVIS for MacOS

## Summary
Jarvey is a local voice-first desktop agent for macOS that can be invoked via a hotkey and then controlled with natural language to perform cross-application tasks on your computer. It combines native desktop control, real-time voice interaction, task planning, and local memory into a computer-use agent that can actually operate a GUI.

## Problem
- The problem it aims to solve is that when users perform multi-step desktop operations on macOS—such as opening apps, filling out forms, navigating interfaces, and managing files—the process is cumbersome, repetitive, and costly in terms of cross-application switching.
- This matters because a truly useful desktop agent must not only “chat,” but also take direct action on graphical interfaces, turning natural-language instructions into real software operations.
- At the same time, computer-control agents are high-risk: they may click, type, approve dialogs, or delete data, so permissions, local deployment, and security boundaries become critical concerns as well.

## Approach
- The core mechanism is simple: the user presses a global hotkey and speaks a task, Jarvey listens to the voice input, sends the request to a model for planning, and then executes mouse, keyboard, screenshot, and other actions through a local control bridge to complete the desktop task.
- The system consists of a native Swift overlay app, a local Node sidecar, a hidden WKWebView voice runtime, the OpenAI Realtime voice channel, and a GPT-5.4 planning/tool-use module.
- In terms of agent architecture, it uses “GPT-5.4 supervisor + specialists” to break down multi-step tasks and coordinate GUI operations with workbench-style task execution.
- For usability and persistent context, the system provides local SQLite persistent memory, an approval center, settings persistence, and guided permissions for microphone, screen recording, and accessibility.
- To constrain risk, it states that all local services bind only to 127.0.0.1, with no built-in analytics or third-party telemetry, but it does send user requests, context, screenshots, and audio to OpenAI to complete model interactions.

## Results
- The text does not provide standard academic experiments, benchmark data, or quantitative performance results, so there are no reportable accuracy, success-rate, latency, or SOTA figures.
- It explicitly claims the following executable task types: opening apps, filling out forms, browsing UIs, managing files, and more general multi-step desktop automation.
- The system gives fairly specific engineering capabilities: global hotkey `Option+Space` trigger, low-latency audio streaming based on OpenAI Realtime, and two local HTTP services running separately on `127.0.0.1:4818` and `127.0.0.1:4819`.
- In terms of release format, it provides a self-contained macOS archive that includes the sidecar, voice runtime, and built-in Node runtime, meaning end users can run it without checking out the source code.
- Its security and deployment statements are among its stronger concrete claims: it is limited to the local loopback address, not exposed to the network, and has no analytics telemetry, but it also emphasizes that a CUA carries the risk of deleting data and acting on user accounts on the user’s behalf.

## Link
- [https://github.com/novynlabs-repo/Jarvey](https://github.com/novynlabs-repo/Jarvey)
