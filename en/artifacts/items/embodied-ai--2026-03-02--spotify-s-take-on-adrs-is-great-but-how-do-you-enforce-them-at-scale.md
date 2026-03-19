---
source: hn
url: https://news.ycombinator.com/item?id=47226046
published_at: '2026-03-02T23:59:47'
authors:
- iamalizaidi
topics:
- software-architecture
- adr-enforcement
- github-action
- code-review
- developer-tooling
relevance_score: 0.01
run_id: materialize-outputs
language_code: en
---

# Spotify's take on ADRs is great, but how do you enforce them at scale?

## Summary
This is an open-source tooling practice for engineering teams: by automatically posting relevant ADRs when a PR touches protected files, it truly embeds architectural decisions that were "written but never read" into the code review workflow. The core value is not creating more documentation, but proactively surfacing existing decisions at the most appropriate moment, thereby improving enforcement of architectural constraints.

## Problem
- Even if teams write ADRs following Spotify's recommendations, the files usually still sit in `docs/adr/`, and developers do not proactively read them before opening a PR.
- The real gap is not a "lack of documentation," but a "lack of timely decision prompts when related code is being changed," which makes architectural constraints hard to uphold in day-to-day development.
- Existing alternatives such as CODEOWNERS are more focused on assigning reviewers, while Danger.js often requires writing code-based rules; neither directly uses concise Markdown ADRs to explain during review "why this review matters."

## Approach
- Write ADR/decision files in plain Markdown, declaring metadata such as protected file scope, status, and severity level, while remaining compatible with existing ADR formats.
- Scan PR changes in a GitHub Action or CLI; once a file matches the rules, automatically post the relevant decisions as a PR comment.
- Rule matching supports glob patterns, regex, content-based rules, and boolean logic, so it can be triggered not only by path but also by more complex conditions.
- Use severity levels (Critical / Warning / Info) to tier decisions; critical violation scenarios can block PRs, upgrading the system from "reminder" to "enforced constraint."
- The design emphasizes engineering usability: the CLI can integrate with any CI; idempotent comment updates avoid spam; and no external network calls are made, protecting the privacy of code and metadata.

## Results
- The post **does not provide formal benchmark experiments, public dataset evaluations, or comparative numerical metrics**, so there are no paper-style SOTA results.
- The strongest concrete engineering claim is that it can handle PRs with **3000+ files** **without OOM**, indicating usability in large-scale code review scenarios.
- The tool claims to include **109 tests**, as well as **ReDoS protection** and **path traversal protection**, emphasizing the robustness and security of the rule engine and file handling.
- Verifiable feature-level claims include support for **3 severity levels** (Critical / Warning / Info), with Critical able to **block PRs**.
- Compatibility claims include that it can be used either as a **single-step GitHub Action** or integrated via the **`npx decision-guardian` CLI** into environments such as GitLab, Jenkins, CircleCI, and pre-commit hooks.
- Its positioning relative to baselines is: compared with **CODEOWNERS**, it adds "why this review matters"; compared with **Danger.js**, it uses **Markdown rather than code** to maintain rules, allowing non-JavaScript engineers to maintain architectural decisions as well.

## Link
- [https://news.ycombinator.com/item?id=47226046](https://news.ycombinator.com/item?id=47226046)
