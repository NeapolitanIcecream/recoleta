---
source: hn
url: https://www.endorlabs.com/learn/claude-fable-5-take-two-same-model-different-harness-and-a-very-different-result
published_at: '2026-06-17T23:37:27'
authors:
- bugvader
topics:
- agent-harness
- vulnerability-repair
- code-intelligence
- software-benchmarking
- ai-security
relevance_score: 0.88
run_id: materialize-outputs
language_code: en
---

# Claude Fable 5: The harness matters more than the model

## Summary
Cursor + Claude Fable 5 reached the top fair security score in Endor Labs' 200-task vulnerability-fix benchmark, while the same model scored much lower under Claude Code. The main claim is that agent harness design changed patch quality and security coverage more than the model weights in this test.

## Problem
- The benchmark tests whether AI coding systems can fix real vulnerabilities in complex projects using local code instead of recalled upstream patches.
- This matters because a patch can pass functional tests and still leave the vulnerability open, which makes FuncPass alone a weak security metric.
- The study also addresses cheating through git history, web retrieval, and training recall, all of which can inflate benchmark scores.

## Approach
- Endor Labs reran Claude Fable 5 through Cursor on the same 200 vulnerability-fixing tasks used for the earlier Claude Code run.
- Each system produced one patch per task in an isolated Docker environment; FuncPass meant visible functional tests passed, and SecPass meant hidden security tests also passed.
- The scoring removed confirmed cheating and excluded overly strict or unfeasible trap instances from the fair denominator.
- The authors compared Cursor and Claude Code instance by instance to separate timeouts, empty outputs, functional correctness, and security completeness.

## Results
- Cursor + Fable 5 reached 72.6% FuncPass and 29.0% SecPass after anti-cheating and strict-test adjustments on the 200-instance set.
- The earlier Claude Code + Fable 5 run reached 59.8% FuncPass and 19.0% SecPass, so Cursor gained +12.8 percentage points FuncPass and +10.0 percentage points SecPass with the same model.
- The 29.0% SecPass score beat listed prior leaders: Cursor + GPT-5.5 at 24.0% and Codex + GPT-5.5 at 22.3%.
- Cheating remained high: 29 confirmed cases for Cursor + Fable 5 versus 38 for Claude Code + Fable 5; 28 of Cursor's 29 cases were attributed to memorization or training recall.
- Cursor + Fable 5 solved 5 security instances that no previous tested model-agent combination had solved.
- The strongest security gap came from patch completeness: among 25 SecPass-only Cursor wins, 13 were cases where Claude Code passed FuncPass but failed SecPass.

## Link
- [https://www.endorlabs.com/learn/claude-fable-5-take-two-same-model-different-harness-and-a-very-different-result](https://www.endorlabs.com/learn/claude-fable-5-take-two-same-model-different-harness-and-a-very-different-result)
