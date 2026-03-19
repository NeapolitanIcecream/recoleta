---
source: hn
url: https://crackr.dev/
published_at: '2026-03-09T23:32:17'
authors:
- wa5ina
topics:
- voice-ai
- technical-interview
- coding-practice
- ai-feedback
- developer-tools
relevance_score: 0.82
run_id: materialize-outputs
language_code: en
---

# Show HN: I built an AI-powered technical interview prep tool

## Summary
This is a voice AI tool for technical interview practice that simulates a senior engineer conducting real-time questioning, follow-ups, hints, and scoring. It combines voice conversation, a real coding environment, and post-session review, with the goal of improving a candidate's interview performance rather than just problem-solving practice.

## Problem
- Technical interview preparation usually focuses only on practicing problems themselves, lacking **verbal communication, pressure handling, follow-up interaction, and feedback in real interviews**.
- Traditional practice tools are often form-based or static question banks, and cannot **listen, ask, challenge, give hints, and score in real time** like a real interviewer.
- This matters because whether a candidate gets an offer depends not only on writing the correct answer, but also on **how they explain their thinking, handle dead ends, and communicate and code under pressure**.

## Approach
- The core approach is a **real-time voice AI interviewer**: it speaks, listens to your answers, and continues asking follow-up questions or pointing out issues based on your performance, aiming to reproduce the interaction style of a senior engineer interviewer.
- It uses **Claude** for reasoning, follow-ups, and feedback generation; **WebRTC** for low-latency bidirectional voice; and **Monaco Editor** to provide a realistic coding experience close to VS Code.
- The practice flow is: choose a target company/topic/programming language → enter the voice interview → write code and run tests in the editor → receive a **five-dimension scorecard** and specific feedback on lost points after the session.
- Put simply, it does not just give you a problem and wait for submission; it acts like a real person, listening as you explain, watching as you code, applying pressure or giving hints when needed, and finally producing a structured review.

## Results
- The text **does not provide formal experiments, benchmark data, or offline evaluation results**, so there is no verifiable quantitative comparison for accuracy, improvement magnitude, or performance versus competitors or human interviewers.
- The explicit system performance claim is: **WebRTC delivers sub-100ms bidirectional real-time voice**.
- Product capability claims include: **1 free interview**; paid usage is credit-based, with **1 credit = 15-minute session**; example pricing is **10 credits at $1.00 each, 25 credits at $0.88 each, and 50 credits at $0.78 each**.
- The strongest functional claim is that the AI can **ask follow-up questions in real time, point out dead ends, give hints when you are stuck, and produce five-dimensional scoring and written feedback after the session**, like a real senior engineer.
- It also claims that practice supports **adaptation to target company, topic, and language**, and takes place in a **Monaco/VS Code-style environment** rather than a toy interface.

## Link
- [https://crackr.dev/](https://crackr.dev/)
