---
source: hn
url: https://play.thomaskidane.com/
published_at: '2026-03-14T23:01:53'
authors:
- meneliksecond
topics:
- gui-agent
- mobile-ui-control
- real-world-demo
- natural-language-agent
relevance_score: 0.3
run_id: materialize-outputs
language_code: en
---

# Show HN: I let the internet control my iPad with AI

## Summary
This is an AI agent demo system that lets the public remotely control a real iPad through natural language, showcasing AI's real-time planning and execution capabilities on a mobile graphical interface. It is more of a product/demo than an academic paper, but it demonstrates the feasibility of GUI agents for real devices.

## Problem
- The target problem is: how to enable AI to understand natural-language instructions and autonomously complete graphical interface operations on a **real iPad**.
- This matters because controlling real mobile devices is closer to actual human-computer interaction than working in purely text-based or simulated environments, and it better tests an agent's closed-loop capabilities in perception, planning, and execution.
- The challenges include multi-step UI navigation, real-time execution, shared queued usage, and ensuring basic usability and safety under real hardware constraints.

## Approach
- The system provides a queue-based web entry point where users enter English natural-language commands, and when their turn arrives, an AI agent executes them on a real iPad.
- The core mechanism can be understood simply as: the AI first breaks a one-sentence goal into a series of UI action steps, then moves the cursor on the screen, taps icons/buttons, and scrolls pages until the goal is completed or time runs out.
- The current capabilities focus on basic touch-based GUI operations: opening/closing/switching apps, tapping UI elements, scrolling up and down, returning to the home screen, and completing simple multi-step instructions.
- To control risk and complexity, the system explicitly restricts high-difficulty or sensitive interactions such as text input, complex gestures, notifications/Control Center/lock screen, and apps requiring login.

## Results
- It provides a **real-time control** demo of a real iPad: users can issue commands such as "Open Safari" or "Open Goodnotes then close it" and watch the agent execute them.
- The declared supported capabilities include **5 categories**: opening/closing/switching apps, tapping buttons/icons/UI elements, in-app scrolling, returning to the home screen from anywhere, and executing multi-step instructions.
- The explicitly listed current limitations also include **5 categories**: **no support** for text input, swiping across home-screen pages, gestures such as two-finger actions/pinch-to-zoom, interactions with notifications/Control Center/lock screen, and apps requiring login/authentication.
- The text **does not provide quantitative experimental results**: there is no success rate, task completion time, benchmark dataset, comparison method, or ablation study, so it is not possible to verify relative SOTA performance or a research breakthrough.
- The strongest concrete claim is: the system allows "people from around the world" to take turns sending natural-language commands to a real iPad, with an AI agent executing them autonomously, forming a publicly visible real-time demo loop.

## Link
- [https://play.thomaskidane.com/](https://play.thomaskidane.com/)
