---
source: hn
url: https://docs.damsecure.ai/blog/pr-review-security-benchmark/
published_at: '2026-07-12T22:57:23'
authors:
- pcollins123
topics:
- code-intelligence
- security-review
- software-foundation-models
- automated-software-production
- human-ai-interaction
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Grok 4.5 and GPT5.6 beat Anthropic for finding security vulnerabilities in PRs

## Summary
Dam Secure benchmarks 10 AI models on pull-request security review using 10 synthetic PRs with planted access-control bugs. GPT-5.6 Sol leads the reported cost-quality frontier, while Grok 4.5 and Gemini 3.1 Flash Lite offer lower-cost alternatives.

## Problem
- Security teams need models that can detect vulnerabilities introduced by changed code in pull requests.
- Model choice affects recall, false-positive rates, review cost, and token usage.
- Results from full-code scanning do not directly measure pull-request review performance.

## Approach
- The benchmark evaluated 10 models on 10 PRs, each containing one planted access-control flaw such as IDOR, missing authentication, or broken authorization.
- Each model ran five times with the same Dam Secure scanner and toolset. Agents could read full files and search changed files with grep.
- The dataset combined private synthetic repositories with reverse-replayed real CVEs embedded in realistic commit histories.
- Findings were scored against hidden ground truth using recall, precision, F1, cost per PR, and cost per true positive.
- The authors also tested Pydantic and Claude Code harnesses and report similar rankings.

## Results
- GPT-5.6 Sol achieved 100% recall, 0.91 F1, and a cost of $0.70 per PR. The authors report that it was about 45% cheaper than GPT-5.5 at similar performance.
- Grok 4.5 reached the reported frontier at $0.20 per PR with 0.77 F1, 74% recall, and 80.4% precision.
- Gemini 3.1 Flash Lite cost about $0.04 per PR and achieved 0.75 F1, 68% recall, and 82.9% precision.
- Fable 5 with an Opus 4.8 fallback cost about $3.61 per PR and ranked below GPT-5.6 Sol on both quality and cost. The fallback occurred in 10.7% of runs.
- No tested Anthropic model reached the reported cost-quality frontier.
- The benchmark covers PR scans only, so the results do not establish model rankings for open-ended full-code vulnerability scans.

## Link
- [https://docs.damsecure.ai/blog/pr-review-security-benchmark/](https://docs.damsecure.ai/blog/pr-review-security-benchmark/)
