---
source: arxiv
url: https://arxiv.org/abs/2605.22534v1
published_at: '2026-05-21T14:24:20'
authors:
- Sien Reeve O. Peralta
- Fumika Hoshi
- Hironori Washizaki
- Naoyasu Ubayashi
- Inase Kondo
- Yoshiki Higo
- Hiroki Mukai
- Norihiro Yoshida
- Kazuki Kusama
- Hidetake Tanaka
- Youmei Fan
topics:
- agentic-pull-requests
- code-review
- ai-coding-agents
- human-ai-collaboration
- software-engineering-metrics
relevance_score: 0.86
run_id: materialize-outputs
language_code: en
---

# Why Are Agentic Pull Requests Merged or Rejected? An Empirical Study

## Summary
This paper finds that merge and rejection labels mismeasure AI coding agents because PR decisions often depend on review comments, CI results, commits, and repository process. It studies 11,048 closed agentic pull requests and manually codes 717 cases to separate agent failures from process effects and human help.

## Problem
- Agentic PRs are often judged by merge or rejection status, which can mix faulty code with duplicate work, superseded changes, silent closures, or project rules.
- This matters because merge-rate evaluation can overstate agent errors on rejected PRs and overstate autonomy on merged PRs.
- Better evaluation needs the review record: comments, CI status, commit history, closure context, and reviewer edits.

## Approach
- The study starts from the AIDev dataset, keeps closed Agentic-PRs in repositories with at least 500 stars, and obtains 11,048 PRs.
- After removing bot-only reviews, the refined dataset has 9,799 human-reviewed PRs: 6,179 merged and 3,620 rejected.
- The authors manually inspect a stratified sample of 717 PRs: 353 rejected and 364 merged, balanced across agents and repositories.
- Rejected PRs are coded as agentic failure, non-agentic failure, or unknown. Merged PRs are coded as feedback loop, human intervention, no feedback loop, or unknown.
- Two annotators code each PR. Reported agreement is Cohen’s κ≈0.90 for rejection reasons and κ=1.0 for merged-PR interaction patterns.

## Results
- In 353 rejected PRs, only 126 were clear agentic failures, equal to 35.7%. Non-agentic causes accounted for 110 PRs, or 31.2%, and unknown rationale accounted for 117 PRs, or 33.1%.
- Devin rejected PRs had 37/153 agentic failures, or 24.2%, while OpenAI Codex had 54/113, or 47.8%. The paper reports this as evidence that rejection labels cannot be compared across agents without review context.
- In 364 merged PRs, 288 PRs, or 79.1%, had no observed feedback loop or reviewer-applied commit.
- Human involvement appeared in 56/364 merged PRs, or 15.4%: 28 feedback loops, or 7.7%, and 28 reviewer-applied commits, or 7.7%.
- Copilot and Devin accounted for 54 of the 56 merged PRs with feedback loops or human intervention. Copilot had 29/49 such merged PRs, or 59.2%; Devin had 25/107, or 23.4%.
- OpenAI Codex had 1/167 merged PRs with human intervention, or 0.6%, and 0 feedback-loop cases in the inspected sample; Cursor had 1/33 feedback-loop case, or 3.0%.

## Link
- [https://arxiv.org/abs/2605.22534v1](https://arxiv.org/abs/2605.22534v1)
