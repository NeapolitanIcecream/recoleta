---
source: arxiv
url: https://arxiv.org/abs/2607.13156v1
published_at: '2026-07-14T18:06:29'
authors:
- Luciane Silva
- Thayssa Rocha
- Nicole Davila
- Gustavo Pinto
topics:
- code-intelligence
- automated-software-production
- design-systems
- front-end-development
- human-ai-interaction
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Design-System-Aware Development with AI: Evaluating Productivity and Design Consistency

## Summary
A controlled industrial experiment found that AI assistance grounded in an enterprise Design System accelerated front-end and mobile interface development and improved implementation completeness. The evidence comes from 49 developers completing two mockup-based screens across Angular, iOS, and Android, with results limited by the single-company setting and narrowly defined task.

## Problem
- Generic AI coding tools lack internal Design System context, so their output may be syntactically valid but visually inconsistent or non-compliant with enterprise standards.
- Organizations need evidence on whether combining AI with a Design System improves delivery time, design fidelity, and workflow consistency in practical front-end development.

## Approach
- Researchers ran a controlled, remote experiment at Zup Innovation with 49 professional developers across two cycles in June and October 2025.
- Participants used one of three workflows: manual development, Design System-only development, or StackSpot AI contextualized with the enterprise Design System.
- Each participant implemented two high-fidelity mockup screens in Angular, iOS, or Android, with specialist review and timed incremental submissions.
- The study measured time-to-delivery, task completeness, performance variability, and break patterns as an indirect indicator of workflow friction.

## Results
- AI-assisted completion times were 69.4% lower than the manual baseline in Angular, falling from 536.15 to 164.00 minutes; 46.7% lower in iOS, from 593.00 to 316.00 minutes; and 57.9% lower in Android, from 387.75 to 163.25 minutes. The reported differences were statistically significant at p<0.05.
- AI assistance was also faster than Design System-only development by 24.4% in Angular, 15.5% in iOS, and 23.4% in Android.
- Average task completeness reached 96% with AI assistance, compared with 85% for Design System-only development and 68% for manual development.
- Completion-time variability decreased in the AI group: standard deviations were 42 minutes in Angular, 51 in iOS, and 35 in Android, versus 85, 112, and 75 minutes for the Design System group.
- Breaks were shorter and more homogeneous with AI assistance, ranging from 0 to 90 minutes, while the manual group recorded a break of up to 195 minutes in one dataset; this supports reduced workflow friction but is only an indirect measure of cognitive load.
- Generalizability remains uncertain because all participants came from one Brazilian enterprise, the task covered only two predefined screens, and completeness was judged by specialists rather than an automated or multi-reviewer assessment.

## Link
- [https://arxiv.org/abs/2607.13156v1](https://arxiv.org/abs/2607.13156v1)
