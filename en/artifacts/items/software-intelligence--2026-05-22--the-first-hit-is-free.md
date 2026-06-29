---
source: hn
url: https://whattotelltherobot.com/p/the-first-hit-is-free
published_at: '2026-05-22T22:28:04'
authors:
- stefie10
topics:
- human-ai-interaction
- ai-assisted-coding
- ai-policy
- robotics-software
- research-automation
relevance_score: 0.64
run_id: materialize-outputs
language_code: en
---

# The First Hit Is Free

## Summary
The article argues for open AI use with human ownership: let AI write, code, and draft, then make a skilled person accountable for the output. Its main value is a practical policy stance for AI-assisted research, teaching, and robotics work.

## Problem
- AI can produce papers, slides, code, and presentations, which raises a concrete question: who is responsible for the quality, accuracy, and licensing of the artifact?
- The author says AI help matters because it can speed up research communication and software work, but weak domain knowledge can lead users to accept bad fixes or poor research ideas.
- Course policies need to preserve the expertise students need for hard problems while allowing real AI use.

## Approach
- The core method is human-led AI use: ask tools such as Claude Code to draft, translate, implement, and fix artifacts, then review and redirect the tool.
- The author tests this pattern on real tasks, including LaTeX math writing, Python implementation, a Kalman filter change, ROS1-to-ROS2 migration, slide generation, and video presentation generation.
- The control mechanism is domain judgment. In the AIBO project, Claude suggested source-file fixes, while the author identified package.xml as the likely build issue and steered the tool.
- The proposed policy matches the Linux kernel stance in spirit: AI-generated contributions are allowed, but named humans must review them, check licensing, and take responsibility.

## Results
- No benchmark, dataset, or controlled evaluation is reported.
- Claude Code completed math write-up support, LaTeX generation, Python algorithm implementation, and error fixes for a task the author had tried to get done for more than 10 years.
- The author requested a switch from an Extended Kalman Filter to an Unscented Kalman Filter, and the tool made the change.
- Claude helped convert an old ROS1 program to ROS2 for an AIBO outreach project; the author says the fix was faster than working alone, but gives no time measurement.
- In a Brown course during one semester, students were allowed to use AI for any course work, including presentations; several used it for slides, code, and video presentations.
- When pointed at recent lab papers and asked for new research ideas, the tool produced poor ideas, which the author uses as evidence that expert review remains necessary.

## Link
- [https://whattotelltherobot.com/p/the-first-hit-is-free](https://whattotelltherobot.com/p/the-first-hit-is-free)
