---
source: hn
url: https://www.portify.ca/
published_at: '2026-03-12T23:06:55'
authors:
- lucasadilla
topics:
- developer-portfolio
- github-mining
- career-narrative
- repo-summarization
- automation
relevance_score: 0.77
run_id: materialize-outputs
language_code: en
---

# Portify: Generate a developer portfolio from your GitHub

## Summary
Portify is a website tool that automatically organizes a developer’s GitHub activity into a shareable portfolio. It turns repositories, commits, tech stacks, and timelines into a personal narrative page better suited for job applications and showcasing work.

## Problem
- A raw GitHub profile is not user-friendly enough for recruiters or collaborators; the information is scattered, making it hard to quickly understand what a developer has built and how they have grown.
- Developers need to manually organize commit history, repository descriptions, tech stacks, and project evolution into a portfolio, which is costly and difficult to keep continuously updated.
- This matters because job seeking, networking, and collaboration scenarios require a clear, credible, continuously synced entry point for presenting technical work.

## Approach
- After signing in with GitHub, users select several repositories that best represent them, and the system reads commits, languages, and repository metadata.
- Portify automatically generates readable repository summaries, identifies tech stacks, builds contribution/language/evolution charts, and stitches them into a single-page personal narrative.
- It generates a fixed, shareable personal URL and keeps it synced with GitHub activity.
- Users can also manually edit content and add screenshots and Mermaid diagrams, making the page feel more like a product showcase than a résumé list.

## Results
- The text does not provide formal paper-style experiments, benchmarks, or quantitative metrics, so there are **no reportable quantitative results**.
- Explicitly stated outputs include generating **1 shareable portfolio URL** from GitHub history (for example, `/yourname`).
- The system claims it can automatically generate multiple kinds of content: project summaries, tech stack badges, contribution-over-time charts, language distribution, and a public timeline.
- The stated workflow has **3 steps**: select repositories, automatically generate the narrative, then share and keep it continuously synced.
- Its strongest concrete claim is that it transforms “raw GitHub activity” into a “single-page portfolio suitable for job-sharing,” while supporting continuous updates rather than being a one-off static résumé.

## Link
- [https://www.portify.ca/](https://www.portify.ca/)
