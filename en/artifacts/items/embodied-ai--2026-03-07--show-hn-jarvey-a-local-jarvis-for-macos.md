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
relevance_score: 0.16
run_id: materialize-outputs
language_code: en
---

# Show HN: Jarvey - a local JARVIS for MacOS

## Summary
Jarvey is a locally running, voice-first macOS desktop agent that lets users control their computer with speech to perform cross-application GUI operations. It combines native macOS control, streaming voice interaction, task planning, and local memory, but is essentially an engineering system showcase rather than an academic paper.

## Problem
- The problem it solves is enabling users to directly operate the macOS desktop with natural speech, without manually clicking, typing, and switching between applications.
- This matters because many desktop workflows are cross-application, multi-step, and GUI-based, while traditional voice assistants usually lack reliable desktop execution capabilities.
- At the same time, computer-use agents are high-risk, involving clicking, typing, file modification, and account actions, so localized deployment, permission controls, and approval mechanisms are needed.

## Approach
- The core mechanism is simple: the user presses a global hotkey and speaks a command; Jarvey listens, sends the request to a voice model and a planning model, then calls local mouse, keyboard, and screenshot tools to execute desktop actions.
- The system consists of a native Swift overlay app, a local Node sidecar, a hidden WKWebView voice runtime, and a local input bridge, all running on the user's machine.
- The voice component uses OpenAI Realtime for low-latency audio streaming; the task planning component uses a GPT-5.4 supervisor to coordinate GUI and workbench specialists in executing multi-step tasks.
- It provides local SQLite persistent memory, an approval center, permission onboarding, and local services bound only to 127.0.0.1 to reduce exposure.

## Results
- The text does not provide standard academic experiments, benchmark datasets, or quantitative metrics, so there are no accuracy, success rate, latency comparison, or baseline comparison numbers to report.
- Specific claimed capabilities include opening applications, filling forms, navigating UIs, managing files, mouse clicking, dragging, scrolling, keyboard input, and screenshots.
- Clear implementation details at the architecture level include **2 local HTTP services** (`127.0.0.1:4818` sidecar and `127.0.0.1:4819` input bridge), as well as the local state directory `~/Library/Application Support/Jarvey/`.
- The build and runtime requirements specify engineering constraints such as **Node.js 20 or 22** and **Swift 6**; the release artifact is a self-contained macOS zip/app with the sidecar, voice runtime, and vendored Node runtime built in.
- The strongest practical claim is not a performance breakthrough, but productized integration: voice-first interaction, local desktop control, persistent memory, approval, and permission management are packaged into a directly runnable macOS agent.

## Link
- [https://github.com/novynlabs-repo/Jarvey](https://github.com/novynlabs-repo/Jarvey)
