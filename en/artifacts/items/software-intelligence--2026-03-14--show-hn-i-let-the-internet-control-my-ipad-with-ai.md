---
source: hn
url: https://play.thomaskidane.com/
published_at: '2026-03-14T23:01:53'
authors:
- meneliksecond
topics:
- gui-agent
- mobile-automation
- human-ai-interaction
- real-device-control
- natural-language-interface
relevance_score: 0.84
run_id: materialize-outputs
language_code: en
---

# Show HN: I let the internet control my iPad with AI

## Summary
This is an AI agent demo system that lets internet users remotely control a real iPad with natural language, highlighting real-time execution of language-to-GUI actions. It is more like an interactive product prototype than a formal paper, but it clearly demonstrates agent-based UI automation for consumer devices.

## Problem
- The goal is to solve the problem of how ordinary people can use natural language to have AI directly operate a real mobile device, without writing scripts or clicking manually.
- This matters because it is a key step toward general device agents, GUI automation, and more natural human-computer interaction.
- Real mobile environments are complex and involve engineering challenges such as shared queueing, real-time execution, interface navigation, and safety constraints.

## Approach
- Users first join a queue to get a turn, then directly enter natural-language commands, such as "Open Safari".
- The AI agent breaks the command down into a series of interface actions and executes them autonomously on a real iPad, such as moving the cursor, tapping icons, switching apps, and scrolling.
- The system makes the execution process public via live stream, allowing users to watch in real time how the agent completes the goal or ends the turn after a timeout.
- Current capabilities focus on basic GUI operations: opening/closing/switching apps, tapping UI elements, scrolling, returning to the home screen, and carrying out simple multi-step tasks.
- The system explicitly restricts high-risk or highly complex capabilities, such as text input, complex gestures, notification/lock-screen interaction, and apps that require login.

## Results
- What is provided is a publicly playable online demo of a real iPad, rather than a research paper with standard benchmark evaluation; the passage **does not provide formal quantitative metrics**, such as success rate, latency, task completion rate, or baseline comparisons.
- Task types it claims to support include opening/closing/switching apps, tapping buttons and icons, scrolling up and down within apps, and returning to the home screen from anywhere.
- It also claims to support simple multi-step instructions, such as "Open Goodnotes then close it," indicating that the agent has basic task decomposition and sequential execution ability.
- In terms of operating mechanism, it supports shared multi-user access: users queue up, take turns executing commands, and automatically hand off to the next person on timeout, showing that the system has handled the most basic concurrent-use workflow.
- Capabilities it clearly does not support include text input, home-screen page swiping, two-finger/multi-finger gestures, notifications and Control Center, the lock screen, and login scenarios, indicating that the current result is closer to a runnable prototype in a constrained environment than a breakthrough in general mobile agents.

## Link
- [https://play.thomaskidane.com/](https://play.thomaskidane.com/)
