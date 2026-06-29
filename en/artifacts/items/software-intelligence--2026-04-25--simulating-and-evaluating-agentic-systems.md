---
source: hn
url: https://www.gojiberries.io/simulating-and-evaluating-agentic-systems/
published_at: '2026-04-25T23:00:50'
authors:
- neehao
topics:
- agent-evaluation
- agent-simulation
- multi-agent-systems
- llm-judge
- software-testing
relevance_score: 0.95
run_id: materialize-outputs
language_code: en
---

# Simulating and Evaluating Agentic Systems

## Summary
The paper argues that testing agentic systems needs simulation plus evaluation, because fixed prompt datasets and transcript-only checks miss failures that emerge across multi-step actions, tools, and state changes. It lays out a practical sim/eval stack with scenario design, synthetic users, structured episode logs, deterministic assertions, and calibrated model-based judges.

## Problem
- Agentic systems act over many steps, branch in response to ambiguous input, use tools, and maintain state, so fixed golden datasets break when the agent takes a valid but different path.
- Transcript-only assertions can pass even when the agent never used the right tool or changed the backend state incorrectly; language is not the system of record.
- Single-pass LLM judges are noisy and biased. The paper names position bias, verbosity bias, self-enhancement bias, low intra-rater reliability, and prompt sensitivity as failure modes.

## Approach
- Split sim/eval into three separate stages: scenario data, simulation run, and episode evaluation. Keep them separate so teams can tell whether a failure came from bad scenarios, a bad simulator, or a bad judge.
- Define each scenario with a starting prompt, user goal, branching conversation plan, persona, backend fixtures, and explicit expectations such as allowed terminal states and forbidden actions.
- Run the real agent end-to-end against a controlled environment with mocked external services and a synthetic user, usually an LLM, that follows the scenario plan while adapting to the agent's actual behavior.
- Log each episode as structured artifacts: world state after the run, tool-call trace, transcript, and any downstream surface such as screenshots, telemetry, or audio.
- Grade episodes with four assertion classes: outcome assertions on end state, procedure assertions on tool usage, consistency assertions across trace and transcript, and surface assertions on what the user-facing channel actually showed or did. Use deterministic checks where possible, and use model-based grading only for narrow questions with aggregation and calibration.

## Results
- The excerpt does not report benchmark scores, win rates, or ablation numbers.
- It claims sim/eval covers behavior that unit tests, contract tests, and component integration tests cannot reach: decision branching, ambiguity handling, tool use in context, recovery from misunderstanding, and end-to-end task resolution.
- It gives one concrete traffic-weighting example: if 40% of production volume is order-status inquiries, the scenario mix should reflect that rather than over-sampling return requests.
- It recommends repeated trials per scenario and reporting pass^k, the probability that all k runs pass, plus distributions for turns, steps, tokens, latency, and tool calls instead of single-run point estimates.
- It names concrete implementation options and tools: Google's ADK user simulation as a reference pattern, CheckList (Ribeiro et al., 2020) for pairwise directional tests, and three stack tools: understudy, mimiq, and layoutlens.

## Link
- [https://www.gojiberries.io/simulating-and-evaluating-agentic-systems/](https://www.gojiberries.io/simulating-and-evaluating-agentic-systems/)
