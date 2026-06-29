---
source: arxiv
url: http://arxiv.org/abs/2604.17460v1
published_at: '2026-04-19T14:20:09'
authors:
- Zain Naboulsi
topics:
- agentic-coding
- developer-education
- claude-code
- adaptive-learning
- multi-agent-workflows
relevance_score: 0.92
run_id: materialize-outputs
language_code: en
---

# Agentic Education: Using Claude Code to Teach Claude Code

## Summary
This paper presents **cc-self-train**, a 50-module curriculum that uses Claude Code itself to teach developers how to use Claude Code. The main claim is that agentic coding tools need structured, auto-updating instruction, and the pilot study reports large self-efficacy gains across all measured skill areas.

## Problem
- Developers can access powerful agentic coding tools, but current learning materials are fragmented, feature-by-feature, and often stale within days because the tools change quickly.
- Existing docs, blog posts, and courses do not provide a progressive path from beginner use to advanced features such as hooks, skills, subagents, and multi-agent workflows.
- This matters because advanced agentic features require compositional understanding; without a structured path, adoption and effective use stay limited.

## Approach
- The system is a hands-on curriculum called **cc-self-train** with **50 modules** organized as **10 sequential modules across 5 project paths**: Canvas, Forge, Nexus, Sentinel, and BYOP.
- It teaches Claude Code by having learners build real software projects while interacting with Claude Code as the instructor inside the same environment.
- Instruction changes across **4 personas** aligned to Gradual Release of Responsibility: **Guide → Collaborator → Peer → Launcher**. Early modules explain more; later modules step back and expect more learner control.
- An adaptive layer watches learner engagement through hook-based heuristics, uses streak detection for mid-module intervention, and changes persona schedules at module boundaries.
- The system also includes step pacing, cross-session state tracking, a parameterized test suite for structural consistency across all modules, and an onboarding agent that checks for upstream Claude Code changes and updates teaching materials before instruction starts.

## Results
- The paper reports a **pilot evaluation with 27 participants**.
- It claims **statistically significant reported self-efficacy gains across all 10 assessed skill areas**, with **p < 0.001**.
- The largest reported gains were on more advanced Claude Code features, including **hooks** and **custom skills**.
- The curriculum contains **50 module files**, **5 project domains**, **10 progressive modules per path**, **22 context documents**, and **8 test files** used for consistency checks.
- The excerpt does **not provide task-performance metrics, completion rates, time savings, or comparisons against a baseline curriculum or alternative tool-training method**.

## Link
- [http://arxiv.org/abs/2604.17460v1](http://arxiv.org/abs/2604.17460v1)
